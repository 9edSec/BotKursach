from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter

from bot.tools.tool import UserTools
from bot.handlers.user import router_handler_user




@router_handler_user.message(
        StateFilter(None),
)
async def fsm_reg_user(
        message: Message,
        user_type: str,
        state = FSMContext):
     
    await message.answer(
        text = UserTools
        .user_answer['msg_reg_student'] 
        if user_type == 'student' else UserTools.user_answer['msg_reg_teacher']
    )