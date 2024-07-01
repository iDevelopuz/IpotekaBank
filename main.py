import logging
import random
from enum import Enum
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, \
    ConversationHandler
from languages import LANGUAGES

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define states for conversation
class States(Enum):
    LANGUAGE = 1
    CATEGORY = 2
    SUBCATEGORY = 3
    FULL_NAME = 4
    CONTACT = 5
    DESCRIPTION = 6


# Used report IDs
used_ids = set()

TOKEN = "7156917810:AAEuN7cVpC8KntEejvI9vdBRAr8VNGqBQ2s"
AML_REQUIREMENTS_GROUP_ID = "-1002144716474"
SANCTIONS_COMPLIANCE_GROUP_ID = "-4275826655"


async def start(update: Update, context: CallbackContext) -> States:
    try:
        reply_keyboard = [
            [KeyboardButton(text='🇬🇧 English')],
            [KeyboardButton(text='🇺🇿 O\'zbekcha')],
            [KeyboardButton(text='🇷🇺 Русский')]
        ]
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
                                           input_field_placeholder="Choose language")

        await update.message.reply_text(
            "Please, choose your language: \n"
            "Iltimos, tilingizni tanlang: \n"
            "Пожалуйста, выберите свой язык: \n",
            reply_markup=reply_markup
        )
        return States.LANGUAGE
    except Exception as e:
        logger.error(f"Error in start: {e}")
        await update.message.reply_text("An error occurred. Please try again.")
        return States.LANGUAGE


# Define handler to set language and proceed with the conversation
async def set_language(update: Update, context: CallbackContext) -> States:
    language_choice = update.message.text
    if language_choice == '🇬🇧 English':
        context.user_data['language'] = 'en'
    elif language_choice == '🇺🇿 O\'zbekcha':
        context.user_data['language'] = 'uz'
    elif language_choice == '🇷🇺 Русский':
        context.user_data['language'] = 'ru'
    else:
        await update.message.reply_text("Invalid input. Try again.")
        return States.LANGUAGE
    lang = LANGUAGES[context.user_data['language']]
    reply_keyboard = [[KeyboardButton(text) for text in lang['buttons']['category']]]
    await update.message.reply_text(
        lang['start'],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
                                         input_field_placeholder='Category')
    )
    return States.CATEGORY


async def category(update: Update, context: CallbackContext) -> States:
    lang = LANGUAGES[context.user_data['language']]
    category_choice = update.message.text
    context.user_data['category'] = category_choice
    valid_categories = lang['buttons']['category']
    if category_choice in valid_categories:
        # Map the chosen category to a common internal value
        if category_choice in lang['buttons']['category']:
            if category_choice == lang['buttons']['category'][0]:
                context.user_data['category_internal'] = 'Anti-Money Laundering'
                reply_keyboard = [[KeyboardButton(text) for text in sub] for sub in lang['aml_subcategories']]
            else:
                context.user_data['category_internal'] = 'Sanctions Compliance'
                reply_keyboard = [[KeyboardButton(text) for text in sub] for sub in lang['sc_subcategories']]

            await update.message.reply_text(
                lang['category_prompt'],
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
                                                 input_field_placeholder='Subcategory')
            )
            return States.SUBCATEGORY
    else:
        await update.message.reply_text('Invalid data. Try again.')  # Specific error message
        return States.CATEGORY


async def subcategory(update: Update, context: CallbackContext) -> States:
    lang = LANGUAGES[context.user_data['language']]
    subcategory_choice = update.message.text
    # Fetching valid subcategories based on the chosen category
    valid_subcategories = []
    if context.user_data['category'] == lang['buttons']['category'][0]:
        valid_subcategories = lang['aml_subcategories']
    elif context.user_data['category'] == lang['buttons']['category'][1]:
        valid_subcategories = lang['sc_subcategories']
    if any(subcategory_choice in sub for sub in valid_subcategories):
        context.user_data['subcategory'] = subcategory_choice
        await update.message.reply_text(
            lang['full_name_prompt'],
            reply_markup=ForceReply(selective=True, input_field_placeholder='Full Name')
        )
        return States.FULL_NAME
    else:
        await update.message.reply_text('Invalid input. Try again.')
        return States.SUBCATEGORY


