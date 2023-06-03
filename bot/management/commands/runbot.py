from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from django.core.management import BaseCommand
from VideoDownloaderBot.settings import TOKEN
from bot.views import start, url_handler, inline_handler


class Command(BaseCommand):
    def handle(self, *args, **options):
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.Entity('url'), url_handler))
        application.add_handler(CallbackQueryHandler(inline_handler))
        application.run_polling()
