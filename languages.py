LANGUAGES = {
    'en': {
        'start': "Hello! Please select the category of your issue.",
        'category_prompt': "Please select the category of your issue.",
        'aml_subcategories': [['KYC'], ['Stop-List'], ['AML Requirements (Letter/Order)'], ['Other']],
        'sc_subcategories': [['Export/Import Contract'], ['Checklist'], ['SWIFT Screening'],
                             ['KFC (For Non-Residents)'], ['Sanctions Requirements (Letter/Order)']],
        'full_name_prompt': "Please enter your full name.",
        'contact_prompt': "Thank you! Now, please enter your contact number or press 'Share Contact'.",
        'description_prompt': "Great! Finally, please describe your issue.",
        'thanks': "Thank you! Your issue has been reported.",
        'cancel': "Operation cancelled. To start again, type /start.",
        'buttons': {
            'language': ['🇬🇧 English', '🇺🇿 O\'zbekcha', '🇷🇺 Русский'],
            'category': ['Anti-Money Laundering', 'Sanctions Compliance'],
            'contact': 'Share Contact'
        },
        'report_message': (
            "New Report:\n\n"
            "<b>Report ID:</b> {report_id}\n"
            "<b>Category:</b> {category}\n"
            "<b>Subcategory:</b> {subcategory}\n"
            "<b>Full Name:</b> {full_name}\n"
            "<b>Contact:</b> {contact}\n\n"
            "<b>Description:</b>\n<i>{description}</i>"
        )
    },
    'uz': {
        'start': "Salom! Muammo kategoriyasini tanlang.",
        'category_prompt': "Muammo kategoriyasini tanlang.",
        'aml_subcategories': [['KYC'], ['Stop-List'],
                              ['AML Talablar (Xat/Buyruq)'], ['Boshqa']],
        'sc_subcategories': [['Eksport/Import shartnoma'], ['Checklist'], ['SWIFT skrening'],
                             ['KYC (Norezidentlar uchun)'], ['Sanksiyalar Talablar (Xat/Buyruq)']],
        'full_name_prompt': "Iltimos, to'liq ismingizni kiriting.",
        'contact_prompt': "Rahmat! Endi, telefon raqamingizni kiriting.",
        'description_prompt': "Ajoyib! Oxirgi, muammongizni tavsiflang.",
        'thanks': "Rahmat! Sizning muammongiz xabar qilindi.",
        'cancel': "Operatsiya bekor qilindi. Qayta boshlash uchun, /start yozing.",
        'buttons': {
            'language': ['🇬🇧 English', '🇺🇿 O\'zbekcha', '🇷🇺 Русский'],
            'category': ['Anti-Money Laundering', 'Sanctions Compliance'],
            'contact': 'Kontaktni ulashish'
        },
        'report_message': (
            "Yangi Report:\n\n"
            "<b>Hisobot ID:</b> {report_id}\n"
            "<b>Kategoriya:</b> {category}\n"
            "<b>Subkategoriya:</b> {subcategory}\n"
            "<b>To'liq ismi:</b> {full_name}\n"
            "<b>Aloqa:</b> {contact}\n\n"
            "<b>Tavsif:</b>\n<i>{description}</i>"
        )
    },
    'ru': {
        'start': "Здравствуйте! Выберите категорию вашей проблемы.",
        'category_prompt': "Выберите категорию вашей проблемы.",
        'aml_subcategories': [['KYC'], ['Стоп-лист'], ['Требования по AML (Письмо/Приказ)'], ['Другой']],
        'sc_subcategories': [['Экспорт/Импорт контракт'], ['Чек-лист'], ['SWIFT скренинг'], ['KYC (Для нерезидентов)'],
                             ['Требования по санкциям (Письмо/Приказ)']],
        'full_name_prompt': "Пожалуйста, укажите ваше полное имя.",
        'contact_prompt': "Спасибо! Теперь укажите ваш контактный номер.",
        'description_prompt': "Отлично! Наконец, опишите вашу проблему.",
        'thanks': "Спасибо! Ваша проблема была сообщена.",
        'cancel': "Операция отменена. Чтобы начать заново, напишите /start.",
        'buttons': {
            'language': ['🇬🇧 English', '🇺🇿 O\'zbekcha', '🇷🇺 Русский'],
            'category': ['Anti-Money Laundering', 'Sanctions Compliance'],
            'contact': 'Поделиться контактом'
        },
        'report_message': (
            "Новый Репорт:\n\n"
            "<b>ID отчета:</b> {report_id}\n"
            "<b>Категория:</b> {category}\n"
            "<b>Подкатегория:</b> {subcategory}\n"
            "<b>Полное имя:</b> {full_name}\n"
            "<b>Контакт:</b> {contact}\n\n"
            "<b>Описание:</b>\n<i>{description}</i>"
        )
    }
}