from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from peewee import *
from latin_words import latin_dict
from greek_words import greek_dict
from english_words import english_dict

import asyncio
import random
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from db import LatinWords, GreekWords, EnglishWords

app = FastAPI()

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()
router = Router()

dp.include_router(router)


class TestStates(StatesGroup):
    waiting_for_answer = State()


class TestCallback(CallbackData, prefix="test"):
    answer_id: int


keys_latin_list = list(latin_dict.keys())
keys_greek_list = list(greek_dict.keys())
keys_english_list = list(english_dict.keys())


@app.get("/")
async def root():
    return {"message": "Сервер бота успішно працює!"}


@router.message(Command("start"))
async def start_the_bot(message: Message):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Латинка",
                                                                                callback_data="latin_test"),
                                                           InlineKeyboardButton(text="Грецька",
                                                                                callback_data="greek_test")],
                                                          [InlineKeyboardButton(text="Англійська",
                                                                                callback_data="english_test")],
                                                          [InlineKeyboardButton(text="Про проєкт",
                                                                                callback_data="about")],
                                                          ])

    await message.answer("<blockquote>Вас вітає Medical Linguist!</blockquote>\n"
                              "<b>Medical Linguist</b> - це бот, який допоможе вам опанувати латинську,"
                              "грецьку та англійску мови для медичного спрямування.\n"
                              "\n"
                              "Щоб продовжити далі оберіть мову для вивчення",
                              parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


async def latin_words_creation(callback: CallbackQuery, state: FSMContext):
    predicted_answers = []

    user_choice = await state.get_data()
    used_words = user_choice.get("used_words")

    random_latin_word = LatinWords.select().order_by(fn.Random()).get()
    rand_word = random_latin_word.latin_original
    rand_word_translate = random_latin_word.latin_translated

    while rand_word in used_words:
        random_latin_word = LatinWords.select().order_by(fn.Random()).get()

        rand_word = random_latin_word.latin_original
        rand_word_translate = random_latin_word.latin_translated

    word_variant_one = LatinWords.select().order_by(fn.Random()).get()
    rand_translated_word_one = word_variant_one.latin_translated
    print(rand_translated_word_one)

    word_variant_two = LatinWords.select().order_by(fn.Random()).get()
    rand_translated_word_two = word_variant_two.latin_translated
    print(rand_translated_word_two)

    predicted_answers.append(rand_word_translate)
    predicted_answers.append(rand_translated_word_one)
    predicted_answers.append(rand_translated_word_two)

    if predicted_answers.count(rand_translated_word_one) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_one)

        word_variant_one = LatinWords.select().order_by(fn.Random()).get()
        rand_translated_word_one = word_variant_one.latin_translated
        print(rand_translated_word_one)

        predicted_answers.append(rand_translated_word_one)

    elif predicted_answers.count(rand_translated_word_two) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_two)

        word_variant_two = LatinWords.select().order_by(fn.Random()).get()
        rand_translated_word_two = word_variant_two.latin_translated
        print(rand_translated_word_two)

        predicted_answers.append(rand_translated_word_two)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def greek_words_creation(callback: CallbackQuery, state: FSMContext):
    predicted_answers = []

    user_choice = await state.get_data()
    used_words = user_choice.get("used_words")

    random_greek_word = GreekWords.select().order_by(fn.Random()).get()
    rand_word = random_greek_word.greek_original
    rand_word_translate = random_greek_word.greek_translated

    while rand_word in used_words:
        random_greek_word = GreekWords.select().order_by(fn.Random()).get()

        rand_word = random_greek_word.greek_original
        rand_word_translate = random_greek_word.greek_translated

    word_variant_one = GreekWords.select().order_by(fn.Random()).get()
    rand_translated_word_one = word_variant_one.greek_translated
    print(rand_translated_word_one)

    word_variant_two = GreekWords.select().order_by(fn.Random()).get()
    rand_translated_word_two = word_variant_two.greek_translated
    print(rand_translated_word_two)

    predicted_answers.append(rand_word_translate)
    predicted_answers.append(rand_translated_word_one)
    predicted_answers.append(rand_translated_word_two)

    if predicted_answers.count(rand_translated_word_one) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_one)

        word_variant_one = GreekWords.select().order_by(fn.Random()).get()
        rand_translated_word_one = word_variant_one.greek_translated
        print(rand_translated_word_one)

        predicted_answers.append(rand_translated_word_one)

    elif predicted_answers.count(rand_translated_word_two) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_two)

        word_variant_two = GreekWords.select().order_by(fn.Random()).get()
        rand_translated_word_two = word_variant_two.greek_translated
        print(rand_translated_word_two)

        predicted_answers.append(rand_translated_word_two)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


