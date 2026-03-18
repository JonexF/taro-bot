import asyncio
import os
import random

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ==============================
# ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ==============================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не найдена")

if not ADMIN_ID:
    raise ValueError("Переменная окружения ADMIN_ID не найдена")

ADMIN_ID = int(ADMIN_ID)

# ==============================
# ССЫЛКИ
# ==============================
COURSE_LINK = "https://yookassa.ru/my/i/abexX5Cytb8c/l"
CHANNEL_LINK = "https://t.me/+T1jWi1N41_UyYTIy"
CHANNEL_ID = -1003693758070  # пока не используется, можно оставить

# ==============================
# БАЗА КАРТ ПО ТЕМАМ
# ==============================
cards_by_theme = {
    "love": [
        {
            "name": "Паж Жезлов",
            "text": "В ближайшее время тебя ждет новое знакомство или сообщение, лёгкий флирт, инициатива и интерес со стороны кого-то молодого или спонтанного.",
            "image": "cards/love/1.jpg"
        },
        {
            "name": "3 Мечей",
            "text": "В ближайшее время тебя ждет боль, разочарование или откровенное предательство; нужно это пережить, чтобы двигаться дальше к счастливой жизни.",
            "image": "cards/love/2.jpg"
        },
        {
            "name": "4 Жезлов",
            "text": "В ближайшее время тебя ждёт стабильный и радостный этап, повод для праздника в отношениях, укрепление связи или примирение.",
            "image": "cards/love/3.jpg"
        },
        {
            "name": "Влюбленные",
            "text": "В ближайшее время вас ждёт значимый эмоциональный поворот: либо укрепление искренних отношений, либо необходимость сделать осознанный выбор. Результат зависит от честности с собой и готовности нести ответственность за решение.",
            "image": "cards/love/4.jpg"
        },
        {
            "name": "Мир",
            "text": "В ближайшее время тебя ждёт завершение цикла, приход чувства целостности; либо гармоничное достижение цели в отношениях, либо окончательное закрытие главы.",
            "image": "cards/love/5.jpg"
        },
        {
            "name": "6 Мечей",
            "text": "В ближайшее время тебя ждёт постепенный уход от проблем, переход к более спокойному периоду, возможно переосмысление или физический переезд.",
            "image": "cards/love/6.jpg"
        },
        {
            "name": "6 Кубков",
            "text": "В ближайшее время тебя ждёт всплеск ностальгии, возврат прошлых чувств или встречи с кем-то из прошлого; тёплые воспоминания влияют на выбор.",
            "image": "cards/love/7.jpg"
        },
        {
            "name": "Паж Кубков",
            "text": "В ближайшее время тебя ждёт нежное предложение, искренние чувства, флирт с романтическим подтекстом или эмоциональная открытость.",
            "image": "cards/love/8.jpg"
        },
        {
            "name": "Рыцарь Жезлов",
            "text": "В ближайшее время тебя ждут страстные, быстрые действия; вероятна импульсивность, стремление к приключению и сильное влечение.",
            "image": "cards/love/9.jpg"
        },
        {
            "name": "Шут",
            "text": "В ближайшее время тебя ждёт новый рискованный старт, спонтанность и свобода; начало без гарантий, но с потенциалом для открытия нового пути в любви.",
            "image": "cards/love/10.jpg"
        }
    ],
    "career": [
        {
            "name": "2 Мечей",
            "text": "Какое-то важное решение висит в воздухе; сейчас ты можешь оттягивать выбор или игнорировать конфликт. Нужно убрать сомнения и получить недостающую информацию прежде чем двигаться дальше.",
            "image": "cards/career/1.jpg"
        },
        {
            "name": "Туз Жезлов",
            "text": "В ближайшее время тебя ждёт новый проект, инициатива или возможность проявить себя. Появится заряд энергии и шанс начать что-то перспективное; используй вдохновение сразу.",
            "image": "cards/career/2.jpg"
        },
        {
            "name": "Королева Жезлов",
            "text": "В ближайшее время ты или кто-то рядом проявит харизму, уверенность и лидерство. Поддержка, способность вести за собой команду и привлекать внимание начальства.",
            "image": "cards/career/3.jpg"
        },
        {
            "name": "3 Пентаклей",
            "text": "В ближайшее время тебя ждёт признание профессионализма через сотрудничество; командная работа и хорошие результаты на практике. Возможность показать мастерство и получить повышение статуса.",
            "image": "cards/career/4.jpg"
        },
        {
            "name": "Император",
            "text": "Эта карта говорит о структуре, власти и стабильности. Появится сильный руководитель или ты войдёшь в более упорядоченную роль с ясными обязанностями и ответственностью.",
            "image": "cards/career/5.jpg"
        },
        {
            "name": "Мир",
            "text": "В ближайшее время тебя ждёт завершение цикла, достижение значимой цели и чувство завершённости. Успех проекта и признание на более широком уровне; возможен карьерный переход по кругу заслуг.",
            "image": "cards/career/6.jpg"
        },
        {
            "name": "Колесница",
            "text": "В ближайшее время тебя ждёт движение вперёд через волю и дисциплину; преодоление препятствий и активный карьерный рывок. Потребуется целеустремлённость и контроль эмоций.",
            "image": "cards/career/7.jpg"
        },
        {
            "name": "9 Мечей",
            "text": "В ближайшее время у тебя может быть беспокойство, бессонные ночи из-за рабочих страхов или перегрузки. Следи за выгоранием и не позволяй тревоге саботировать результат.",
            "image": "cards/career/8.jpg"
        },
        {
            "name": "7 Мечей",
            "text": "В ближайшее время важна осторожность с коллегами или с методами достижения целей; также возможны скрытые интриги или соблазн пойти нечестным путём. Действуй прозрачно и защищай свою репутацию.",
            "image": "cards/career/9.jpg"
        },
        {
            "name": "8 Кубков",
            "text": "В ближайшее время тебя ждёт уход от того, что больше не даёт роста; возможно, ты оставишь проект или среду, которая не соответствует ценностям. Это шаг к поиску более осознанной карьеры.",
            "image": "cards/career/10.jpg"
        }
    ],
    "finance": [
        {
            "name": "9 Пентаклей",
            "text": "Тебя ждет устойчивый доход и финансовая независимость; комфорт от результатов собственных усилий, возможность откладывать и пользоваться плодами труда.",
            "image": "cards/finance/1.jpg"
        },
        {
            "name": "Мир",
            "text": "В ближайшее время тебя ждёт завершение финансового цикла или долгого проекта с получением вознаграждения; крупное погашение долга, закрытие обязательств или признание твоей платежеспособности.",
            "image": "cards/finance/2.jpg"
        },
        {
            "name": "5 Жезлов",
            "text": "В ближайшее время тебя ждёт конкуренция за ресурсы или споры по деньгам; возможны разногласия в коллективных расходах или борьба за премию и лучшие условия.",
            "image": "cards/finance/3.jpg"
        },
        {
            "name": "9 Жезлов",
            "text": "Тебя ждет осторожность в тратах после прошлых потерь; необходимость защищать накопления, держать под контролем бюджет несмотря на усталость.",
            "image": "cards/finance/4.jpg"
        },
        {
            "name": "7 Пентаклей",
            "text": "В ближайшее время тебя ждёт период оценки инвестиций и доходов; терпеливое ожидание отдачи, решение продолжать вкладывать или перенаправить средства.",
            "image": "cards/finance/5.jpg"
        },
        {
            "name": "Колесница",
            "text": "В ближайшее время тебя ждёт ускорение финансовых процессов; получение дохода через активные действия, поездки, сделки или решительные шаги по улучшению денежного положения.",
            "image": "cards/finance/6.jpg"
        },
        {
            "name": "Королева Пентаклей",
            "text": "Тебя ждёт разумное управление ресурсами и забота о стабильности; улучшение бытовых и финансовых условий благодаря практичным решениям и планированию.",
            "image": "cards/finance/7.jpg"
        },
        {
            "name": "7 Мечей",
            "text": "В ближайшее время есть риск обмана или скрытых потерь; следи за прозрачностью договоренностей, документооборотом и не доверяй сомнительным схемам.",
            "image": "cards/finance/8.jpg"
        },
        {
            "name": "8 Жезлов",
            "text": "В ближайшее время тебя ждут быстрые поступления или внезапные финансовые новости; ускорение выплат, контрактов или поступление предложений, требующих оперативной реакции.",
            "image": "cards/finance/9.jpg"
        },
        {
            "name": "Справедливость",
            "text": "В ближайшее время тебя ждут официальные расчеты, возвраты или корректные решения по долгам и договорам; честные оценки и возможное восстановление баланса, если документы в порядке.",
            "image": "cards/finance/10.jpg"
        }
    ],
    "advice": [
        {
            "name": "Мир",
            "text": "Завязывай проекты и отпускай то, что исчерпало себя; завершение цикла принесёт ясность и пространство для нового. Подпиши документы и закрой старые дела, чтобы не тянуть за собой лишнее.",
            "image": "cards/advice/1.jpg"
        },
        {
            "name": "Звезда",
            "text": "Действуй с надеждой и доверяй интуиции; восстанавливай ресурсы и планируй долгосрочно. Делай мелкие шаги к целям, это укрепит веру в успех.",
            "image": "cards/advice/2.jpg"
        },
        {
            "name": "2 Жезлов",
            "text": "Решайся на выбор и строй планы; оцени варианты и выбери направление перед активными действиями. Подготовься к расширению, но не бросайся сразу в риск.",
            "image": "cards/advice/3.jpg"
        },
        {
            "name": "Дьявол",
            "text": "Избегай привязанностей и соблазнов материального; не пускайся в долговые или зависимые схемы. Проверь, не держишь ли себя в ловушке привычек, которые подрывают свободу.",
            "image": "cards/advice/4.jpg"
        },
        {
            "name": "Рыцарь Пентаклей",
            "text": "Будь методичен и терпелив; соблюдай дисциплину, следи за деталями и выполняй план шаг за шагом. Надёжность сейчас важнее спешки.",
            "image": "cards/advice/5.jpg"
        },
        {
            "name": "7 Жезлов",
            "text": "Защищай свои позиции и отстаивай границы; не сдавайся при встрече с сопротивлением. Чётко формулируй условия и не позволяй давить на себя.",
            "image": "cards/advice/6.jpg"
        },
        {
            "name": "4 Кубков",
            "text": "Не игнорируй предложения, но и не принимай решения в апатии; сделай паузу для переоценки мотивации. Возможно, нужно немного отдохнуть, чтобы увидеть реальные возможности.",
            "image": "cards/advice/7.jpg"
        },
        {
            "name": "Король Жезлов",
            "text": "Действуй решительно и лидерски; проявляй инициативу, вдохновляй окружающих и веди за собой, если цель ясна. Береги энергию и используй харизму для привлечения поддержки.",
            "image": "cards/advice/8.jpg"
        },
        {
            "name": "3 Кубков",
            "text": "Используй поддержку окружения и празднуй небольшие победы; налаживай связи, договаривайся в неформальной атмосфере — это поможет в продвижении планов.",
            "image": "cards/advice/9.jpg"
        },
        {
            "name": "Колесница",
            "text": "Действуй решительно и целеустремлённо; сочетай волю с контролем, чтобы быстро двигаться к цели. Сосредоточься и направь энергию в одно русло для максимального эффекта.",
            "image": "cards/advice/10.jpg"
        }
    ]
}

