from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Group, Student


async def inl_group(admin=True):
    groups: list[Group] = await Group.get_all()
    ikb = InlineKeyboardBuilder()
    for i in groups:
        ikb.add(*[InlineKeyboardButton(text=i.name, callback_data=f'group_access_{i.id}')])
        if admin:
            ikb.add(*[InlineKeyboardButton(text='❌', callback_data=f'group_delete_{i.id}')])
    else:
        if admin:
            ikb.add(*[InlineKeyboardButton(text='Yangi guruh qo\'shish', callback_data=f'group_add')])
            ikb.add(*[InlineKeyboardButton(text='◀️ Back', callback_data=f'group_back')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def inl_student_in_group(group_id, admin=True):
    group: Group = await Group.get(group_id)
    students: list[Student] = group.students
    ikb = InlineKeyboardBuilder()
    for i in students:
        ikb.add(*[InlineKeyboardButton(text=i.first_name + ' ' + i.last_name[0],
                                       callback_data=f'student_access_{i.id}')])
        if admin:
            ikb.add(*[InlineKeyboardButton(text="Baholash", callback_data=f'student_addball_{i.id}'),
                      InlineKeyboardButton(text='❌', callback_data=f'student_delete_{i.id}')
                      ])

    ikb.add(*[InlineKeyboardButton(text='◀️ Ortga', callback_data=f'student_back')])
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


def ball():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=str(i), callback_data=f'ball_{i}') for i in range(1, 11)])
    ikb.add(*[InlineKeyboardButton(text='◀️ Ortga', callback_data='ball_back')])
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()
