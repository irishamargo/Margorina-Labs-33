from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler, ContextTypes
from datetime import datetime, timedelta
import asyncio

# Определяем состояния
SELECT_SERVICE, SELECT_MASTER, SELECT_DAY, SELECT_TIME = range(4)

# Данные
SERVICES = {
    "haircut": {
        "name": "Стрижка",
        "masters": ["Анна (опыт 5 лет)", "Иван (стилист)", "Мария (детский мастер)"]
    },
    "manicure": {
        "name": "Маникюр",
        "masters": ["Ольга (гель-лак)", "Екатерина (аппаратный)", "Светлана (европейский)"]
    },
    "massage": {
        "name": "Массаж",
        "masters": ["Алексей (спортивный)", "Дарья (релакс)", "Михаил (лечебный)"]
    }
}

#Выбор услуги
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    keyboard = [
        [InlineKeyboardButton("Стрижка", callback_data="service_haircut")],
        [InlineKeyboardButton("Маникюр", callback_data="service_manicure")],
        [InlineKeyboardButton("Массаж", callback_data="service_massage")],
    ]

    await update.message.reply_text(
        "Добро пожаловать в салон красоты!\nВыберите услугу:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SELECT_SERVICE

#Обработка выбора услуги и переход к выбору мастера
async def select_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Извлекаем тип услуги из callback_data
    service_type = query.data.replace("service_", "")

    if service_type not in SERVICES:
        await query.edit_message_text("Ошибка: услуга не найдена")
        return ConversationHandler.END

    service = SERVICES[service_type]

    # Сохраняем выбранную услугу
    context.user_data['service'] = {
        'type': service_type,
        'name': service['name']
    }

    # Создаем кнопки для выбора мастера
    keyboard = []
    for idx, master in enumerate(service['masters']):
        keyboard.append([InlineKeyboardButton(master, callback_data=f"master_{idx}")])

    # Кнопка возврата к выбору услуги
    keyboard.append([InlineKeyboardButton("Назад к выбору услуги", callback_data="back_to_service")])

    await query.edit_message_text(
        f"Выбрана услуга: <b>{service['name']}</b>\n\nВыберите мастера:",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return SELECT_MASTER

# Выбор мастера и переход к выбору дня
async def select_master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Обработка кнопки "Назад к выбору услуги"
    if query.data == "back_to_service":
        keyboard = [
            [InlineKeyboardButton("Стрижка", callback_data="service_haircut")],
            [InlineKeyboardButton("Маникюр", callback_data="service_manicure")],
            [InlineKeyboardButton("Массаж", callback_data="service_massage")],
        ]

        await query.edit_message_text(
            "Выберите услугу:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return SELECT_SERVICE

    # Обработка выбора мастера
    if query.data.startswith("master_"):
        try:
            # Извлекаем индекс мастера
            master_idx = int(query.data.split("_")[1])

            # Проверяем, есть ли данные об услуге
            if 'service' not in context.user_data:
                await query.edit_message_text("Ошибка: данные об услуге утеряны")
                return ConversationHandler.END

            service_type = context.user_data['service']['type']
            masters = SERVICES[service_type]['masters']

            # Проверяем корректность индекса
            if master_idx < 0 or master_idx >= len(masters):
                await query.edit_message_text("Ошибка: неверный индекс мастера")
                return ConversationHandler.END

            selected_master = masters[master_idx]
            context.user_data['master'] = selected_master

            # Генерируем дни для выбора
            today = datetime.now()
            keyboard = []

            for day_offset in range(1, 8):  # Следующие 7 дней
                current_date = today + timedelta(days=day_offset)
                date_str = current_date.strftime("%d.%m.%Y")

                weekdays_ru = {
                    "Monday": "Понедельник",
                    "Tuesday": "Вторник",
                    "Wednesday": "Среда",
                    "Thursday": "Четверг",
                    "Friday": "Пятница",
                    "Saturday": "Суббота",
                    "Sunday": "Воскресенье"
                }

                weekday_en = current_date.strftime("%A")
                weekday_ru = weekdays_ru.get(weekday_en, weekday_en)

                keyboard.append([
                    InlineKeyboardButton(
                        f"{weekday_ru}, {date_str}",
                        callback_data=f"day_{current_date.strftime('%Y-%m-%d')}"
                    )
                ])

            # Кнопка возврата к выбору мастера
            keyboard.append([InlineKeyboardButton("Выбрать другого мастера", callback_data="back_to_master")])

            await query.edit_message_text(
                f"Услуга: <b>{context.user_data['service']['name']}</b>\n"
                f"Мастер: <b>{selected_master}</b>\n\n"
                "Выберите день:",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

            return SELECT_DAY

        except (ValueError, IndexError, KeyError) as e:
            await query.edit_message_text(
                "Произошла ошибка при выборе мастера\n"
                "Пожалуйста, начните заново с /start"
            )
            return ConversationHandler.END

    await query.edit_message_text("Неизвестная команда")
    return ConversationHandler.END

#Выбор дня и переход к выбору времени
async def select_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Обработка кнопки "Выбрать другого мастера"
    if query.data == "back_to_master":
        # Возврат к выбору мастера
        service_type = context.user_data['service']['type']
        service = SERVICES[service_type]

        keyboard = []
        for idx, master in enumerate(service['masters']):
            keyboard.append([InlineKeyboardButton(master, callback_data=f"master_{idx}")])

        # Кнопка возврата к выбору услуги
        keyboard.append([InlineKeyboardButton("Назад к выбору услуги", callback_data="back_to_service")])

        await query.edit_message_text(
            f"Выберите мастера для услуги {service['name']}:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return SELECT_MASTER

    # Обработка выбора дня
    if query.data.startswith("day_"):
        # Сохраняем выбранный день
        date_str = query.data.replace("day_", "")
        context.user_data['selected_day'] = date_str

        # Форматируем для отображения
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            context.user_data['selected_day_display'] = date_obj.strftime("%d.%m.%Y")
        except ValueError:
            await query.edit_message_text("Ошибка формата даты")
            return ConversationHandler.END

        # Генерируем временные слоты (каждые 2 часа с 10:00 до 18:00)
        time_slots = []
        for hour in range(10, 20, 2):
            time_slots.append(f"{hour:02d}:00")

        # Создаем кнопки времени
        keyboard = []
        row = []
        for i, time_slot in enumerate(time_slots):
            row.append(InlineKeyboardButton(time_slot, callback_data=f"time_{time_slot}"))
            if len(row) == 3 or i == len(time_slots) - 1:
                keyboard.append(row)
                row = []

        # Кнопка возврата к выбору дня
        keyboard.append([InlineKeyboardButton("Выбрать другой день", callback_data="back_to_day")])

        await query.edit_message_text(
            f"Услуга: <b>{context.user_data['service']['name']}</b>\n"
            f"Мастер: <b>{context.user_data['master']}</b>\n"
            f"День: <b>{context.user_data['selected_day_display']}</b>\n\n"
            "Выберите время:",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return SELECT_TIME

    await query.edit_message_text("Неизвестная команда")
    return ConversationHandler.END

#Выбор времени и завершение записи
async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Обработка кнопки "Выбрать другой день"
    if query.data == "back_to_day":
        # Возврат к выбору дня
        today = datetime.now()
        keyboard = []

        for day_offset in range(1, 8):
            current_date = today + timedelta(days=day_offset)
            date_str = current_date.strftime("%d.%m.%Y")

            weekdays_ru = {
                "Monday": "Понедельник",
                "Tuesday": "Вторник",
                "Wednesday": "Среда",
                "Thursday": "Четверг",
                "Friday": "Пятница",
                "Saturday": "Суббота",
                "Sunday": "Воскресенье"
            }

            weekday_en = current_date.strftime("%A")
            weekday_ru = weekdays_ru.get(weekday_en, weekday_en)

            keyboard.append([
                InlineKeyboardButton(
                    f"{weekday_ru}, {date_str}",
                    callback_data=f"day_{current_date.strftime('%Y-%m-%d')}"
                )
            ])

        # Кнопка возврата к выбору мастера
        keyboard.append([InlineKeyboardButton("Выбрать другого мастера", callback_data="back_to_master")])

        await query.edit_message_text(
            f"Услуга: <b>{context.user_data['service']['name']}</b>\n"
            f"Мастер: <b>{context.user_data['master']}</b>\n\n"
            "Выберите день:",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return SELECT_DAY

    # Обработка выбора времени
    if query.data.startswith("time_"):
        selected_time = query.data.replace("time_", "")
        context.user_data['selected_time'] = selected_time

        # Формируем итоговое сообщение
        summary = (
            "<b>Запись успешно оформлена!</b>\n\n"
            f"Услуга: {context.user_data['service']['name']}\n"
            f"Мастер: {context.user_data['master']}\n"
            f"Дата: {context.user_data['selected_day_display']}\n"
            f"Время: {selected_time}\n\n"
            "Ждем вас в салоне!"
        )

        await query.edit_message_text(summary, parse_mode='HTML')

        # Логируем запись
        print("НОВАЯ ЗАПИСЬ:")
        print(f"  Услуга: {context.user_data['service']['name']}")
        print(f"  Мастер: {context.user_data['master']}")
        print(f"  Дата: {context.user_data['selected_day_display']}")
        print(f"  Время: {selected_time}")
        print(f"  Пользователь: {query.from_user.full_name}")

        return ConversationHandler.END

    await query.edit_message_text("Неизвестная команда")
    return ConversationHandler.END

def main():
    # Запуск бота
    TOKEN = "8505727530:AAGXfjTIbL7nZ6ckSTX4RcPD_c_r2L_TYqQ"

    # Правильное создание Application с использованием create
    application = Application.builder().token(TOKEN).build()

    # Создаем ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_SERVICE: [
                CallbackQueryHandler(select_service, pattern='^service_')
            ],
            SELECT_MASTER: [
                CallbackQueryHandler(select_master)
            ],
            SELECT_DAY: [
                CallbackQueryHandler(select_day)
            ],
            SELECT_TIME: [
                CallbackQueryHandler(select_time)
            ],
        },
        fallbacks=[],
    )

    # Регистрируем обработчик
    application.add_handler(conv_handler)

    print("="*50)
    print("Бот запущен!")
    print("Для остановки нажмите Ctrl+C")
    print("="*50)

    # Запускаем бота с правильной обработкой
    application.run_polling()

if __name__ == '__main__':
    main()
