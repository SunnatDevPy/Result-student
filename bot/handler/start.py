from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.text_decorations import html_decoration

from bot.buttons.inl import inl_group
from bot.buttons.simple import menu_button, confirm
from bot.filter import IsAdmin
from bot.utils import access_detail, form_detail, confirm_detail, create_student, top_group_student, detail_student
from config import conf
from db import Student, Group
from state import FormStudent

start_router = Router()


@start_router.message(CommandStart())
async def command_start(msg: Message, state: FSMContext):
    if IsAdmin(conf.bot.OWNER):
        await msg.answer('Hello admin', reply_markup=menu_button(admin=True))
    else:
        user = await Student.get(msg.from_user.id)
        if user:
            await msg.answer(html_decoration.bold(await access_detail(msg)), parse_mode='HTML',
                             reply_markup=menu_button())
        else:
            await state.set_state(FormStudent.first_name)
            await msg.answer(html_decoration.bold(form_detail(msg)), parse_mode='HTML')


@start_router.message(FormStudent.first_name)
async def send_first_name(msg: Message, state: FSMContext):
    await state.update_data(first_name=msg.text)
    await state.set_state(FormStudent.last_name)
    await msg.answer(html_decoration.bold(f'Ismingiz: {msg.text}\nFamiliyangizni kiriting❗️'), parse_mode='HTML')


@start_router.message(FormStudent.last_name)
async def send_last_name(msg: Message, state: FSMContext):
    await state.update_data(last_name=msg.text)
    await state.set_state(FormStudent.group)
    await msg.answer(html_decoration.bold(f'Familiyangiz: {msg.text}\n👥Guruhingizni tanlang❗️'), parse_mode='HTML',
                     reply_markup=await inl_group())


@start_router.callback_query(FormStudent.group)
async def send_group_id(call: CallbackQuery, state: FSMContext):
    group_id = call.data.split('_')[-1]
    await state.update_data(group_id=group_id)
    await state.set_state(FormStudent.confirm)
    await call.message.answer(html_decoration.bold(await confirm_detail(await state.get_data())), parse_mode='HTML',
                              reply_markup=await confirm())


@start_router.callback_query(FormStudent.confirm)
async def send_group_id(call: CallbackQuery, state: FSMContext):
    confi = call.data
    if confi == 'yes':
        await create_student(await state.get_data(), call)
        await call.message.answer(html_decoration.bold('Malumotingiz qabul qilindi'), parse_mode='HTML',
                                  reply_markup=menu_button())
    else:
        await state.set_state(FormStudent.first_name)
    await state.clear()


@start_router.message(F.text == '📒 Mening natijam 📒')
async def send_result_in_student(msg: Message):
    student: Student = await Student.get(msg.from_user.id)
    group: Group = await Group.get(student.group_id)
    await msg.answer(html_decoration.bold(await top_group_student(group.id, student.id)), parse_mode='HTML')
    await msg.answer(html_decoration.bold(await detail_student(msg.from_user.id)), parse_mode='HTML')


@start_router.message(F.text == '📊 Statistika 📊', IsAdmin(conf.bot.OWNER))
async def send_result_in_student(msg: Message):
    groups: list[Group] = await Group.get_all()
    for i in groups:
        await msg.answer(html_decoration.bold(await top_group_student(i.id)), parse_mode='HTML')

