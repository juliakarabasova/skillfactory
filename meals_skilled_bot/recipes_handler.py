import aiohttp

from datetime import datetime

from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types

from googletrans import Translator

from utils import meals_list, collect_recipes, gather_recipes

router = Router()
translator = Translator()


class OrderRecipe(StatesGroup):
    waiting_for_category = State()
    waiting_for_description = State()


@router.message(Command("category_search_random"))
async def category_search_random(message: Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    if not command.args.isdigit():
        await message.answer("Ошибка: аргумент должен быть целым числом без пробелов")
        return

    await state.set_data({'recipe_number': int(command.args)})

    async with aiohttp.ClientSession() as session:
        meals = await meals_list(session)
        data_dates = [item['strCategory'] for item in meals]

    builder = ReplyKeyboardBuilder()
    for date_item in data_dates:
        builder.add(types.KeyboardButton(text=date_item))
    builder.adjust(4)

    await message.answer(
        f"Выберите категорию:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
    await state.set_state(OrderRecipe.waiting_for_category.state)


@router.message(OrderRecipe.waiting_for_category)
async def choose_random_meals(message: types.Message, state: FSMContext):
    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        meals = await collect_recipes(session, category=message.text, choice_num=data['recipe_number'])

    await state.set_data({'meals_id': [item['idMeal'] for item in meals]})
    translated_meals = translator.translate(', '.join([item['strMeal'] for item in meals]), dest='ru')

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Покажи рецепты"))

    await message.answer(
        f"Как Вам такие варианты:  "
        f"{translated_meals.text}", reply_markup=builder.as_markup(resize_keyboard=True)
    )
    await state.set_state(OrderRecipe.waiting_for_description.state)


@router.message(OrderRecipe.waiting_for_description)
async def send_description(message: types.Message, state: FSMContext):
    data = await state.get_data()

    async with aiohttp.ClientSession() as session:
        meals = await gather_recipes(session, data['meals_id'])

    for meal in meals:
        """
        message example:
        Домашний Мандази

        Рецепт:
        Это рецепт, который просили многие люди, и я постарался сделать его…
        
        Ингредиенты: Самоподнимающаяся Мука, сахар, яйца, молоко
        """
        translated_name = translator.translate(meal['strMeal'], dest='ru')
        translated_recipe = translator.translate(meal['strInstructions'], dest='ru')
        translated_ingredients = translator.translate(
            ', '.join([v for k, v in meal.items() if k.startswith('strIngredient') and v]),
            dest='ru'
        )

        await message.answer(
            f"_{translated_name.text}_\n\n"
            f"*Рецепт*:\n{translated_recipe.text}\n\n"
            f"*Ингредиенты*: {translated_ingredients.text}",
            parse_mode='Markdown',
            reply_markup=types.ReplyKeyboardRemove()
        )
