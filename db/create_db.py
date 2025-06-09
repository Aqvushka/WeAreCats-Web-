from data import db_session
from data.cats import Cats
from data.users import Users
from data.shelters import Shelters
from random import *
import sqlalchemy


def add_admin():
    db_sess = db_session.create_session()
    user = Users()
    user.email = 'admin@mail.ru'
    user.login = 'admin'
    user.set_password('admin')
    db_sess.add(user)
    db_sess.commit()


def main():
    db_session.global_init("we_are_cats.db")


main()
add_admin()