theme_names = {
    "love": "Отношения",
    "career": "Карьера",
    "finance": "Финансы",
    "advice": "Совет",
}

# ==============================
# СОЗДАЁМ БОТА
# ==============================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==============================
# КЛАВИАТУРЫ
# ==============================
def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Мини-расклад", callback_data="mini_reading")
    builder.adjust(1)
    return builder.as_markup()


def get_theme_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="❤️ На отношения", callback_data="theme_love")
    builder.button(text="💼 На карьеру", callback_data="theme_career")
    builder.button(text="💰 На финансы", callback_data="theme_finance")
    builder.button(text="🔮 Совет", callback_data="theme_advice")
    builder.adjust(2)
    return builder.as_markup()


def get_after_reading_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔁 Сделать расклад ещё", callback_data="mini_reading")
    builder.adjust(1)
    return builder.as_markup()


def get_promo_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="💎 Купить обучение за 990 ₽", callback_data="buy_course")
    builder.button(text="🔁 Сделать расклад ещё", callback_data="mini_reading")
    builder.adjust(1)
    return builder.as_markup()


def get_buy_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Перейти к оплате", url=COURSE_LINK)
    builder.adjust(1)
    return builder.as_markup()


def get_admin_check_menu(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Подтвердить оплату", callback_data=f"approve_{user_id}")
    builder.button(text="❌ Отклонить", callback_data=f"reject_{user_id}")
    builder.adjust(1)
    return builder.as_markup()

# ==============================
# ОБРАБОТЧИКИ
# ==============================
@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Здравствуйте ✨\n\n"
        "Добро пожаловать в бот с мини-раскладами Таро.\n\n"
        "Выберите, что хотите сделать:",
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == "mini_reading")
async def mini_reading_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Выберите тему, на которую хотите получить мини-расклад:",
        reply_markup=get_theme_menu()
    )


