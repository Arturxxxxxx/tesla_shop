import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler

# Токен и URL API
TOKEN = '7306256466:AAExI2px66yo-WbMwI_XvxCGd7lCufaDa7Y'
API_URL = 'http://104.197.92.255/products/product/'
CATEGORY_API_URL = 'http://104.197.92.255/products/categories/'

AUTHORIZED_USERS = [5901656337]

# Определение состояний
START, TITLE, PRICE, DESCRIPTION, ARTIKUL, YEAR, IN_STOCK, MARKA, MODEL, SPARE_PART_NUMBER, GENERATION, CATEGORY, PRODUCT_IMAGES, CATEGORY_NAME, CATEGORY_IMAGES, CONDITION = range(16)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    user = update.message.from_user
    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text('У вас нет доступа к этому боту.')
        return ConversationHandler.END
    
    await update.message.reply_text(f'Ваш ID пользователя: {user.id}')
    
    keyboard = [
        [InlineKeyboardButton("Создать продукт", callback_data='create_product')],
        [InlineKeyboardButton("Добавить категорию", callback_data='add_category')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
    return START

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    action = query.data
    if action == 'create_product':
        await query.message.reply_text('Привет! Давайте начнем создание нового продукта. Назовите продукт.')
        return TITLE
    elif action == 'add_category':
        await query.message.reply_text('Введите название новой категории:')
        return CATEGORY_NAME

async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['title'] = update.message.text
    await update.message.reply_text('Введите цену продукта:')
    return PRICE

async def receive_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['price'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Введите корректное значение для цены.')
        return PRICE
    await update.message.reply_text('Введите описание продукта:')
    return DESCRIPTION

async def receive_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['description'] = update.message.text
    await update.message.reply_text('Введите артикул продукта:')
    return ARTIKUL

async def receive_artikul(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['artikul'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Введите корректное значение для артикула.')
        return ARTIKUL
    await update.message.reply_text('Введите год выпуска:')
    return YEAR

async def receive_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        context.user_data['year'] = int(update.message.text)
    except ValueError:
        await update.message.reply_text('Введите корректное значение для года.')
        return YEAR
    
    keyboard = [
        [InlineKeyboardButton("Да", callback_data='yes')],
        [InlineKeyboardButton("Нет", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Продукт в наличии?', reply_markup=reply_markup)
    
    return IN_STOCK

async def handle_in_stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    in_stock = query.data
    context.user_data['in_stock'] = in_stock == 'yes'
    
    keyboard = [
        [InlineKeyboardButton("Новый", callback_data='new')],
        [InlineKeyboardButton("Б/У", callback_data='used')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Выберите состояние продукта:', reply_markup=reply_markup)
    return CONDITION

async def handle_condition(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    condition = query.data
    context.user_data['choice'] = 'Новый' if condition == 'new' else 'Б/У'
    await query.message.reply_text('Введите марку:')
    return MARKA

async def receive_marka(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['marka'] = update.message.text
    await update.message.reply_text('Введите модель:')
    return MODEL

async def receive_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['model'] = update.message.text
    await update.message.reply_text('Введите номер запасной части:')
    return SPARE_PART_NUMBER

async def receive_spare_part_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['spare_part_number'] = update.message.text
    await update.message.reply_text('Введите поколение:')
    return GENERATION

async def receive_generation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['generation'] = update.message.text
    
    try:
        response = requests.get(CATEGORY_API_URL)
        response.raise_for_status()
        categories = response.json()
    except requests.RequestException as e:
        await update.message.reply_text(f'Ошибка при получении категорий: {e}')
        return ConversationHandler.END
    
    keyboard = [[InlineKeyboardButton(cat['category'], callback_data=cat['id'])] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)
    return CATEGORY

async def receive_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    category_id = int(query.data)
    context.user_data['category'] = category_id
    await query.message.reply_text('Теперь отправьте изображения (до 4 изображений).')
    return PRODUCT_IMAGES

async def receive_product_images(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        
        try:
            file_url = file.file_path
            context.user_data.setdefault('image_urls', []).append(file_url)
        except Exception as e:
            await update.message.reply_text(f'Не удалось загрузить изображение: {e}')
            return PRODUCT_IMAGES

        if len(context.user_data['image_urls']) < 4:
            await update.message.reply_text(f'Загружено {len(context.user_data["image_urls"])} изображения. Загрузите следующее фото.')
            return PRODUCT_IMAGES
        else:
            await update.message.reply_text('Загружено 4 изображения. Завершаем.')

            product_data = {
                'title': context.user_data.get('title'),
                'price': context.user_data.get('price'),
                'description': context.user_data.get('description'),
                'artikul': context.user_data.get('artikul'),
                'year': context.user_data.get('year'),
                'in_stock': context.user_data.get('in_stock'),
                'marka': context.user_data.get('marka'),
                'model': context.user_data.get('model'),
                'spare_part_number': context.user_data.get('spare_part_number'),
                'generation': context.user_data.get('generation'),
                'choice': context.user_data.get('choice'),
                'category': context.user_data.get('category'),
            }

            files = {
                'image1': (f'Image1.jpg', requests.get(context.user_data['image_urls'][0]).content, 'image/jpeg'),
                'image2': (f'Image2.jpg', requests.get(context.user_data['image_urls'][1]).content, 'image/jpeg'),
                'image3': (f'Image3.jpg', requests.get(context.user_data['image_urls'][2]).content, 'image/jpeg'),
                'image4': (f'Image4.jpg', requests.get(context.user_data['image_urls'][3]).content, 'image/jpeg')
            }

            try:
                response = requests.post(API_URL, data=product_data, files=files)
                response.raise_for_status()
                await update.message.reply_text('Продукт успешно создан!')
            except requests.RequestException as e:
                await update.message.reply_text(f'Произошла ошибка при создании продукта: {e}\nОтвет сервера: {response.text}')
                    
            return ConversationHandler.END
    else:
        await update.message.reply_text('Пожалуйста, отправьте изображение.')
        return PRODUCT_IMAGES

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [CallbackQueryHandler(handle_choice)],
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_price)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_description)],
            ARTIKUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_artikul)],
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_year)],
            IN_STOCK: [CallbackQueryHandler(handle_in_stock)],
            CONDITION: [CallbackQueryHandler(handle_condition)],
            MARKA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_marka)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_model)],
            SPARE_PART_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_spare_part_number)],
            GENERATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_generation)],
            CATEGORY: [CallbackQueryHandler(receive_category)],
            PRODUCT_IMAGES: [MessageHandler(filters.PHOTO, receive_product_images)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
