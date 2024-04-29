# Класс для работы с базой данных
from peewee import *

db = SqliteDatabase('passwords.db', pragmas={'key': 'password'})



class BaseModel(Model):
    class Meta:
        database = db



class Password(BaseModel):
    name = CharField()
    password = CharField()


def create_db():
    db.create_tables([Password])


create_db()
