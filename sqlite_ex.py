import os
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now())

class User(TimestampMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    screen_name = Column(String(250), nullable=False)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    verified = Column(Integer)
    location = Column(Integer)
    default_profile = Column(Integer)
    default_profile_image = Column(Integer)
    favourites_count = Column(Integer)
    listed_count = Column(Integer)
    followers_count = Column(Integer)
    statuses_count = Column(Integer)
    friends_count = Column(Integer)
    #I don't know if the end db will be MYSLQ, PG or Mongo
    #created_at = Column(DateTime)
    created_at = Column(String(250))
    time_zone = Column(String(250))
    profile_image_url = Column(String(250))
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweet = Column(String(250), nullable=False)
    lang = Column(String(7))
    in_reply_to_user_id = Column(Integer)
    coordinates = Column(Integer)
    geo = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Mention(Base):
    __tablename__ = 'mention'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    screen_name = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Hashtag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    expanded_url = Column(String(250), nullable=False)
    shortened_url = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    profile_image_url = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

def create_table():
    try:
        os.remove("dr_elizabeth_research.db")
    except:
        pass
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///dr_elizabeth_research.db')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()
