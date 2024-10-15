import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler

tooth_info = [
    "Чистить зубы необходимо не менее 2 минут.",
    "Зубную щётку нужно менять каждые 3 месяца.",
    "После употребления пищи полезно использовать зубную нить.",
    "Регулярные визиты к стоматологу помогают избежать проблем с зубами."
]

dental_sites = [
    "https://www.stom.ru/",
    "https://www.dentalcentr.ru/",
    "https://www.mosdental.ru/",
    "https://www.smile-at-once.ru/",
    "https://vrn.docdoc.ru/clinic/klinika_renessans"
]

scheduler = BackgroundScheduler()


async def send_reminder(context):
    job = context.job
    chat_id = job.args[0]
    await context.bot.send_message(chat_id=chat_id, text="Напоминание: не забудьте почистить зубы!")


async def start(update: Update, context) :
    panel = [
        [InlineKeyboardButton("Полезная информация", callback_data='info')],
        [InlineKeyboardButton("Случайный стоматологический сайт", callback_data='site')],
        [InlineKeyboardButton("Напоминания о чистке зубов", callback_data='reminders')]
    ]
    reply_markup = InlineKeyboardMarkup(panel)
    await update.message.reply_text('Привет! Я бот для здоровья зубов. Чем могу помочь?', reply_markup=reply_markup)


async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        info_message = random.choice(tooth_info)
        await query.edit_message_text(text=f"Полезная информация: {info_message}")
    elif query.data == 'site':
        site_link = random.choice(dental_sites)
        await query.edit_message_text(text=f"Вот случайный стоматологический сайт: {site_link}")
    elif query.data == 'reminders':
        await start_reminders(update, query, context)


def schedule_reminders(chat_id):
    if not scheduler.running:
        scheduler.start()
    scheduler.add_job(send_reminder, 'cron', hour=8, minute=0, args=[chat_id])
    scheduler.add_job(send_reminder, 'cron', hour=20, minute=0, args=[chat_id])


async def start_reminders(update: Update, query, context):
    chat_id = query.message.chat.id
    schedule_reminders(chat_id)
    await query.message.reply_text('Напоминания установлены!')


async def soobcheniya(update: Update, context):
    await update.message.reply_text("Я не умею отвечать на ваши сообщения, напишите /start")


def main():
    token_telega = "Место для токена"
    zubnoy_bot = Application.builder().token(token_telega).build()
    zubnoy_bot.add_handler(CommandHandler('start', start))
    zubnoy_bot.add_handler(CallbackQueryHandler(button))
    zubnoy_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, soobcheniya))
    zubnoy_bot.run_polling()

if __name__ == '__main__':
    main()