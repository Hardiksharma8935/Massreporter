import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import InputReportReasonChildAbuse, InputReportReasonSpam
from telethon.errors import FloodWaitError
from app.config import API_ID, API_HASH
from app.database import AsyncSessionLocal
from app.models import AuditLog, AuthorizedAccount
from sqlalchemy.future import select
from app.encryption import decrypt_session

async def execute_report(target: str, reason_str: str) -> bool:
    reason = InputReportReasonChildAbuse() if reason_str == "csam" else InputReportReasonSpam()
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(AuthorizedAccount).limit(1))
        account = result.scalars().first()
        
        if not account:
            logging.error("No authorized accounts found.")
            return False
            
        decrypted_session = decrypt_session(account.encrypted_session)
    
    client = TelegramClient(StringSession(decrypted_session), API_ID, API_HASH)
    
    try:
        await client.connect()
        if not await client.is_user_authorized():
            logging.error("Session is not authorized.")
            return False
            
        await client(ReportRequest(
            peer=target,
            id=[1],
            reason=reason,
            message="Violates Telegram Terms of Service."
        ))
        
        async with AsyncSessionLocal() as db_session:
            new_log = AuditLog(
                target_entity=target,
                reason=reason_str,
                timestamp=datetime.utcnow()
            )
            db_session.add(new_log)
            await db_session.commit()
            
        return True
    except FloodWaitError as e:
        logging.error(f"Rate limited. Must wait {e.seconds} seconds.")
        return False
    except Exception as e:
        logging.error(f"Error executing report: {e}")
        return False
    finally:
        await client.disconnect()
      
