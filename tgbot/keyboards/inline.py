from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup()

sub_admin_keyboard = InlineKeyboardMarkup()

statistics_button = InlineKeyboardButton(text="Статистика", callback_data="statistics")
all_time_button = InlineKeyboardButton(text="За все время", callback_data="all_time")
last_7_days_button = InlineKeyboardButton(text="Последние 7 дней", callback_data="last_7_days")
mailing_button = InlineKeyboardButton(text="Рассылка", callback_data="mailing")

admin_keyboard.add(statistics_button)
sub_admin_keyboard.add(all_time_button)
sub_admin_keyboard.add(last_7_days_button)
admin_keyboard.add(mailing_button)

feedback_client_keyboard = InlineKeyboardMarkup()
feedback_client_keyboard.add(
    InlineKeyboardButton(text="Доволен ✅", callback_data="positive_feedback"),
    InlineKeyboardButton(text="Не доволен ⛔️", callback_data="negative_feedback")
)

negative_feedback_client_keyboard = InlineKeyboardMarkup()
negative_feedback_client_keyboard.row(
    InlineKeyboardButton(text="Индивидуальный заказ 🦄", url="https://t.me/andre7777andre"),
    InlineKeyboardButton(text="Закрытый канал 😈", url="https://t.me/+yF0w8WOrS20wMDRi")
)