@dp.callback_query(F.data.startswith("theme_"))
async def theme_handler(callback: CallbackQuery):
    await callback.answer()

    theme = callback.data.replace("theme_", "")

    if theme not in theme_names:
        await callback.message.answer("Не удалось определить тему расклада.")
        return

    selected_card = random.choice(cards_by_theme[theme])

    reading_text = (
        f"✨ Ваш мини-расклад на тему: {theme_names[theme]}\n\n"
        f"🃏 Карта: {selected_card['name']}\n\n"
        f"📖 Интерпретация:\n{selected_card['text']}"
    )

    promo_text = (
        "Твой расклад готов ✅\n\n"
        "А что если у тебя ВСЕГДА под рукой будет инструмент, который сможет дать все необходимые ответы "
        "и поможет сэкономить на платных раскладах?\n\n"
        "За 990 ₽ ты получишь доступ к моему телеграм-каналу с обучением по Таро, "
        "где освоишь не только этот мощный инструмент, но и при желании превратишь его "
        "в дополнительный ДОХОД 💰\n\n"
        "Что внутри канала:\n\n"
        "• Полное собрание значений карт — простые и понятные объяснения даже для новичков\n"
        "• Чёткие инструкции по раскладам и практике, чтобы сразу применять знания\n"
        "• Система обучения без зубрёжки — работа через понимание\n"
        "• Поддержка в чате и ответы на вопросы\n"
        "• Доступ навсегда\n\n"
        "После оплаты пришли сюда скриншот чека, и я отправлю доступ в закрытый Telegram-канал.\n\n"
        "Ну что? Готова стать будущей ведьмой? ✨"
    )

    image_path = selected_card.get("image")

    if image_path and os.path.exists(image_path):
        photo = FSInputFile(image_path)
        await callback.message.answer_photo(
            photo=photo,
            caption=reading_text,
            reply_markup=get_after_reading_menu()
        )
    else:
        await callback.message.answer(
            reading_text,
            reply_markup=get_after_reading_menu()
        )

    await asyncio.sleep(7)

    await callback.message.answer(
        promo_text,
        reply_markup=get_promo_menu()
    )


