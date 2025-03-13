from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json

# Замените на ваш токен и ID администратора
BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_CHAT_ID = 123456789  # ID чата администратора

def handle_web_app_data(update: Update, context: CallbackContext) -> None:
    # Получаем данные из Mini App
    data = update.message.web_app_data.data
    data = json.loads(data)
    
    if data["action"] == "request_price":
        item_name = data["item"]
        user = update.message.from_user
        message = f"Пользователь {user.first_name} {user.last_name} запросил цену на товар: {item_name}"
        
        # Отправляем сообщение администратору
        context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик данных из Mini App
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_web_app_data))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

def add_item(update: Update, context: CallbackContext) -> None:
    # Проверяем, что команду вызвал администратор
    if update.message.from_user.id != ADMIN_CHAT_ID:
        update.message.reply_text("У вас нет прав для выполнения этой команды.")
        return

    try:
        # Парсим аргументы команды
        category, name, description, photo = context.args
        
        # Загружаем текущие данные
        with open("data.json", "r") as file:
            data = json.load(file)
        
        # Добавляем новый товар
        data.append({
            "category": category,
            "name": name,
            "description": description,
            "img": [photo]
        })
        
        # Сохраняем обновленные данные
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
        
        update.message.reply_text(f"Товар {name} добавлен в категорию {category}.")
    except ValueError:
        update.message.reply_text("Использование: /add_item <категория> <название> <описание> <фото>")

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Обработчик данных из Mini App
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_web_app_data))

    # Команда для добавления товара
    dispatcher.add_handler(CommandHandler("add_item", add_item))

    updater.start_polling()
    updater.idle()