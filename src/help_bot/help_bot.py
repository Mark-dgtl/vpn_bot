import asyncio
from collections import deque
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from src.config import settings
import urllib.parse

bot = Bot(token=settings.HELP_BOT_TOKEN)
dp = Dispatcher()

# Хранилище для связи message_id в чате админа -> user_id
# Используем deque для ограничения количества записей
admin_message_links = deque(maxlen=200)

# Список заблокированных пользователей
banned_users = set()

# Локальное хранилище метаданных пользователей, получаемых через deep link
# Формат: user_meta[user_id] = {"reg_date": "...", "subs_status": "..."}
user_meta: dict[int, dict] = {}


@dp.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandStart):
    # Если админ зашёл — показываем админ-панель
    if message.chat.id == settings.ADMIN_ID:
        await message.answer(
            "👋 Привет, администратор! Вы получаете сообщения от пользователей.\n\n"
            "<b>Команды модерации:</b>\n"
            "🚫 <code>бан</code> или <code>/ban</code> - заблокировать пользователя (ответ на его сообщение)\n"
            "✅ <code>разбан</code> или <code>/unban</code> - разблокировать пользователя\n\n"
            f"📊 Заблокировано пользователей: {len(banned_users)}",
            parse_mode=ParseMode.HTML
        )
        return

    if message.from_user.id in banned_users:
        await message.answer(
            "⛔️ 🗑Вы заблокированы в боте поддержки.⛔️\n"
            "Если считаете это ошибкой, свяжитесь с администратором другим способом."
        )
        return

    args = command.args
    if args in ("1", "2"):
        if args == "1":
            subs_status = "Активна"
        if args =="2":
            subs_status = "Неактивна"

        user_meta[message.from_user.id] = {
            "subs_status": subs_status
        }
    else:
        user_meta[message.from_user.id] = {
            "subs_status": "Неизвестно"
        }

    await message.answer(
        "👋 Привет! Я бот поддержки.\n\n"
        "Отправьте мне ваш вопрос, и я передам его в службу поддержки."
    )


@dp.message(lambda m: m.chat.id == settings.ADMIN_ID and m.reply_to_message)
async def handle_admin_reply(message: types.Message):
    """Обработка ответа администратора"""
    replied_to_id = message.reply_to_message.message_id

    # Ищем пользователя, которому нужно ответить
    user_id = None
    for msg_id, uid in admin_message_links:
        if replied_to_id == msg_id:
            user_id = uid
            break

    if not user_id:
        await message.answer(
            "⚠️ Не удалось найти получателя.\n"
            "Возможно, сообщение слишком старое или не является запросом пользователя, или бот был перезапущен."
        )
        return

    # Проверяем команду БАН
    if message.text and message.text.strip().lower() in ['/ban', 'бан', '/бан', 'ban']:
        banned_users.add(user_id)
        try:
            await bot.send_message(
                chat_id=user_id,
                text="⛔️ 🗑Вы были заблокированы в боте поддержки за нарушение правил использования."
            )
        except:
            pass  # Пользователь мог заблокировать бота

        await message.answer(
            f"🚫 <b>Пользователь заблокирован!</b>\n\n"
            f"📊 Всего забанено: {len(banned_users)}",
            parse_mode=ParseMode.HTML
        )
        return

    # Проверяем команду РАЗБАН
    if message.text and message.text.strip().lower() in ['/unban', 'разбан', '/разбан', 'unban']:
        if user_id in banned_users:
            banned_users.remove(user_id)
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text="✅ Вы были разблокированы! Теперь вы снова можете обращаться в поддержку."
                )
            except:
                pass

            await message.answer(
                f"✅ <b>Пользователь разблокирован!</b>\n\n"
                f"📊 Всего забанено: {len(banned_users)}",
                parse_mode=ParseMode.HTML
            )
        else:
            await message.answer("⚠️ Этот пользователь не был заблокирован.")
        return

    try:
        # Отправляем ответ пользователю
        if message.text:
            await bot.send_message(
                chat_id=user_id,
                text=f"💬 <b>Ответ от поддержки:</b>\n\n{message.text}",
                parse_mode=ParseMode.HTML
            )
        elif message.photo:
            await bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=f"💬 <b>Ответ от поддержки:</b>\n\n{message.caption or ''}",
                parse_mode=ParseMode.HTML
            )
        elif message.document:
            await bot.send_document(
                chat_id=user_id,
                document=message.document.file_id,
                caption=f"💬 <b>Ответ от поддержки:</b>\n\n{message.caption or ''}",
                parse_mode=ParseMode.HTML
            )
        elif message.video:
            await bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=f"💬 <b>Ответ от поддержки:</b>\n\n{message.caption or ''}",
                parse_mode=ParseMode.HTML
            )
        else:
            # Для других типов сообщений
            await message.copy_to(chat_id=user_id)

        # Подтверждаем админу
        await message.answer("✅ Ответ успешно отправлен пользователю!")

    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке сообщения пользователю:\n{e}")


