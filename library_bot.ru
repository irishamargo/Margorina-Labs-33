import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8253815167:AAGDY_If-K723N1PK5j9n4h5p-kyouwXYwA"

# База данных книг
BOOKS_DATABASE = {
    "Фантастика": [
        {"title": "Дюна", "author": "Фрэнк Герберт", "year": 1965,
         "description": "Эпическая сага о далеком будущем. Планета Арракис, известная как Дюна, — единственный источник ценной пряности."},
        {"title": "Пикник на обочине", "author": "Братья Стругацкие", "year": 1972,
         "description": "Зона — опасная территория с аномалиями. Сталкеры рискуют жизнью, чтобы добыть артефакты."},
    ],
    "Детектив": [
        {"title": "Убийство в Восточном экспрессе", "author": "Агата Кристи", "year": 1934,
         "description": "Знаменитый детектив Эркюль Пуаро расследует убийство в поезде, застрявшем в снегу."},
        {"title": "Шерлок Холмс: Этюд в багровых тонах", "author": "Артур Конан Дойл", "year": 1887,
         "description": "Первая повесть о великом сыщике Шерлоке Холмсе и его друге докторе Ватсоне."},
    ],
    "Роман": [
        {"title": "Война и мир", "author": "Лев Толстой", "year": 1869,
         "description": "Роман-эпопея, описывающий русское общество в эпоху войн против Наполеона."},
        {"title": "Гордость и предубеждение", "author": "Джейн Остин", "year": 1813,
         "description": "История о любви и социальных предрассудках в Англии начала XIX века."},
    ],
    "Фэнтези": [
        {"title": "Властелин колец", "author": "Дж. Р. Р. Толкин", "year": 1954,
         "description": "Эпопея о Средиземье, где хоббит Фродо должен уничтожить Кольцо Всевластья."},
        {"title": "Гарри Поттер и философский камень", "author": "Дж. К. Роулинг", "year": 1997,
         "description": "Первая книга о юном волшебнике Гарри Поттере и его обучении в Хогвартсе."},
    ]
}

# ==================== КОМАНДЫ БОТА ====================

"""Обработчик команды /start"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    welcome_text = (
        f"📚 *Добро пожаловать в Электронную Библиотеку!*\n\n"
        "Выберите жанр книг:"
    )

    # Создаем reply-кнопки с жанрами
    keyboard = [
        ['📖 Фантастика', '🔍 Детектив'],
        ['💖 Роман', '🐉 Фэнтези']
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите жанр..."
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

"""Обработка выбора жанра из reply-кнопок"""
async def handle_genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    # Определяем жанр по кнопке
    genre_mapping = {
        '📖 Фантастика': 'Фантастика',
        '🔍 Детектив': 'Детектив',
        '💖 Роман': 'Роман',
        '🐉 Фэнтези': 'Фэнтези'
    }

    selected = genre_mapping.get(text)

    if selected in BOOKS_DATABASE:
        books = BOOKS_DATABASE[selected]

        # Создаем inline-кнопки для книг
        keyboard = []
        for i, book in enumerate(books):
            keyboard.append([
                InlineKeyboardButton(
                    f"{book['title']}",
                    callback_data=f"book_{selected}_{i}"
                )
            ])

        # Добавляем кнопку назад
        keyboard.append([
            InlineKeyboardButton("🔙 Назад к выбору жанра", callback_data="back_to_genres")
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"*📚 Книги в жанре '{selected}':*\n\n"
            f"Выберите книгу:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

"""Обработка нажатий на inline-кнопки с книгами"""
async def handle_book_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Убираем "часики"

    data = query.data

    # Обработка навигации
    if data == "back_to_genres":
        await show_genres_menu(query)
        return

    # Обработка выбора книги
    elif data.startswith("book_"):
        parts = data.split("_")
        if len(parts) >= 3:
            genre = parts[1]
            book_index = int(parts[2])

            if genre in BOOKS_DATABASE and 0 <= book_index < len(BOOKS_DATABASE[genre]):
                book = BOOKS_DATABASE[genre][book_index]
                await show_book_info(query, book, genre)

"""Показать информацию о книге"""
async def show_book_info(query, book, genre):
    # Создаем кнопку назад
    keyboard = [[
        InlineKeyboardButton("🔙 Назад к списку книг", callback_data=f"back_to_{genre}")
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    book_info = (
        f"*📖 {book['title']}*\n\n"
        f"*Автор:* {book['author']}\n"
        f"*Год издания:* {book['year']}\n"
        f"*Жанр:* {genre}\n\n"
        f"*Описание:*\n{book['description']}"
    )

    await query.edit_message_text(
        book_info,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

"""Показать меню с жанрами"""
async def show_genres_menu(query):
    keyboard = [
        ['📖 Фантастика', '🔍 Детектив'],
        ['💖 Роман', '🐉 Фэнтези']
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите жанр..."
    )

    await query.message.reply_text(
        "*📚 Выберите жанр книг:*",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

"""Обработка кнопки назад к списку книг"""
async def handle_back_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("back_to_"):
        # Извлекаем название жанра, например, "Фантастика"
        genre = data.replace("back_to_", "")

        # Важно: проверяем, что такой жанр существует
        if genre in BOOKS_DATABASE:
            await show_genre_books(query, genre)
        else:
            # Если жанр не найден (например, была ошибка в данных), сообщаем пользователю
            await query.answer(f"Жанр '{genre}' не найден.", show_alert=True)

"""Обработка кнопки 'Назад к выбору жанра' (back_to_genres)"""
async def handle_back_to_genres(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Убираем "часики" на кнопке
    await show_genres_menu(query)  # Показываем меню с reply-кнопками жанров

"""Показать книги выбранного жанра"""
async def show_genre_books(query, genre):
    books = BOOKS_DATABASE[genre]

    keyboard = []
    for i, book in enumerate(books):
        keyboard.append([
            InlineKeyboardButton(
                f"{book['title']}",
                callback_data=f"book_{genre}_{i}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton("🔙 Назад к выбору жанра", callback_data="back_to_genres")
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"*📚 Книги в жанре '{genre}':*\n\n"
        f"Выберите книгу:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ==================== ОСНОВНАЯ ФУНКЦИЯ ====================

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик выбора жанра из reply-кнопок
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND &
        filters.Regex(r'^(📖 Фантастика|🔍 Детектив|💖 Роман|🐉 Фэнтези)$'),
        handle_genre_selection
    ))

    # Обработчик нажатий на inline-кнопки
    application.add_handler(CallbackQueryHandler(handle_back_to_genres, pattern="^back_to_genres$"))
    application.add_handler(CallbackQueryHandler(handle_back_button, pattern="^back_to_"))
    application.add_handler(CallbackQueryHandler(handle_book_selection, pattern="^book_"))

    # Запускаем бота
    print("🤖 Бот электронной библиотеки запускается...")
    print("📚 Откройте Telegram и найдите вашего бота")
    print("🛑 Нажмите Ctrl+C для остановки")

    application.run_polling()

# Точка входа
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
