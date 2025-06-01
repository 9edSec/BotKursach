import os 
import asyncio
import bot.keyboards.user as bku

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.tools.tool import UserTools
from bot.other.questions import questions
from bot.other import certificate_generator


router_handler_user = Router()


class CertificateStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()


@router_handler_user.message(F.text == "Получить сертификат")
async def st_get_certificate(message: Message):
    await message.answer('''
    <b><u>🎓 Сертификат по курсу Python</u></b>

<b>Готовы завершить курс и получить сертификат?</b>

        1. Изучите материалы.
            Если вы еще не ознакомились с ними, перейдите по кнопке ниже!
            

        2. Пройдите тест.
            Он состоит из этапов, соответствующих разделам курса (с ссылками для повторения).
            

        3. Получите сертификат
            После прохождения теста, Вы получите сертификат!

<b>Важно: Этот сертификат — награда за ваше стремление к развитию, не является официальной квалификацией.</b>

<b>Желаем успехов!</b>


''', parse_mode="HTML", reply_markup= bku.kb_get_certificate())
    

@router_handler_user.message(F.text == "Частые вопросы")
async def st_faq(message: Message):
    await message.answer('''
    <b>1)Какой язык программирования выбрать для начала обучения?</b>
        Рекомендуем начать с Python. Он простой в изучении и имеет широкое применение в различных областях, таких как веб-разработка, анализ данных и машинное обучение.

    <b>2)Как я могу получить сертификат после завершения курса?</b>
        После успешного прохождения тестирования вы получите сертификат, подтверждающий ваше умение и знания по изученному курсу. Сертификат будет доступен для скачивания в формате PDF.

    <b>3)Где я могу найти учебные материалы?</b>
        Учебные материалы доступны на нашем сайте.

    <b>4)Есть ли возможность пройти тестирование несколько раз?</b>
        Да, вы можете проходить тестирование столько раз, сколько пожелаете. Ваш зачёт будет основан на наилучшем результате, поэтому вы всегда можете попробовать ещё раз, чтобы улучшить свою оценку!

    <b>5)Что делать, если у меня возникли проблемы во время обучения?</b>
        Если у вас возникли проблемы, вы можете обратиться в службу поддержки, при помощи команды /contact !
''', parse_mode="HTML", reply_markup=bku.no_response)
    

@router_handler_user.callback_query(F.data == 'no_to_respone')
async def no_response(callback: CallbackQuery):
    await callback.message.answer('Нажмите кнопку ниже, чтобы связаться с Вашим персональным помощником', reply_markup=bku.reply_kb)


'''Начало главного тестирование'''

#словарь с вопросами хранится в questions.py)

user_answers = {}

def create_answer_kb(q_idx):
    answers = questions[q_idx]["answers"]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=ans, callback_data=f"answer_{q_idx}_{i}")] for i, ans in enumerate(answers)
        ]
    )
    return keyboard


@router_handler_user.callback_query(F.data == 'take_test')
async def start_test(callback: CallbackQuery):
    user_answers.clear()
    q_idx = 0
    question_text = questions[q_idx]["question"]
    msg = await callback.message.answer(
        f"Вопрос {q_idx + 1}:\n{question_text}",
        reply_markup=create_answer_kb(q_idx)
    )
    


@router_handler_user.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery):
    data = callback.data.split("_")
    q_idx = int(data[1])
    answer_idx = int(data[2])
    user_answers[q_idx] = answer_idx  
    
    next_q = q_idx + 1
    if next_q < len(questions):
        question = questions[next_q]["question"]
        msg = await callback.message.answer(f"Вопрос {next_q+1}:\n{question}", reply_markup=create_answer_kb(next_q))
    else:
        
        await callback.message.answer("Вы прошли все вопросы. Нажмите кнопку ниже для проверки.", reply_markup=bku.check_kb)
    await callback.answer()

   


@router_handler_user.callback_query(F.data == "check_answers")
async def check_answers(callback: CallbackQuery):
    correct_count = 0
    wrong_questions = []
    for i, q in enumerate(questions):
        user_ans = user_answers.get(i)
        if user_ans == q["correct"]:
            correct_count += 1
        else:
            wrong_questions.append(i+1)  
    
    total = len(questions)
    result_msg = f"Вы правильно ответили на {correct_count} из {total} вопросов.\n"
    if wrong_questions:
        result_msg += "Ошибки в вопросах: " + ", ".join(map(str, wrong_questions))
    else:
        result_msg += "Все ответы правильные! 🎉"
    await callback.message.answer(result_msg)
    await callback.answer()

    if correct_count <= 7:
        await callback.message.answer("Для получения сертификата, нужно не менее 7 правильных ответов, иди готовься!", reply_markup=bku.restart_test_kb)
    else:
        await callback.message.answer("Нажмите на кнопку нижу, чтобы получить сертификат!", reply_markup=bku.get_certificate_kb)

        

user_data = {}


@router_handler_user.callback_query(F.data == 'get_certificate') 
async def start_certificate_fsm(callback: CallbackQuery, state: FSMContext): 
    await callback.message.answer("Пожалуйста, введите ваше имя:")
    await state.set_state(CertificateStates.waiting_for_name) 
    await callback.answer()
    

@router_handler_user.message(CertificateStates.waiting_for_name) 
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text) 
    await message.answer("Пожалуйста, введите вашу фамилию:")
    await state.set_state(CertificateStates.waiting_for_surname) 


@router_handler_user.message(CertificateStates.waiting_for_surname)
async def process_surname_and_generate(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text) 

    user_fsm_data = await state.get_data() 
    full_name = f"{user_fsm_data.get('surname')} {user_fsm_data.get('name')}"

   
    user_fsm_data = await state.get_data()
    
    name_from_state = user_fsm_data.get('name', 'ИмяНеУказано')
    surname_from_state = user_fsm_data.get('surname', 'ФамилияНеУказана')
    full_name = f"{surname_from_state} {name_from_state}".strip()

    if name_from_state == 'ИмяНеУказано' or surname_from_state == 'ФамилияНеУказана':
        await message.answer("Произошла ошибка: имя или фамилия не были сохранены. Пожалуйста, начните процесс заново.")
        await state.clear()
        return

    await message.answer(f"Генерирую сертификат для: <b>{full_name}</b>...", parse_mode="HTML")

    try:
        pdf_path = certificate_generator.generate_certificate(full_name)

        if pdf_path: 
            
            document_to_send = types.FSInputFile(
                path=pdf_path,
                filename=f"Сертификат_{full_name.replace(' ', '_')}.pdf" 
            )
            await message.answer_document(
                document=document_to_send,
                caption=f"Ваш сертификат для {full_name} готов!"
            )
            
            try:
                
                os.remove(pdf_path)
            except OSError as e:
                print(f"Ошибка при удалении файла сертификата {pdf_path}: {e}") # Логирование
        else:
            
            await message.answer(
                "К сожалению, не удалось сгенерировать ваш сертификат в данный момент. "
                "Это могло произойти из-за проблемы с файлом шаблона или другой внутренней ошибки.\n"
                "Пожалуйста, попробуйте позже или свяжитесь с администратором."
            )

    except Exception as e: 
        print(f"Непредвиденная ошибка при генерации или отправке сертификата: {e}") # Логирование
        
        await message.answer(
            "Произошла очень неожиданная ошибка при создании вашего сертификата. "
            "Пожалуйста, свяжитесь с администратором."
        )
    finally: 
        await state.clear()