async def full_name(update: Update, context: CallbackContext) -> States:
    full_name_len = update.message.text
    if 2 <= len(full_name_len) <= 50:  # Example validation: name must be 2-50 characters
        context.user_data['full_name'] = full_name
        context.user_data['full_name'] = update.message.text
        lang = LANGUAGES[context.user_data['language']]
        contact_button = KeyboardButton(lang['buttons']['contact'], request_contact=True)
        await update.message.reply_text(
            lang['contact_prompt'],
            reply_markup=ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True,
                                             input_field_placeholder='Contact')
        )
        return States.CONTACT
    else:
        await update.message.reply_text('Invalid Name. Try again.')
        return States.FULL_NAME


async def contact(update: Update, context: CallbackContext) -> States:
    if update.message.contact:
        context.user_data['contact'] = update.message.contact.phone_number
        lang = LANGUAGES[context.user_data['language']]
        await update.message.reply_text(
            lang['description_prompt'],
            reply_markup=ReplyKeyboardRemove()  # Remove keyboard after contact is received
        )
        return States.DESCRIPTION
    else:
        await update.message.reply_text(
            'Invalid data. Try again.'
        )
        return States.CONTACT


async def description(update: Update, context: CallbackContext) -> int | States:
    description_len = update.message.text
    if 10 <= len(description_len) <= 500:
        context.user_data['description'] = update.message.text
        lang = LANGUAGES[context.user_data['language']]
        report_id = generate_unique_id()
        group_id = None

        category_topic = context.user_data['category_internal']
        subcategory_title = context.user_data['subcategory']

        # Checking the internal category value
        if category_topic == 'Anti-Money Laundering':
            if subcategory_title in ['KYC', 'Stop-List', 'AML Requirements (Letter/Order)', 'Other',
                                     'AML Talablar (Xat/Buyruq)', 'Boshqa', 'Стоп-лист', 'Другой',
                                     'Требования по AML (Письмо/Приказ)']:
                group_id = AML_REQUIREMENTS_GROUP_ID
        else:
            if subcategory_title in ['Export/Import Contract', 'Checklist', 'SWIFT Screening',
                                     'KFC (For Non-Residents)', 'Sanctions Requirements (Letter/Order)',
                                     'Eksport/Import shartnoma', 'SWIFT skrening',
                                     'KYC (Norezidentlar uchun)', 'Sanksiyalar Talablar (Xat/Buyruq)',
                                     'Экспорт/Импорт контракт', 'Чек-лист', 'SWIFT скренинг',
                                     'KYC (Для нерезидентов)',
                                     'Требования по санкциям (Письмо/Приказ)'
                                     ]:
                group_id = SANCTIONS_COMPLIANCE_GROUP_ID

        if group_id:
            user_data = context.user_data
            message = lang['report_message'].format(
                report_id=report_id,
                category=user_data['category'],
                subcategory=user_data['subcategory'],
                full_name=user_data['full_name'],
                contact=user_data['contact'],
                description=user_data['description']
            )
            await context.bot.send_message(chat_id=group_id, text=message, parse_mode='HTML')
            reply_keyboard = [[KeyboardButton('/start')]]
            await update.message.reply_text(
                lang['thanks'],
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True,
                                                 input_field_placeholder='Description')
            )
        else:
            await update.message.reply_text(
                "Error: Invalid category or subcategory. Please try again.",
                reply_markup=ReplyKeyboardMarkup([[KeyboardButton('/start')]], one_time_keyboard=True)
            )
        return ConversationHandler.END
    else:
        await update.message.reply_text('No less than 10 characters. Try again.')
        return States.DESCRIPTION


def generate_unique_id() -> int:
    global used_ids
    while True:
        new_id = random.randint(10000, 99999)
        if new_id not in used_ids:
            used_ids.add(new_id)
            return new_id


async def cancel(update: Update, context: CallbackContext) -> int:
    try:
        lang = LANGUAGES[context.user_data['language']]
        await update.message.reply_text(
            lang['cancel']
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Error in set_language: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        return ConversationHandler.END


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)],
            States.CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            States.SUBCATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, subcategory)],
            States.FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, full_name)],
            States.CONTACT: [MessageHandler(filters.CONTACT, contact),
                             MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
            States.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
