"""Telegram-бот магазина lopendres2 + запросы из Mini App.

Требуется python-telegram-bot >= 20 (в проекте — 22.x).

Настройка:
    1. Скопируйте .env.example в .env и впишите BOT_TOKEN от @BotFather.
    2. Узнайте свой chat_id командой /myid и добавьте его в ADMIN_IDS.

Запуск:
    python bot.py
"""

from __future__ import annotations

import html
import json
import logging
import os
from pathlib import Path
from typing import Any

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    MenuButtonWebApp,
    ReplyKeyboardMarkup,
    Update,
    WebAppInfo,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    TypeHandler,
    filters,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = Path(os.getenv("DATA_FILE") or BASE_DIR / "data" / "data.json")
DEFAULT_WEBAPP_URL = "https://lopendres2.github.io/"

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("shop-bot")


# --------------------------------------------------------------------------- #
# Конфигурация
# --------------------------------------------------------------------------- #
def load_env_file(path: Path = BASE_DIR / ".env") -> None:
    """Минимальная замена python-dotenv: KEY=VALUE построчно."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = {
    int(part)
    for part in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",")
    if part.lstrip("-").isdigit()
}
WEBAPP_URL = (os.getenv("WEBAPP_URL") or DEFAULT_WEBAPP_URL).strip()

if not BOT_TOKEN:
    raise SystemExit(
        "Не задан BOT_TOKEN.\n"
        "Создайте файл .env рядом с bot.py со строкой:\n"
        "    BOT_TOKEN=123456:AA...\n"
        "или задайте переменную окружения BOT_TOKEN."
    )


# --------------------------------------------------------------------------- #
# Работа с каталогом (data/data.json)
# --------------------------------------------------------------------------- #
def load_catalog() -> list[dict[str, Any]]:
    if not DATA_FILE.exists():
        log.warning("Файл каталога не найден: %s", DATA_FILE)
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        log.error("Битый JSON в %s: %s", DATA_FILE, exc)
        return []
    return data if isinstance(data, list) else []


def save_catalog(items: list[dict[str, Any]]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    tmp.replace(DATA_FILE)


def find_item(name: str) -> dict[str, Any] | None:
    needle = name.strip().casefold()
    for item in load_catalog():
        if str(item.get("name", "")).strip().casefold() == needle:
            return item
    return None


def item_card(item: dict[str, Any]) -> str:
    lines = [f"<b>{html.escape(str(item.get('name', '—')))}</b>"]
    if item.get("category"):
        lines.append(f"Категория: {html.escape(str(item['category']))}")
    if item.get("price"):
        lines.append(f"Цена: {html.escape(str(item['price']))} ₽")
    if item.get("description"):
        lines.append("")
        lines.append(html.escape(str(item["description"])))
    return "\n".join(lines)


def is_admin(update: Update) -> bool:
    user = update.effective_user
    return bool(user and user.id in ADMIN_IDS)


async def deny(update: Update) -> None:
    await update.effective_message.reply_text(
        "Команда доступна только администратору.\n"
        "Свой ID можно узнать командой /myid."
    )


# --------------------------------------------------------------------------- #
# Клавиатуры
# --------------------------------------------------------------------------- #
def main_keyboard() -> InlineKeyboardMarkup:
    if WEBAPP_URL.startswith("https://"):
        button = InlineKeyboardButton(
            "🛍 Открыть каталог", web_app=WebAppInfo(url=WEBAPP_URL)
        )
    else:
        button = InlineKeyboardButton("🛍 Открыть каталог", url=WEBAPP_URL)
    return InlineKeyboardMarkup([[button]])


def menu_button() -> ReplyKeyboardMarkup | None:
    """Кнопка Mini App рядом с полем ввода (только для https-ссылки)."""
    if not WEBAPP_URL.startswith("https://"):
        return None
    return ReplyKeyboardMarkup(
        [[KeyboardButton("🛍 Каталог", web_app=WebAppInfo(url=WEBAPP_URL))]],
        resize_keyboard=True,
        is_persistent=True,
    )


# --------------------------------------------------------------------------- #
# Команды
# --------------------------------------------------------------------------- #
WELCOME = (
    "Привет, {name}! 👋\n\n"
    "Это бот магазина <b>lopendres2</b>.\n"
    "Откройте каталог кнопкой ниже, выберите товар и нажмите "
    "«Запросить цену» — заявка сразу придёт продавцу.\n\n"
    "Доступные команды: /catalog, /myid, /help"
)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = WELCOME.format(name=html.escape(user.first_name or "друг"))
    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard(),
    )
    keyboard = menu_button()
    if keyboard:
        await update.effective_message.reply_text(
            "Кнопка «🛍 Каталог» также закреплена внизу 👇",
            reply_markup=keyboard,
        )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = [
        "<b>Что умеет бот</b>",
        "/start — открыть каталог, /catalog — список товаров",
        "/myid — показать ваш Telegram ID",
    ]
    if is_admin(update):
        lines += [
            "",
            "<b>Для администратора</b>",
            "/add_item категория | название | цена | описание | ссылка_на_фото",
            "/del_item название — удалить товар",
            "/items — список товаров с ID",
            "/reload — перечитать data.json",
        ]
    await update.effective_message.reply_text(
        "\n".join(lines), parse_mode=ParseMode.HTML
    )


async def cmd_myid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.effective_message.reply_text(
        f"Ваш ID: <code>{user.id}</code>\n"
        f"Чат: <code>{update.effective_chat.id}</code>\n\n"
        "Добавьте ID в ADMIN_IDS в файле .env, чтобы получить права "
        "администратора.",
        parse_mode=ParseMode.HTML,
    )


async def cmd_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = load_catalog()
    if not items:
        await update.effective_message.reply_text(
            "Каталог пока пуст.", reply_markup=main_keyboard()
        )
        return

    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(str(item.get("category") or "Без категории"), []).append(item)

    chunks: list[str] = ["<b>Каталог</b>"]
    for category, category_items in grouped.items():
        chunks.append(f"\n<b>{html.escape(category)}</b>")
        for item in category_items:
            price = item.get("price")
            suffix = f" — {html.escape(str(price))} ₽" if price else ""
            chunks.append(f"• {html.escape(str(item.get('name', '—')))}{suffix}")
    chunks.append("\nПодробности и фото — в Mini App.")
    await update.effective_message.reply_text(
        "\n".join(chunks),
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard(),
    )


async def cmd_add_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await deny(update)
        return

    raw = " ".join(context.args)
    parts = [part.strip() for part in raw.split("|")]
    if len(parts) < 3:
        await update.effective_message.reply_text(
            "Формат:\n"
            "<code>/add_item категория | название | цена | описание | ссылка_на_фото</code>\n\n"
            "Описание и фото необязательны.",
            parse_mode=ParseMode.HTML,
        )
        return

    category, name, price = parts[0], parts[1], parts[2]
    description = parts[3] if len(parts) > 3 else ""
    photo = parts[4] if len(parts) > 4 else ""

    if find_item(name):
        await update.effective_message.reply_text(
            f"Товар «{name}» уже есть. Сначала удалите его: /del_item {name}"
        )
        return

    items = load_catalog()
    items.append(
        {
            "category": category,
            "name": name,
            "price": price,
            "description": description,
            "img": [photo] if photo else [],
        }
    )
    save_catalog(items)
    log.info("Добавлен товар %r (%s) пользователем %s", name, category, update.effective_user.id)
    await update.effective_message.reply_text(
        f"✅ Товар «{name}» добавлен в категорию «{category}»."
    )


async def cmd_del_item(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await deny(update)
        return

    name = " ".join(context.args).strip()
    if not name:
        await update.effective_message.reply_text(
            "Укажите название: /del_item Название товара"
        )
        return

    items = load_catalog()
    kept = [item for item in items if str(item.get("name", "")).casefold() != name.casefold()]
    if len(kept) == len(items):
        await update.effective_message.reply_text(f"Товар «{name}» не найден.")
        return

    save_catalog(kept)
    await update.effective_message.reply_text(
        f"🗑 Удалено позиций: {len(items) - len(kept)} («{name}»)."
    )


async def cmd_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await deny(update)
        return

    items = load_catalog()
    if not items:
        await update.effective_message.reply_text("Каталог пуст.")
        return

    lines = [f"<b>Товары ({len(items)})</b>"]
    for index, item in enumerate(items, start=1):
        lines.append(
            f"{index}. {html.escape(str(item.get('name', '—')))}"
            f" — {html.escape(str(item.get('price', '—')))} ₽"
            f" — {html.escape(str(item.get('category') or 'без категории'))}"
        )
    await update.effective_message.reply_text(
        "\n".join(lines), parse_mode=ParseMode.HTML
    )


async def cmd_reload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await deny(update)
        return
    items = load_catalog()
    await update.effective_message.reply_text(
        f"Каталог перечитан: {len(items)} позиций в {DATA_FILE}."
    )


# --------------------------------------------------------------------------- #
# Данные из Mini App
# --------------------------------------------------------------------------- #
async def notify_admins(context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    sent = 0
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            sent += 1
        except Exception as exc:  # noqa: BLE001 — один админ не должен ломать остальных
            log.error("Не удалось отправить сообщение %s: %s", admin_id, exc)
    if not sent:
        log.error(
            "Заявка не доставлена: ADMIN_IDS пуст или недоступен. "
            "Сообщение:\n%s",
            text,
        )


def describe_user(update: Update) -> str:
    user = update.effective_user
    name = html.escape(" ".join(filter(None, [user.first_name, user.last_name])))
    username = f" (@{html.escape(user.username)})" if user.username else ""
    return f"{name}{username}, id <code>{user.id}</code>"


def format_request(payload: dict[str, Any], update: Update) -> str:
    action = str(payload.get("action", ""))
    item_name = str(payload.get("item", "")).strip()
    catalog_item = find_item(item_name) if item_name else None
    title = {
        "request_price": "💰 Запрос цены",
        "request_item": "🛒 Заявка на товар",
    }.get(action, "📩 Сообщение из Mini App")

    parts = [f"<b>{title}</b>", f"От: {describe_user(update)}"]
    parts.append(f"Товар: <b>{html.escape(item_name or '—')}</b>")
    if catalog_item:
        if catalog_item.get("price"):
            parts.append(f"Цена в каталоге: {html.escape(str(catalog_item['price']))} ₽")
        if catalog_item.get("img"):
            photo = catalog_item["img"][0]
            if photo:
                parts.append(f'<a href="{html.escape(str(photo))}">Фото товара</a>')
    if action not in {"request_price", "request_item"}:
        parts.append(f"\nДанные: <code>{html.escape(json.dumps(payload, ensure_ascii=False))}</code>")
    return "\n".join(parts)


def format_order(items: list[Any], update: Update) -> str:
    lines = ["<b>🧾 Новая заявка из Mini App</b>", f"От: {describe_user(update)}", ""]
    total = 0
    for index, entry in enumerate(items, start=1):
        if isinstance(entry, dict):
            name = str(entry.get("name") or entry.get("item") or "—")
        else:
            name = str(entry)
        catalog_item = find_item(name)
        price = None
        if catalog_item and str(catalog_item.get("price", "")).isdigit():
            price = int(catalog_item["price"])
            total += price
        price_text = f" — {price} ₽" if price is not None else ""
        lines.append(f"{index}. {html.escape(name)}{price_text}")
    if total:
        lines.append(f"\nИтого: <b>{total} ₽</b>")
    return "\n".join(lines)


async def on_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    raw = message.web_app_data.data
    try:
        payload = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        text = (
            f"📩 Данные из Mini App\nОт: {describe_user(update)}\n"
            f"<code>{html.escape(str(raw))}</code>"
        )
        await notify_admins(context, text)
        await message.reply_text("Заявка отправлена продавцу ✅")
        return

    if isinstance(payload, list):
        text = format_order(payload, update)
    elif isinstance(payload, dict):
        text = format_request(payload, update)
    else:
        text = f"📩 Данные из Mini App\nОт: {describe_user(update)}\n<code>{html.escape(raw)}</code>"

    await notify_admins(context, text)
    await message.reply_text(
        "Спасибо! Заявка отправлена продавцу, он свяжется с вами ✅",
        reply_markup=main_keyboard(),
    )


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Не понял сообщение 🤔\nОткройте каталог кнопкой ниже или нажмите /help.",
        reply_markup=main_keyboard(),
    )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.exception("Ошибка при обработке апдейта", exc_info=context.error)


async def log_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Пишем в лог, кто написал боту — удобно для настройки ADMIN_IDS."""
    user = update.effective_user
    if user:
        log.info(
            "Апдейт: %s (@%s, id=%s) → %s",
            user.full_name,
            user.username,
            user.id,
            getattr(update.effective_message, "text", None) or update.effective_message,
        )


