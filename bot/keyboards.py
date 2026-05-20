from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔍 Qidirish", callback_data="search"),
            InlineKeyboardButton(text="🤖 AI Chat", callback_data="ai_chat")
        ],
        [
            InlineKeyboardButton(text="❤️ Sevimlilar", callback_data="favorites"),
            InlineKeyboardButton(text="🎁 Referral", callback_data="referral")
        ],
        [
            InlineKeyboardButton(text="📋 Statistika", callback_data="stats"),
            InlineKeyboardButton(text="💰 Premium", callback_data="buy_premium")
        ]
    ])
    return keyboard

def quality_keyboard(video_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="480p", callback_data=f"quality_480_{video_id}"),
            InlineKeyboardButton(text="720p", callback_data=f"quality_720_{video_id}"),
            InlineKeyboardButton(text="1080p", callback_data=f"quality_1080_{video_id}")
        ],
        [
            InlineKeyboardButton(text="❤️ Saqlash", callback_data=f"favorite_{video_id}")
        ]
    ])
    return keyboard

def search_result_keyboard(video_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📥 Yuklab olish", callback_data=f"download_{video_id}")
        ],
        [
            InlineKeyboardButton(text="❤️ Sevimlilarga qo'shish", callback_data=f"favorite_{video_id}")
        ]
    ])
    return keyboard

def progress_keyboard(text: str = "⏳ Yuklanmoqda..."):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="progress")]
    ])
    return keyboard
