from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.text_decorations import html_decoration

from bot.buttons.inl import inl_group, inl_student_in_group, ball
from bot.buttons.simple import settings_btn, menu_button
from bot.filter import IsAdmin
from bot.utils import create_ball, detail_student
from config import conf
from db import Group, Student
from state import GroupForm

admin_router = Router()


@admin_router.message(F.text == '⚙️ Settings ⚙️')
async def settings_handler(msg: Message):

    await msg.answer(html_decoration.bold('Settings'), parse_mode='HTML', reply_markup=settings_btn())


@admin_router.message(F.text == '👥 Group 👥')
async def settings_groups_handler(msg: Message):
    await msg.answer(html_decoration.bold('Guruxlar'), parse_mode='HTML', reply_markup=await inl_group())


@admin_router.callback_query(F.data.startswith('group_'))
async def settings_group_handler(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = call.data.split('_')

    if data[1] == 'access':
        await state.update_data(group_id=data[-1])
        group = await Group.get(int(data[-1]))
        await call.message.edit_text(html_decoration.bold(f"{group.name} gurux O'quvchilari"), parse_mode='HTML',
                                     reply_markup=await inl_student_in_group(int(data[-1])))
    elif data[1] == 'delete':
        await Group.delete(int(data[-1]))
        await call.answer(html_decoration.bold(f'Id: {data[-1]} gurux o\'chdi'), parse_mode='HTML', show_alert=True)
        await call.message.edit_text(html_decoration.bold(f'Guruxlar'), parse_mode='HTML',
                                     reply_markup=await inl_group())
    elif data[1] == 'add':
        await state.set_state(GroupForm.name)
        await call.message.answer(html_decoration.bold(f'Gurux nomi kiriting'), parse_mode='HTML')
    elif data[-1] == 'back':
        await call.message.delete()
        await call.message.answer(html_decoration.bold('Settings'), parse_mode='HTML', reply_markup=settings_btn())


@admin_router.message(GroupForm.name)
async def settings_group_handler(msg: Message):
    await Group.create(name=msg.text)
    await msg.answer(html_decoration.bold('Yangi guruh qo\'shildi'), parse_mode='HTML')
    await msg.answer(html_decoration.bold('Guruhlar'), parse_mode='HTML', reply_markup=await inl_group())


@admin_router.message(F.text == '◀️ Ortga')
async def back_to_menu(msg: Message):
    await msg.answer(html_decoration.bold('Bosh menu'), parse_mode='HTML', reply_markup=menu_button())


@admin_router.callback_query(F.data.startswith('student_'))
async def settings_group_handler(call: CallbackQuery, state: FSMContext):
    cashe = await state.get_data()
    data = call.data.split('_')
    if data[1] == 'access':
        await call.answer()
        await call.message.answer(html_decoration.bold(await detail_student(int(data[-1]))), parse_mode='HTML')
    elif data[1] == 'delete':
        group = await Group.get(int(data[-1]))
        await Student.delete(int(data[-1]))
        await call.answer(html_decoration.bold(f'Id: {data[-1]} o\'quvchi o\'chdi'), parse_mode='HTML', show_alert=True)
        await call.message.edit_text(html_decoration.bold(f"{group.name} guruh O'quvchilar"), parse_mode='HTML',
                                     reply_markup=await inl_student_in_group(int(cashe.get('group_id'))))
    elif data[1] == 'addball':
        await call.message.delete()
        student: Student = await Student.get(int(data[-1]))
        await state.update_data(student=student)
        await call.message.answer(html_decoration.bold(f'{student.first_name}ni baholash'), parse_mode='HTML',
                                  reply_markup=ball())
    elif data[-1] == 'back':
        await call.message.delete()
        await call.message.edit_text(html_decoration.bold('Guruh'), parse_mode='HTML', reply_markup=await inl_group())


@admin_router.callback_query(F.data.startswith('ball_'))
async def settings_group_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    group = await Group.get(int(data.get('group_id')))
    if call.data == 'ball_back':
        await call.message.delete()

        await call.message.delete()
        await call.message.edit_text(html_decoration.bold(f"{group.name} guruh O'quvchilar"), parse_mode='HTML',
                                     reply_markup=await inl_student_in_group(int(data.get('group_id'))))
    else:
        await call.message.delete()
        await call.message.answer(
            html_decoration.bold(await create_ball(data.get('student'), call.data.split('_')[-1])),
            parse_mode='HTML')
        await call.message.answer(html_decoration.bold(f"{group.name} guruh O'quvchilar"), parse_mode='HTML',
                                  reply_markup=await inl_student_in_group(int(data.get('group_id'))))
