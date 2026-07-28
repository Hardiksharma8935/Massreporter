import logging
from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.config import ADMIN_ID
from app.telethon_client import execute_report

router = Router()

@router.message(F.from_user.id != ADMIN_ID)
async def unauthorized_access(message: types.Message):
    logging.warning(f"Unauthorized access attempt from {message.from_user.id}")
    return

@router.message(F.text)
async def manual_review_prompt(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
        
    target = message.text
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚨 Report CSAM", callback_data=f"report_csam_{target}")],
        [InlineKeyboardButton(text="🚫 Report Scam", callback_data=f"report_scam_{target}")],
        [InlineKeyboardButton(text="✅ Ignore", callback_data="ignore")]
    ])
    await message.reply(f"Review target: {target}\nSelect an action to dispatch from authorized accounts:", reply_markup=kb)

@router.callback_query(F.data.startswith("report_"))
async def process_report(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return
        
    parts = callback.data.split("_", 2)
    if len(parts) < 3:
        await callback.answer("Invalid data")
        return
        
    action = parts[1]
    target = parts[2]
    
    await callback.message.edit_text(f"⏳ Executing {action} report on {target}...")
    
    success = await execute_report(target, action)
    
    if success:
        await callback.message.edit_text(f"✅ Successfully reported {target} for {action}. Action logged.")
    else:
        await callback.message.edit_text(f"❌ Failed to report {target}. Check logs for rate limits or errors.")
    await callback.answer()

@router.callback_query(F.data == "ignore")
async def process_ignore(callback: types.CallbackQuery):
    await callback.message.edit_text("✅ Target ignored. No action taken.")
    await callback.answer()
  