# --------------------------------------------------------------------------- #
# Запуск
# --------------------------------------------------------------------------- #
async def post_init(application: Application) -> None:
    bot = application.bot
    me = await bot.get_me()
    log.info("Бот запущен: @%s (id=%s)", me.username, me.id)
    if not ADMIN_IDS:
        log.warning(
            "ADMIN_IDS пуст — заявки некому отправлять. "
            "Напишите боту /myid и добавьте ID в .env."
        )
    if WEBAPP_URL.startswith("https://"):
        try:
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(
                    text="Каталог", web_app=WebAppInfo(url=WEBAPP_URL)
                )
            )
            log.info("Кнопка меню Mini App: %s", WEBAPP_URL)
        except Exception as exc:  # noqa: BLE001
            log.warning("Не удалось обновить кнопку меню: %s", exc)
    else:
        log.warning("WEBAPP_URL должен начинаться с https:// — сейчас %r", WEBAPP_URL)


def build_application() -> Application:
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    handlers = [
        CommandHandler("start", cmd_start),
        CommandHandler("help", cmd_help),
        CommandHandler("catalog", cmd_catalog),
        CommandHandler("myid", cmd_myid),
        CommandHandler("add_item", cmd_add_item),
        CommandHandler("del_item", cmd_del_item),
        CommandHandler("items", cmd_items),
        CommandHandler("reload", cmd_reload),
        MessageHandler(filters.StatusUpdate.WEB_APP_DATA, on_web_app_data),
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_text),
    ]
    for handler in handlers:
        application.add_handler(handler)
    application.add_handler(TypeHandler(Update, log_update), group=-1)
    application.add_error_handler(on_error)
    return application


def main() -> None:
    build_application().run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Бот остановлен")
