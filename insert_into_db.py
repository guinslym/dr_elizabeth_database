import json
import os
from os import listdir
from os.path import isfile, join

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tables import Tweet, Base, Mention
from tables import Hashtag, Url, create_table
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

def create_new_tweet(data):
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
    #user
    s_name = (data.get('user').get('screen_name'))
    user_id = (data.get('user').get('id'))
    #Profile
    profile = data.get('user')
    verify = profile.get('verified')#Boolean
    loca = profile.get('location')
    def_pro = profile.get('default_profile')#Boolean
    def_pro_image = profile.get('default_profile_image')#Boolean
    fav_count = profile.get('favourites_count')
    fol_count = profile.get('followers_count')
    sta_count = profile.get('statuses_count')
    fri_count = profile.get('friends_count')
    des  = profile.get('description')
    pro_img_url  = profile.get('profile_image_url')
    #Need to come back for the proper parsing of the date
    profile_created_at = parse(profile.get('created_at'))
    t_zone = profile.get('time_zone')#null

    new_tweet = Tweet(id=tweet_id, tweet_text=tweet_text,
                tweet_lang=language,tweet_created_at=created_at,
                tweet_geo=geo_location, tweet_coordinates=coord,
                #user
                user_id=user_id,
                user_screen_name=s_name,
                #profile
                profile_verified= verify,
                profile_location= loca,
                profile_default_profile= def_pro,
                profile_default_profile_image= def_pro_image,
                profile_favourites_count= fav_count,
                profile_followers_count= fol_count,
                profile_statuses_count= sta_count,
                profile_friends_count= fri_count,
                profile_created_at= profile_created_at,
                profile_time_zone= t_zone,
                profile_profile_image_url= pro_img_url,
                profile_description= des,
                #Picture
                )
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



def parse_value(data):
    """
    """
    #user
    #tweet
    new_tweet = create_new_tweet(data)
    create_new_mention(data, new_tweet)
    create_new_hashtags(data, new_tweet)
    create_new_urls(data, new_tweet)

def parse_each_file(onlyjson):
    """
    Insert the content of the file into the DB
    """
    total_file = len(onlyjson)
    for i in onlyjson:
        print(str(onlyjson.index(i)) + ' / ' + str(total_file))
        data = get_the_json_value(i)
        parse_value(data)

if __name__ == '__main__':
    #todo:
    ##need to add comments
    create_table()
    #import ipdb; ipdb.set_trace()
    json_files = get_all_the_json_files()
    parse_each_file(json_files)
