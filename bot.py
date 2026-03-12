import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = "8696675449:AAGNBSU_II9Y2joV8QE8xZKoyacDgFmfVMk"

cards = [
    {
        "name": "Шут",
        "meanings": {
            "love": "В любви карта говорит о новом этапе, легкости и неожиданном знакомстве.",
            "career": "В карьере это знак нового пути, смелого решения и начала чего-то интересного.",
            "finance": "В финансах карта советует быть осторожнее с рисками и не тратить деньги спонтанно.",
            "advice": "Совет карты: попробуй посмотреть на ситуацию легче и не бойся начать сначала."
        }
    },
    {
        "name": "Императрица",
        "meanings": {
            "love": "В любви карта говорит о тепле, заботе, гармонии и развитии отношений.",
            "career": "В карьере это рост, плодотворная работа и хороший потенциал для развития.",
            "finance": "В финансах карта обещает стабильность и постепенное улучшение ситуации.",
            "advice": "Совет карты: позаботься о себе, не спеши и развивай то, что уже начал."
        }
    },
    {
        "name": "Колесо Фортуны",
        "meanings": {
            "love": "В любви возможны неожиданные повороты и изменения к лучшему.",
            "career": "В карьере карта намекает на перемены, удачный шанс и новый этап.",
            "finance": "В финансах возможны колебания, но ситуация может повернуться в плюс.",
            "advice": "Совет карты: будь гибким, принимай изменения и используй возможности."
        }
    },
    {
        "name": "Солнце",
        "meanings": {
            "love": "В любви это радость, искренность, открытость и теплые чувства.",
            "career": "В карьере карта показывает успех, признание и уверенность в своих силах.",
            "finance": "В финансах это благоприятный знак, стабильность и хороший результат.",
            "advice": "Совет карты: проявляй себя смелее и не скрывай свои сильные стороны."
        }
    }
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Мини-расклад", callback_data="mini_reading")
    builder.button(text="💎 Купить обучение", callback_data="buy_course")
    builder.adjust(1)
    return builder.as_markup()


def get_theme_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text="❤️ Любовь", callback_data="theme_love")
    builder.button(text="💼 Карьера", callback_data="theme_career")
    builder.button(text="💰 Финансы", callback_data="theme_finance")
    builder.button(text="🔮 Совет", callback_data="theme_advice")
    builder.adjust(2)
    return builder.as_markup()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Здравствуйте ✨\n\n"
        "Добро пожаловать в бот с мини-раскладами Таро.\n\n"
        "Вы можете получить короткий расклад по теме или перейти к обучению.",
        reply_markup=get_main_menu()
    )


@dp.callback_query(F.data == "mini_reading")
async def mini_reading_handler(callback: CallbackQuery):
    await callback.message.answer(
        "Выберите тему, на которую хотите получить мини-расклад:",
        reply_markup=get_theme_menu()
    )
    await callback.answer()


@dp.callback_query(F.data == "buy_course")
async def buy_course_handler(callback: CallbackQuery):
    await callback.message.answer(
        "Для покупки обучения перейдите по ссылке:\n"
        "https://example.com\n\n"
        "Сюда потом можно поставить реальную ссылку на оплату, сайт, Taplink или форму заказа."
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("theme_"))
async def theme_handler(callback: CallbackQuery):
    theme = callback.data.replace("theme_", "")

    selected_card = random.choice(cards)
    interpretation = selected_card["meanings"][theme]

    theme_names = {
        "love": "Любовь",
        "career": "Карьера",
        "finance": "Финансы",
        "advice": "Совет"
    }

    text = (
        f"✨ Ваш мини-расклад на тему: {theme_names[theme]}\n\n"
        f"🃏 Карта: {selected_card['name']}\n\n"
        f"📖 Интерпретация:\n{interpretation}\n\n"
        f"💎 Если хотите глубже изучить Таро и научиться делать расклады самостоятельно, "
        f"нажмите кнопку ниже:"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="💎 Купить обучение", callback_data="buy_course")
    builder.button(text="🔁 Сделать ещё расклад", callback_data="mini_reading")
    builder.adjust(1)

    await callback.message.answer(text, reply_markup=builder.as_markup())
    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())