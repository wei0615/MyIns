from datetime import datetime
from sqlalchemy import (Column,Integer,String,DateTime,ForeignKey)
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship

from .db import Base,DBSession

session = DBSession()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(50),unique=True,nullable=False)
    nickname = Column(String(50),nullable=False)
    password = Column(String(50),nullable=False)
    user_img = Column(String(80))
    create_time = Column(DateTime,default=datetime.now())

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id,self.username)

    @classmethod
    def is_exists(cls,username):
        return session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def add_user(cls,username,nickname,password):
        user = User(username=username,nickname=nickname,password=password)
        session.add(user)
        session.commit()

    @classmethod
    def get_pass(cls,username,db_session):
        user = db_session.query(cls).filter_by(username=username).first()
        if user:
            return user.password
        else:
            return ''

class Img(Base):
    """
    用户图片信息
    """
    __tablename__ = 'imgs'

    id = Column(Integer,primary_key=True,autoincrement=True)
    image_url = Column(String(80))
    thumb_url = Column(String(80))

    describe = Column(String(200))
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    user = relationship('User',backref='imgs',uselist=False)
    upload_time = Column(DateTime,default=datetime.now)

    def __repr__(self):
        return '<Img(#{})>'.format(self.id)

class Comment(Base):
    """
    图片评论信息
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    img_id = Column(Integer,ForeignKey('imgs.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    comments = Column(String(200))
    user = relationship('User', backref='comments', uselist=False)
    create_time = Column(DateTime,default=datetime.now)



class Like(Base):
    """
    用户喜欢的图片
    """
    __tablename__ = 'likes'

    user_id = Column(Integer,ForeignKey('users.id'),nullable=False,primary_key=True)
    likeimg_id = Column(Integer,ForeignKey('imgs.id'),nullable=False,primary_key=True)



if __name__ == '__main__':
    Base.metadata.create_all()