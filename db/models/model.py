from sqlalchemy import BIGINT, Integer, ForeignKey
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import CreateModel


class Student(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'), nullable=True)
    ball: Mapped[int] = mapped_column(BIGINT, default=0, nullable=True, sort_order=1)
    green: Mapped[int] = mapped_column(default=0)
    red: Mapped[int] = mapped_column(default=0)
    yellow: Mapped[int] = mapped_column(default=0)
    group: Mapped['Group'] = relationship('Group', back_populates='students', lazy='selectin')


class Group(CreateModel):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    students: Mapped[list['Student']] = relationship('Student', back_populates='group', lazy='selectin',
                                                     order_by="Student.green",
                                                     collection_class=ordering_list('green'))
