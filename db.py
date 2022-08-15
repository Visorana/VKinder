"""База данных для хранения пользователей vk, всех найденных потенциальных партнеров, избранных партнеров и
позиции пользователя в его треде.
"""

import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()
engine = sq.create_engine('postgresql://username:password@localhost:5432/VKinder')
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    """Таблица для хранения информации о пользователе: идентификатор строки в базе данных, идентификатор vk, фамилия,
    имя, предпочитаемый возрастной диапазон партнера, предпочитаемый пол партнера и город.
    """
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    age_from = sq.Column(sq.Integer)
    age_to = sq.Column(sq.Integer)
    target_gender = sq.Column(sq.Integer)
    city = sq.Column(sq.String)


class Partner(Base):
    """Таблица для хранения информации о партнере: идентификатор строки в базе данных, идентификатор vk, фамилия, имя
    и идентификатор пользователя в базе данных.
    """
    __tablename__ = 'partner'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    id_User = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    user = relationship(User)


class Favorite(Base):
    """Таблица для хранения информации об избранном партнере: идентификатор строки в базе данных, идентификатор vk,
    фамилия, имя и идентификатор пользователя в базе данных.
    """
    __tablename__ = 'favorite'
    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    id_User = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    user = relationship(User)


class UserPosition(Base):
    """Таблица для хранения информации о позиции пользователя в треде: идентификатор строки в базе данных,
    идентификатор пользователя в базе данных, идентификатор vk, позиция в треде и смещение относительно первого
    найденного пользователя.
    """
    __tablename__ = 'user_position'
    id = sq.Column(sq.Integer, primary_key=True)
    id_User = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    vk_id = sq.Column(sq.Integer)
    position = sq.Column(sq.SmallInteger)
    offset = sq.Column(sq.SmallInteger)
    user = relationship(User)


def create_tables():
    """Создание таблиц, если они отсутствуют."""
    Base.metadata.create_all(engine)


def add_user(user):
    """Добавление пользователя или партнера в базу данных.

    Если пользователь уже имеется в базе данных, то функция пропускается.
    Если при попытке добавить позицию пользователя в базу данных, обнаруживается, что позиция уже есть, то она
    обновляется на номер 1.
    """
    session.expire_on_commit = False
    if isinstance(user, User) and session.query(User.vk_id).filter(User.vk_id == user.vk_id).first() is not None:
        return
    elif isinstance(user, UserPosition) and \
            session.query(UserPosition.vk_id).filter(UserPosition.vk_id == user.vk_id).first() is not None:
        update(user.vk_id, UserPosition, position=1)
    else:
        session.add(user)
        session.commit()


def update(user_id, target_table, **kwargs):
    """Обновление таблицы в базе данных.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int or Column
    :param target_table: Таблица, которую нужно обновить.
    :param kwargs: Значения для обновления.
    """
    db_user_id = get_db_id(user_id)
    if target_table is User:
        session.query(target_table).filter(target_table.id == db_user_id).update({**kwargs})
    else:
        session.query(target_table).filter(target_table.id_User == db_user_id).update({**kwargs})
    session.commit()


def delete_user(partner_id):
    """Удаление партнера из таблицы избранных.
    :param partner_id: Идентификатор пользователя vk.
    :type partner_id: int
    """
    session.expire_on_commit = False
    session.query(Favorite).filter(Favorite.vk_id == partner_id).delete()
    session.commit()


def view_favorites(user_id):
    """Возвращает список избранных партнеров.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    links = []
    db_user_id = get_db_id(user_id)
    partners_query = session.query(Favorite.vk_id).filter(Favorite.id_User == db_user_id).all()
    for link in partners_query:
        links.append(link[0])
    return links


def avoid_list(user_id):
    """Возвращает список уже найденных партнеров, которых нужно избегать при повторном поиске.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    links = []
    partners_query = session.query(Partner.vk_id).filter(Partner.id_User == user_id).all()
    for link in partners_query:
        links.append(link[0])
    return links


def get_position(user_id):
    """Возвращает позицию пользователя в треде.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    position = session.query(UserPosition.position).filter(UserPosition.vk_id == user_id).first()
    if not position:
        return_count = 0
    else:
        return_count = position[0]
    return return_count


def get_offset(user_id):
    """Возвращает смещение относительно первого найденного пользователя..

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    offset = session.query(UserPosition.offset).filter(UserPosition.vk_id == user_id).first()
    if not offset:
        return_count = 0
    else:
        return_count = offset[0]
    return return_count


def get_db_id(user_id):
    """Возвращает идентификатор пользвателя в базе данных.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    return session.query(User.id).filter(User.vk_id == user_id).first()


def get_city(user_id):
    """Возвращает идентификатор города пользователя.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    return session.query(User.city).filter(User.vk_id == user_id).first()


def get_sex(user_id):
    """Возвращает идентификатор предпочитаемого пола партнера для пользователя.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    return session.query(User.target_gender).filter(User.vk_id == user_id).first()


def get_age_from(user_id):
    """Возвращает нижний предпочитаемый диапазон возраста партнера для пользователя.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    return session.query(User.age_from).filter(User.vk_id == user_id).first()


def get_age_to(user_id):
    """Возвращает верхний предпочитаемый диапазон возраста партнера для пользователя.

    :param user_id: Идентификатор пользователя vk.
    :type user_id: int
    """
    return session.query(User.age_from).filter(User.vk_id == user_id).first()


def get_partner_id():
    """Возвращает идентификатор vk последнего партнера в базе данных."""
    return session.query(Partner.vk_id).order_by(Partner.id.desc()).first()


def get_partner_first_name():
    """Возвращает фамилию последнего партнера в базе данных."""
    return session.query(Partner.first_name).order_by(Partner.id.desc()).first()


def get_partner_last_name():
    """Возвращает имя последнего партнера в базе данных."""
    return session.query(Partner.last_name).order_by(Partner.id.desc()).first()
