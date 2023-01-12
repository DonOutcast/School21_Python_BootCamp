import os
import json
import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import BotCommand, BotCommandScopeDefault
from load_data import dict_to_json_npc, dict_to_json_enemy, dict_to_json_player, dict_to_json_location, \
    dict_to_json_question

DATABASE_PLAYERS = 'player_database.json'
DATABASE_NPC = 'npc_database.json'
DATABASE_ENEMY = 'enemy_database.json'
DATABASE_LOCATION = 'location_database.json'
DATABASE_QUESTION = 'dialog_database.json'

bot = Bot(token="", parse_mode='HTML')
dp = Dispatcher()


def load_file(db):
    with open(db, 'r', encoding='utf8') as file:
        return json.load(file)


def generation_menu_markup() -> InlineKeyboardMarkup:
    person_button = InlineKeyboardButton(text="Персонаж", callback_data="start_person")
    inventory_button = InlineKeyboardButton(text="Инвентарь", callback_data="start_inventory")
    menu_markup = InlineKeyboardBuilder()
    menu_markup.add(person_button, inventory_button)
    menu_markup = menu_markup.as_markup()
    return menu_markup


def get_names(data: dict) -> list:
    names = []
    for count in range(len(data)):
        names.append(data.get(str(count)).get("name"))
    return names


def simple_generation_buttons(names: list, callback_name) -> InlineKeyboardBuilder:
    temp_kb = InlineKeyboardBuilder()
    for name in names:
        temp_kb.add(InlineKeyboardButton(text=f"{name}", callback_data=f"{callback_name}{name}"))
        temp_kb.adjust(2)
    return temp_kb


def get_all_names_planets() -> list:
    planets_names = []
    temp = dict_to_json_location(DATABASE_LOCATION)
    for i in range(len(temp)):
        planets_names.append(temp.get(str(i)).get("name"))
    return planets_names


def generation_planets_markup() -> InlineKeyboardMarkup:
    planets_names = get_all_names_planets()
    menu_planets = simple_generation_buttons(planets_names, "planet_")
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_from_planets")
    menu_planets.add(back_button).adjust(2)
    return menu_planets.as_markup()


def generation_persons_markup() -> InlineKeyboardMarkup:
    data = load_file(DATABASE_PLAYERS)
    names = get_names(data)
    menu_persons = simple_generation_buttons(names, "person_")
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_from_persons")
    menu_persons.add(back_button).adjust(2)
    return menu_persons.as_markup()


def generation_inventory() -> InlineKeyboardMarkup:
    data = [
        "Axe",
        "Blaster",
        "Saber",
        "Food",
        "Coins",
        "Robe jedi"
    ]
    menu_items = simple_generation_buttons(data, "item_")
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_from_items")
    menu_items.add(back_button).adjust(2)
    return menu_items.as_markup()


def generation_stars_roads(planet_index: str) -> InlineKeyboardMarkup:
    if planet_index == "Death Star":
        planet_index = "3"
    elif planet_index == "Yavin":
        planet_index = "2"
    elif planet_index == "Kashyyk":
        planet_index = "0"
    elif planet_index == "Tatooine":
        planet_index = "0"

    planets = dict_to_json_location(DATABASE_LOCATION)
    neighbors_planets_index = planets.get(planet_index).get("Available paths")
    neighbors_planets_names = [planets.get(str(i)).get("name", None) for i in neighbors_planets_index]
    neighbors_planets_menu = simple_generation_buttons(neighbors_planets_names, "neighbors_")
    back_button = InlineKeyboardButton(text="Назад", callback_data="back_from_neighbor")
    neighbors_planets_menu.add(back_button).adjust(2)
    return neighbors_planets_menu.as_markup()


generation_stars_roads("Death Star")


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Запуск",
        ),
        BotCommand(
            command="help",
            description="Помощь"
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


@dp.message(aiogram.filters.Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAIBJ2O7Ib2dtHhLo24HB-jzv3cQ_jYRAAItxjEb4KjZSQgU-x7oU-pfAQADAgADbQADLQQ')
    await bot.send_message(message.from_user.id, text="Добро пожаловать", reply_markup=generation_menu_markup())

@dp.callback_query(aiogram.filters.Text(startswith="item_"))
async def cmd_get_description(callback: types.CallbackQuery):
    description = None
    parse = callback.data.split("_")[-1]
    if parse == "Axe":
        description = "Топор войны плюс 100 к бруальности"
    elif parse == "Blaster":
        description = "Чисто брутальный бластер"
    elif parse == "Saber":
        description = "Это вообще опасная вещь"
    elif parse == "Food":
        description = "Еда бывает разная выбирать порой не приходится"
    elif parse == "Coins":
        description = "Не что так не радует как звон монет в кошельке"
    elif parse == "Robe jedi":
        description = "Про халат я вообще молочу"
    await callback.message.answer(text=description, reply_markup=generation_inventory())


@dp.callback_query(aiogram.filters.Text(startswith="back_"))
async def cmd_back_all(callback: types.CallbackQuery):
    await callback.message.delete()
    parse = callback.data.split('back')[-1]
    back_kb = None
    description = None
    if parse == "_from_persons" or parse == "_from_items":
        back_kb = generation_menu_markup()
        description = "Выберите персонажа"
    elif parse == "_from_planets":
        back_kb = generation_persons_markup()
        description = "Выберите персонажа"
    elif parse == "_from_neighbor":
        back_kb = generation_planets_markup()
        description = "Куда напрвлять звездолед"
    await callback.message.answer(text=f"{description}", reply_markup=back_kb)


@dp.callback_query(aiogram.filters.Text(startswith="start_"))
async def cmd_parse_kb(callback: types.CallbackQuery):
    parse = callback.data.split('_')[1]
    await callback.message.delete()
    if parse == "person":
        await callback.message.answer(text=f"Выберите персонажа", reply_markup=generation_persons_markup())
    elif parse == "inventory":
        await callback.message.answer(text=f"Выберите персонажа", reply_markup=generation_inventory())


@dp.callback_query(aiogram.filters.Text(startswith="person_"))
async def cmd_choice_person(callback: types.CallbackQuery):
    parse = callback.data.split('_')[-1]
    player_name = None
    if parse == "Obi-Van Kenobi":
        player_name = "Obi-Van Kenobi"
    elif parse == "Mandolorian":
        player_name = "Mandolorian"
    elif parse == "Han Solo":
        player_name = "Han Solo"
    elif parse == "Luke":
        player_name = "Luke"
    await callback.message.answer(text=f"Добро пожаловать {player_name}\n Куда напрвлять звездолед",
                                  reply_markup=generation_planets_markup())


@dp.callback_query(aiogram.filters.Text(startswith=("planet_", "neighbors_")))
async def cmd_choice_planet(callback: types.CallbackQuery):
    await callback.message.delete()
    parse = callback.data.split('_')[-1]
    temp_kb = generation_stars_roads(parse)
    await callback.message.answer(text="Готовность к гипер прыжку!")
    for i in range(5, 0, -1):
        await asyncio.sleep(1)
        await callback.message.answer(text=f"{i}" + "." * i)
    await callback.message.answer_photo(
        'AgACAgIAAxkBAAIBFmO7IIeXMP_z9KefzHxpsOiNVQr_AAIJxzEb6dXZSZqNReMHNHJUAQADAgADeQADLQQ')
    await callback.message.answer(text=f"Вы на {parse}", reply_markup=temp_kb)


@dp.message(aiogram.F)
async def c(meesage: types.Message):
    print(meesage)


# Запуск процесса поллинга новых апдейтов
async def main():
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
