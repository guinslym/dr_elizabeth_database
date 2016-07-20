import os
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#I don't know if DR Elizabeth wants MYSLQ or Mongo
#but she should choose MongoDb

class TimestampMixin(object):
    created = Column(DateTime, default=datetime.now())

class Tweet(Base, TimestampMixin):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    user_name = Column(String(250), nullable=False)
    user_screen_name = Column(String(250), nullable=False)
    profile_verified = Column(Integer)
    profile_location = Column(Integer)
    profile_default_profile = Column(Integer)
    profile_default_profile_image = Column(Integer)
    profile_favourites_count = Column(Integer)
    #profile_listed_count = Column(Integer)
    profile_followers_count = Column(Integer)
    profile_statuses_count = Column(Integer)
    profile_friends_count = Column(Integer)
    profile_created_at = Column(DateTime)
    profile_time_zone = Column(String(250))
    profile_profile_image_url = Column(String(250))
    profile_description = Column(String(250))
    tweet_text = Column(String(250), nullable=False)
    tweet_lang = Column(String(7))
    tweet_in_reply_to_user_id = Column(Integer)
    tweet_coordinates = Column(Integer)
    tweet_geo = Column(Integer)
    tweet_created_at = Column(DateTime)

class Mention(TimestampMixin, Base):
    __tablename__ = 'mention'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    screen_name = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Hashtag(TimestampMixin, Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    text = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

class Url(TimestampMixin, Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    expanded_url = Column(String(250), nullable=False)
    shortened_url = Column(String(250), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweet.id'))
    tweet = relationship(Tweet)

def create_table(dbname="dr_elizabeth_research_merged.db"):
    try:
        os.remove(dbname)
    except:
        pass
    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('sqlite:///'+dbname)

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_table()