async def english_words_creation(callback: CallbackQuery, state: FSMContext):
    predicted_answers = []

    user_choice = await state.get_data()
    used_words = user_choice.get("used_words")

    random_english_word = EnglishWords.select().order_by(fn.Random()).get()
    rand_word = random_english_word.english_original
    rand_word_translate = random_english_word.english_translated

    while rand_word in used_words:
        random_english_word = EnglishWords.select().order_by(fn.Random()).get()

        rand_word = random_english_word.english_original
        rand_word_translate = random_english_word.english_translated

    word_variant_one = EnglishWords.select().order_by(fn.Random()).get()
    rand_translated_word_one = word_variant_one.english_translated
    print(rand_translated_word_one)

    word_variant_two = EnglishWords.select().order_by(fn.Random()).get()
    rand_translated_word_two = word_variant_two.english_translated
    print(rand_translated_word_two)

    predicted_answers.append(rand_word_translate)
    predicted_answers.append(rand_translated_word_one)
    predicted_answers.append(rand_translated_word_two)

    if predicted_answers.count(rand_translated_word_one) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_one)

        word_variant_one = EnglishWords.select().order_by(fn.Random()).get()
        rand_translated_word_one = word_variant_one.english_translated
        print(rand_translated_word_one)

        predicted_answers.append(rand_translated_word_one)

    elif predicted_answers.count(rand_translated_word_two) > 1:
        print(f"similar variants. {rand_word_translate}, {rand_translated_word_one}, {rand_translated_word_two}")
        predicted_answers.remove(rand_translated_word_two)

        word_variant_two = EnglishWords.select().order_by(fn.Random()).get()
        rand_translated_word_two = word_variant_two.english_translated
        print(rand_translated_word_two)

        predicted_answers.append(rand_translated_word_two)

    print(predicted_answers)
    random.shuffle(predicted_answers)
    print(predicted_answers)

    answers_keyboard = InlineKeyboardBuilder()

    for ids, predicted_answer in enumerate(predicted_answers):
        answers_keyboard.button(text=predicted_answer,
                                callback_data=TestCallback(answer_id=ids).pack()
                                )

        answers_keyboard.adjust(1)
    await state.update_data(current_variants=predicted_answers.copy())

    await callback.message.answer(f"<b>{rand_word}</b>", reply_markup=answers_keyboard.as_markup(),
                                  parse_mode=ParseMode.HTML)
    predicted_answers.clear()

    await state.update_data(right_answer=rand_word_translate, current_word=rand_word)
    await state.set_state(TestStates.waiting_for_answer)

    used_words.append(rand_word)