@dp.message()
async def handle_user_message(message: types.Message):
    """Обработка сообщений от пользователей"""
    # Игнорируем сообщения от админа, если они не являются ответами
    if message.chat.id == settings.ADMIN_ID:
        # Если админ отправил сообщение без reply, подсказываем
        await message.answer(
            "💡 Чтобы ответить пользователю, используйте <b>Ответить (Reply)</b> на его сообщение.\n\n"
            "Для блокировки ответьте на сообщение пользователя командой <code>бан</code>",
            parse_mode=ParseMode.HTML
        )
        return

    # Проверяем, не заблокирован ли пользователь
    if message.from_user.id in banned_users:
        await message.answer(
            "⛔️ 🗑Вы заблокированы в боте поддержки.\n"
            "Если считаете это ошибкой, свяжитесь с администратором другим способом."
        )
        return

    user = message.from_user
    admin_id = settings.ADMIN_ID

    meta = user_meta.get(user.id, {})
    subs_status_str = meta.get("subs_status", "Неизвестно")

    # Безопасное получение full_name
    try:
        fullname = user.full_name
    except Exception:
        fullname = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Пользователь"

    # Формируем информацию о пользователе в требуемом формате
    user_info = (
        f"📩 <b>Новое обращение от #{fullname}</b>\n\n"
        f"Подписка: {subs_status_str}\n"
        f"🔗 Профиль: tg://user?id={user.id}\n"
        f"{'🙋 Username: @' + user.username if user.username else ''}\n"
    )

    try:
        # Отправляем сообщение админу в зависимости от типа
        if message.text:
            sent_message = await bot.send_message(
                chat_id=admin_id,
                text=f"{user_info}\n💬 <b>Сообщение:</b>\n{message.text}",
                parse_mode=ParseMode.HTML
            )
        elif message.photo:
            sent_message = await bot.send_photo(
                chat_id=admin_id,
                photo=message.photo[-1].file_id,
                caption=f"{user_info}\n📷 <b>Фото с текстом:</b>\n{message.caption or '(без текста)'}",
                parse_mode=ParseMode.HTML
            )
        elif message.document:
            sent_message = await bot.send_document(
                chat_id=admin_id,
                document=message.document.file_id,
                caption=f"{user_info}\n📎 <b>Документ:</b>\n{message.caption or '(без описания)'}",
                parse_mode=ParseMode.HTML
            )
        elif message.video:
            sent_message = await bot.send_video(
                chat_id=admin_id,
                video=message.video.file_id,
                caption=f"{user_info}\n🎥 <b>Видео:</b>\n{message.caption or '(без описания)'}",
                parse_mode=ParseMode.HTML
            )
        elif message.voice:
            sent_message = await bot.send_voice(
                chat_id=admin_id,
                voice=message.voice.file_id,
                caption=f"{user_info}\n🎤 <b>Голосовое сообщение</b>",
                parse_mode=ParseMode.HTML
            )
        elif message.audio:
            sent_message = await bot.send_audio(
                chat_id=admin_id,
                audio=message.audio.file_id,
                caption=f"{user_info}\n🎵 <b>Аудио:</b>\n{message.caption or '(без описания)'}",
                parse_mode=ParseMode.HTML
            )
        elif message.sticker:
            # Сначала отправляем информацию
            info_msg = await bot.send_message(
                chat_id=admin_id,
                text=f"{user_info}\n🎭 <b>Стикер:</b>",
                parse_mode=ParseMode.HTML
            )
            # Затем сам стикер
            sent_sticker = await bot.send_sticker(
                chat_id=admin_id,
                sticker=message.sticker.file_id
            )
            # Сохраняем ID информационного сообщения
            admin_message_links.append((info_msg.message_id, user.id))
            # не используем sent_message дальше
            sent_message = info_msg
        else:
            # Для остальных типов пробуем просто переслать
            sent_message = await bot.send_message(
                chat_id=admin_id,
                text=f"{user_info}\n📨 <b>Сообщение другого типа</b>",
                parse_mode=ParseMode.HTML
            )
            await message.copy_to(chat_id=admin_id)

        # Сохраняем связь между message_id в чате админа и user_id
        admin_message_links.append((sent_message.message_id, user.id))

        # Отправляем подтверждение пользователю
        await message.answer(
            "✅📨 Ваше сообщение отправлено в службу поддержки!\n\n"
            "🏎 Мы ответим вам как можно скорее!"
        )

    except Exception as e:
        print(f"❌ Ошибка при обработке сообщения: {e}")

        # Уведомляем пользователя о проблеме
        try:
            await message.answer(
                "⚠️ К сожалению, произошла ошибка при отправке вашего сообщения.\n"
                "Пожалуйста, попробуйте ещё раз позже."
            )
        except:
            pass

        # Пытаемся уведомить админа об ошибке
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=f"⚠️ <b>Ошибка при получении сообщения от пользователя</b>\n\n"
                     f"🔗 Профиль: tg://user?id={user.id}\n"
                     f"{'🙋 Username: @' + user.username if user.username else ''}\n"
                     f"❌ Ошибка: {e}",
                parse_mode=ParseMode.HTML
            )
        except:
            pass


async def main():
    """Запуск бота"""
    print("🚀 Бот поддержки запущен и готов к работе!")
    print(f"📊 Хранилище сообщений: до {admin_message_links.maxlen} записей")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
