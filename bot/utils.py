from aiogram.types import Message, CallbackQuery

from db import Student, Group


async def access_detail(msg: Message):
    student: Student = await Student.get(msg.from_user.id)
    group: Group = await Group.get(student.group_id)
    return f'''
Salom 🙋‍♂️ {student.first_name} {student.last_name}
👥 Gurux: {group.name.title()}
Hush kelibsiz Hisobot botiga 🟥 | Just Chemistry'''


def form_detail(msg: Message):
    username = f'@{msg.from_user.username}' if msg.from_user.username else msg.from_user.first_name
    return f'''
Salom o'quvchi 🙋‍♂️ {username}
Xush kelibsiz Hisobot botiga 🟥 | Just Chemistry, 
Sizga savol beraman javob berasiz❗️

Ismingiz nima❓'''


async def confirm_detail(data):
    group: Group = await Group.get(int(data.get('group_id')))
    return f'''
Ismingiz: {data.get('first_name')}
Familiyangiz: {data.get('last_name')}
👥Guruh: {group.name.title()}

Ma'lumotlaringiz tog'rimi❓
'''


async def detail_student(student_id):
    student: Student = await Student.get(student_id)
    mativatsia = ''
    natija = "Hech qanday chegirma yo'q"
    if student.ball >= 9 and student.ball <= 10:
        mativatsia = "🟥 Tabriklayman, siz kursni yaxshi olib boryapsiz, bundan keyin ham to'xtamasdan harakat qiling."

    elif student.ball >= 6 and student.ball <= 8:
        mativatsia = "🟩 Natija yomon emas, ko'proq dars qiling, albatta bundan ham ko'p yutuqlarga erishasiz."
    elif student.ball >= 1 and student.ball <= 5:
        mativatsia = "🟨 Bugungi natija yaxshi emas, ko'proq shug'ullanish kerak."
    if student.green > 0:
        natija = f'Chegirma: {student.red * 5}%'
    return f'''\n
Ism: {student.first_name}
Familiya: {student.last_name}
Bugungi natija: {student.ball}

Kartalar soni 
🟥 Qizil: {student.red}
🟩 Yashil: {student.green}
🟨 Sariq: {student.yellow}

{mativatsia}

{natija}
    '''


async def top_group_student(group_id, student_id=False):
    group: Group = await Group.get(group_id)
    students: list[Student] = group.students
    step = 1
    text = f'Guruh nomi:  {group.name}\n\n'
    for i in students:
        s = " 🙋‍♂️" if i.id == student_id else ''
        text += f'{step}){s} {i.first_name} {i.last_name}, Cart: 🟥{i.red} ta, 🟩{i.green} ta, 🟨{i.yellow} ta\n'
        step += 1
    return text


async def create_ball(student: Student, ball):
    natija = 'Hech qanday chegirma yo\'q'
    ball = int(ball)
    if ball >= 9 and ball <= 10:
        await Student.update(student.id, ball=int(ball), red=student.red + 1)
    elif ball >= 6 and ball <= 8:
        await Student.update(student.id, ball=int(ball), green=student.green + 1)
    elif ball >= 1 and ball <= 5:
        await Student.update(student.id, ball=int(ball), yellow=student.yellow + 1)
    student = await Student.get(student.id)
    if student.green > 0:
        natija = f'Chegirma: {student.red * 5}%'
    return f'''
Ball o'zgardi
Ism: {student.first_name}
Familiya: {student.last_name}

Bugungi natija: {student.ball}

Kartalar soni 
🟥 Qizil: {student.red}
🟩 Yashil: {student.green}
🟨 Sariq: {student.yellow}

{natija}
    '''


async def create_student(data, msg):
    await Student.create(id=msg.from_user.id, username=msg.from_user.username,
                         first_name=data.get('first_name'), last_name=data.get('last_name'),
                         group_id=int(data.get('group_id')))