@router.callback_query(F.data == "latin_test")
async def latin_lang_option(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("<blockquote>=== Латинська мова ===</blockquote>", parse_mode=ParseMode.HTML)

    await state.clear()
    await state.update_data(score=0, mistakes=0, total_questions=0, lang="latin", used_words=[], words=[],
                            selected_answers=[], right_answers=[], current_variants=[])
    await latin_words_creation(callback, state)


@router.callback_query(F.data == "greek_test")
async def greek_lang_option(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("<blockquote>=== Грецька мова ===</blockquote>", parse_mode=ParseMode.HTML)

    await state.clear()
    await state.update_data(score=0, mistakes=0, total_questions=0, lang="greek", used_words=[], words=[],
                            selected_answers=[], right_answers=[], current_variants=[])
    await greek_words_creation(callback, state)


@router.callback_query(F.data == "english_test")
async def english_lang_option(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("<blockquote>=== Англійська мова ===</blockquote>", parse_mode=ParseMode.HTML)

    await state.clear()
    await state.update_data(score=0, mistakes=0, total_questions=0, lang="english", used_words=[], words=[],
                            selected_answers=[], right_answers=[], current_variants=[])
    await english_words_creation(callback, state)


@router.callback_query(TestStates.waiting_for_answer, TestCallback.filter())
async def get_answer(callback: CallbackQuery, callback_data: TestCallback, state: FSMContext):
    user_choice = await state.get_data()

    right_answer = user_choice.get("right_answer")
    score = user_choice.get("score", 0)
    mistakes = user_choice.get("mistakes", 0)
    total_questions = user_choice.get("total_questions", 0)
    language = user_choice.get("lang")

    used_words = user_choice.get("used_words")
    words = user_choice.get("words")
    selected_answers = user_choice.get("selected_answers")
    right_answers = user_choice.get("right_answers")
    current_variants = user_choice.get("current_variants")

    selected_answer_id = callback_data.answer_id
    selected_answer = current_variants[selected_answer_id]
    total_questions += 1

    if selected_answer == right_answer:
        score += 1

    elif selected_answer != right_answer:
        mistakes += 1
        previous_word = user_choice.get("current_word")

        words.append(previous_word)
        selected_answers.append(selected_answer)
        right_answers.append(right_answer)

    await state.update_data(score=score, mistakes=mistakes, total_questions=total_questions, used_words=used_words,
                            words=words, selected_answers=selected_answers, right_answers=right_answers)

    if total_questions == 10:
        used_words.clear()

        await callback.message.answer(f"<blockquote>Результати тесту</blockquote>\n"
                                      f"============================\n"
                                      f"<b>Кількість питань:</b> {total_questions}\n"
                                      f"<b>Правильні відповіді:</b> {score}\n"
                                      f"<b>Неправильні відповіді:</b> {mistakes}",
                                      parse_mode=ParseMode.HTML)

        for a, b, c in zip(words, selected_answers, right_answers):
            await callback.message.answer(f"<blockquote>Розбір помилок</blockquote>\n"
                                          f"===========================\n"
                                          f"<b>Слово:</b> {a}\n"
                                          f"<b>Ваш вибір:</b> {b}\n"
                                          f"<b>Правильний переклад:</b> {c}",
                                          parse_mode=ParseMode.HTML)

        words.clear()
        selected_answers.clear()
        right_answers.clear()

        menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Повторити",
                                                                                    callback_data=f"{language}_test"
                                                                                    )],
                                                              [InlineKeyboardButton(text="Меню",
                                                                                    callback_data="menu")],
                                                              ])

        await callback.message.answer("<blockquote>=== Тест закінчено ===</blockquote>", reply_markup=menu_keyboard,
                                      parse_mode=ParseMode.HTML)
        await state.clear()

    else:
        if language == "latin":
            await latin_words_creation(callback, state)

        elif language == "greek":
            await greek_words_creation(callback, state)

        elif language == "english":
            await english_words_creation(callback, state)

    await callback.answer()


@router.callback_query(F.data == "about")
async def about_option(callback: CallbackQuery):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню",
                                                                                callback_data="menu")],
                                                          ])

    await callback.message.answer("<blockquote>Про проєкт</blockquote>\n"
                                       "<b>Medical Linguist</b> - це бот, який допоможе вам опанувати латинську,"
                                       "грецьку та англійску мови для медичного спрямування.\n"
                                       "\n"
                                       "<blockquote>Про розробника проєкту.</blockquote>\n"
                                       "Крім розробки різноманітних програм, сайтів та онлайн-платформ, "
                                       "я є автором власного блогу з програмування під назвою <b>Magnifique numérique</b>.\n"
                                       "\n"
                                       "<blockquote>Посилання на мої соцмережі, блог і т. д.</blockquote>\n"
                                       "- <a href='https://magnifiquedigitalworld.vercel.app/'>Власний сайт</a>\n"
                                       "- <a href='https://uq2xd.weblium.site'>Блог на Друкарні</a>\n"
                                       "- <a href='https://t.me/learn4prog'>Телеграм канал</a>\n"
                                       "- <a href='https://github.com/testingdifferentfunctions-source'>Github</a>",
                                       parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


@router.callback_query(F.data == "menu")
async def replay_menu(callback: CallbackQuery):
    menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Латинка",
                                                                                callback_data="latin_test"),
                                                           InlineKeyboardButton(text="Грецька",
                                                                                callback_data="greek_test")],
                                                          [InlineKeyboardButton(text="Англійська",
                                                                                callback_data="english_test",)],
                                                          [InlineKeyboardButton(text="Про проєкт",
                                                                                callback_data="about")],
                                                          ])

    await callback.message.answer("<blockquote>Вас вітає Medical Linguist!</blockquote>\n"
                                  "<b>Medical Linguist</b> - це бот, який допоможе вам опанувати латинську,"
                                  "грецьку та англійску мови для медичного спрямування.\n"
                                  "\n"
                                  "Щоб продовжити далі оберіть мову для вивчення",
                                  parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


@app.post("/api/webhook")
async def webhook(request: Request):
    update_data = await request.json()
    update = types.Update(**update_data)
    await dp.feed_update(bot=bot, update=update)
    return {"status": 200}
