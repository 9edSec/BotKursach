import bot.keyboards.user as bku


from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from bot.tools.tool import UserTools
from bot.schames.schames import RegUserType
from pydantic import ValidationError



router_user_command = Router()


@router_user_command.message(Command('start'))
async def start_message(message: Message):
    await message.answer(
        UserTools.user_answer['msg_start'])
    

@router_user_command.message(Command('contact'))
async def contact_message(message: Message):
    await message.answer('Нажмите кнопку ниже, чтобы связаться с Вашим персональным помощником', reply_markup=bku.reply_kb)
    

@router_user_command.message(Command('cert'))
async def cert(message:Message):
    await message.answer('Cheat enable', reply_markup=bku.get_certificate_kb)


@router_user_command.message(Command('help'))
async def help_message(message: Message, command: CommandObject):
    await message.answer('''<b><u>*Инструкция по использованию бота*</u></b>\nЭтот бот поможет Вам взаимодействовать с платформой курсов.\n
    <b>*Получить Сертификат*</b> 
            Здесь Вы можете проверить свои 
            знания, пройдя тестирование,
            Вы получите сертификат!
            
    <b>*Частые вопросы*</b>
            Здесь Вы можете получить ответ на 
            свой вопрос.
        <b>P.S. Не нашли ответа?</b> 
            Командой /contact, можете 
            обратиться в поддержку!
            
                         
<b>Все команды:</b>
    /start - перезапустить бота
    /help - *эта инструкция
    /contact - служба поддержки
                
                         ''', parse_mode="HTML", reply_markup=bku.kb_start())
    