from sqlalchemy import Boolean, Column, String, UnicodeText

from Himawari.modules.sql import BASE, SESSION


class Nightmode(BASE):
    __tablename__ = "nightmode"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


Nightmode.__table__.create(checkfirst=True)


def add_nightmode(chat_id: str):
    nightmoddy = Nightmode(chat_id)
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmnightmode(chat_id: str):
    if rmnightmoddy := SESSION.query(Nightmode).get(chat_id):
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def get_all_chat_id():
    stark = SESSION.query(Nightmode).all()
    SESSION.close()
    return stark


def is_nightmode_indb(chat_id: str):
    try:
        if s__ := SESSION.query(Nightmode).get(chat_id):
            return str(s__.chat_id)
    finally:
        SESSION.close()