import json
import os
from os import listdir
from os.path import isfile, join

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlite_ex import Tweet, Base, User, Picture, Mention
from sqlite_ex import Hashtag, Url, create_table, Profile
from dateutil.parser import parse

engine = create_engine('sqlite:///dr_elizabeth_research.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

mypath = os.path.dirname(os.path.realpath(__file__))

def check_if_it_s_null(value):
    """
    Check if it's an Object or not
    a = {"hashtags": []}
    a == NoneType
    """
    if type(value).__name__ == 'NoneType':
        return 0
    else:
        return 1

def get_all_the_json_files():
    """
    """
    #Get the list of all the json file
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlyjson = [f for f in onlyfiles if f.split('.')[1] == 'json']
    return onlyjson


def get_the_json_value(filename):
    """
    open the file and get the content
    """
    print(filename)
    with open(filename, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return(data)


def create_new_user(data):
    """
    insert new user into db
    """
    #user
    s_name = (data.get('user').get('screen_name'))
    user_name = (data.get('user').get('name'))
    user_id = (data.get('user').get('id'))
    new_user = User(id=user_id, name=user_name, screen_name=s_name)
    session.add(new_user)
    session.commit()
    return new_user


def create_new_tweet(data, new_user):
    """
    insert new tweet into db
    """
    #tweet
    tweet_id = data.get('id')
    language = data.get('lang',  'en')
    tweet_text = data.get('text')
    in_reply_to_user = data.get('in_reply_to_user_id')
    coord = check_if_it_s_null(data.get('coordinates'))
    geo_location = check_if_it_s_null(data.get('geo'))
    created_at = parse(data.get('created_at'))
    new_tweet = Tweet(id=tweet_id, tweet=tweet_text,
                    lang=language,created_at=created_at,
                    geo=geo_location, coordinates=coord,
                    user=new_user)
    session.add(new_tweet)
    session.commit()
    return new_tweet

def create_new_mention(data, new_tweet):
    """
    insert new mention into db
    """
    #Mention
    mentions = data.get('entities').get('user_mentions')
    if mentions:
        for value in mentions:
            #mention_id = (value.get('id'))
            mention_name = (value.get('name'))
            mention_s_name = (value.get('screen_name'))
            new_mention = Mention(name=mention_name,
            screen_name=mention_s_name,  tweet=new_tweet)
            session.add(new_mention)
            session.commit()

def create_new_hashtags(data, new_tweet):
    """
    insert new hashtags into db
    """
    #Mention
    hashtags = data.get('entities').get('hashtags')
    if hashtags:
        for value in hashtags:
            h_text = (value.get('text'))
            new_hashtag = Hashtag(text=h_text, tweet=new_tweet)
            session.add(new_hashtag)
            session.commit()

def create_new_urls(data, new_tweet):
    """
    insert new urls into db
    """
    #Mention
    urls = data.get('entities').get('urls')
    if urls:
        for value in urls:
            e_url = (value.get('expanded_url'))
            s_url = (value.get('url'))
            new_url = Url(shortened_url=s_url,
            expanded_url=e_url, tweet=new_tweet)
            session.add(new_url)
            session.commit()

def create_new_profile(data, new_user):
    """
    insert new profile into db
    """
    #tweet
    data = data.get('user')
    verify = data.get('verified')#Boolean
    loca = data.get('location')
    def_pro = data.get('default_profile')#Boolean
    def_pro_image = data.get('default_profile_image')#Boolean
    fav_count = data.get('favourites_count')
    #
    fol_count = data.get('followers_count')
    sta_count = data.get('statuses_count')
    fri_count = data.get('friends_count')
    des  = data.get('description')
    pro_img_url  = data.get('profile_image_url')
    #Need to come back for the proper parsing of the date
    created_at = parse(data.get('created_at'))
    t_zone = check_if_it_s_null(data.get('time_zone'))#null
    new_profile = Profile(verified=verify, location=loca,
        default_profile=def_pro, default_profile_image=def_pro_image,
        favourites_count=fav_count, time_zone=t_zone,
        followers_count=fol_count, statuses_count=sta_count,
        friends_count=fri_count,description=des,
        profile_image_url=pro_img_url, created_at=created_at,
                    user=new_user)
    session.add(new_profile)
    session.commit()

def parse_value(data):
    """
    """
    #user
    new_user = create_new_user(data)
    create_new_profile(data, new_user)
    #tweet
    new_tweet = create_new_tweet(data, new_user)
    create_new_mention(data, new_tweet)
    create_new_hashtags(data, new_tweet)
    create_new_urls(data, new_tweet)

def parse_each_file(onlyjson):
    """
    """
    for i in onlyjson:
        data = get_the_json_value(i)
        parse_value(data)

if __name__ == '__main__':
    #todo:
    ##need to add comments
    create_table()
    json_files = get_all_the_json_files()
    parse_each_file(json_files)