@dp.callback_query(F.data == "buy_course")
async def buy_course_handler(callback: CallbackQuery):
    await callback.answer()

    await callback.message.answer(
        "Для получения доступа к обучению нажмите кнопку ниже 👇\n\n"
        "После оплаты пришлите сюда скриншот чека, и я отправлю вам доступ в закрытый канал.",
        reply_markup=get_buy_menu()
    )


@dp.message(F.photo)
async def payment_screenshot_handler(message: Message):
    user = message.from_user
    photo = message.photo[-1].file_id

    username = f"@{user.username}" if user.username else "без username"
    full_name = user.full_name if user.full_name else "Без имени"

    admin_text = (
        "📩 Пришел новый скриншот оплаты\n\n"
        f"👤 Имя: {full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"🔗 Username: {username}\n\n"
        "Выберите действие ниже:"
    )

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=admin_text,
        reply_markup=get_admin_check_menu(user.id)
    )

    await message.answer(
        "Спасибо 💖\n\n"
        "Скриншот получен и отправлен на проверку.\n"
        "После проверки оплаты я пришлю вам доступ в закрытый канал."
    )


@dp.callback_query(F.data.startswith("approve_"))
async def approve_payment_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer("Оплата подтверждена")

    user_id = int(callback.data.replace("approve_", ""))

    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "Спасибо за оплату 💖\n\n"
                "Оплата подтверждена.\n"
                "Вот ссылка на закрытый канал:\n"
                f"{CHANNEL_LINK}"
            )
        )

        await callback.message.edit_caption(
            caption=f"{callback.message.caption}\n\n✅ Оплата подтверждена",
            reply_markup=None
        )

    except Exception as e:
        await callback.message.answer(
            f"Не удалось отправить сообщение пользователю.\nОшибка: {e}"
        )


@dp.callback_query(F.data.startswith("reject_"))
async def reject_payment_handler(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Нет доступа", show_alert=True)
        return

    await callback.answer("Оплата отклонена")

    user_id = int(callback.data.replace("reject_", ""))

    try:
        await bot.send_message(
            chat_id=user_id,
            text=(
                "Здравствуйте.\n\n"
                "Пока не удалось подтвердить оплату.\n"
                "Пожалуйста, проверьте чек и при необходимости отправьте скриншот повторно."
            )
        )

        await callback.message.edit_caption(
            caption=f"{callback.message.caption}\n\n❌ Оплата отклонена",
            reply_markup=None
        )

    except Exception as e:
        await callback.message.answer(
            f"Не удалось отправить сообщение пользователю.\nОшибка: {e}"
        )


@dp.message()
async def other_messages_handler(message: Message):
    await message.answer(
        "Пожалуйста, используйте кнопки ниже 👇",
        reply_markup=get_main_menu()
    )


async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())