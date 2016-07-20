import json
import os
from os import listdir
from os.path import isfile, join

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlite_ex import Tweet, Base, User, Picture, Mention
from sqlite_ex import Hashtag, Url, create_table, Profile
from dateutil.parser import parse
from threading import Thread

engine = create_engine('sqlite:///dr_elizabeth_research.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

mypath = os.path.dirname(os.path.realpath(__file__))

def create_a_list_of_list(data):
    final_list=[]
    b =[]
    # You don't need `a` to be a list here, just iterate the `range` object
    for num in data:
        if len(b) < 5:
            b.append(num)
        else:
            # Add `b` to `final_list` here itself, so that you don't have
            # to check if `b` has 3 elements in it, later in the loop.
            final_list.append(b)

            # Since `b` already has 3 elements, create a new list with one element
            b = [num]

    # `b` might have few elements but not exactly 3. So, add it if it is not empty
    if len(b) != 0:
        final_list.append(b)

    return final_list

def send_this_data_to_the_thread_function(data_list_json):
    """
    data_list_json=[
        ['60c74c27-3a08-46eb-a624-0954f582219a.json',
          '6d7d0c9c-fc51-4acc-9afc-fb0bf2ef9cf4.json',
          '0000eb71-177c-4153-b4f2-779d53cf0130.json',
          '0001082b-4842-404c-afe0-003c8f9061cb.json',
          '00006244-b977-43c2-8e86-e2f3c888f84e.json'],
         ['000005f0-c1cb-4a5b-9756-f579cc686928.json',
          '00000b61-6e7e-42c6-97af-cecf46951c48.json']
    ]
    """
    for list_of_list in data_list_json:
        threadlist = []
        #for u in list_of_list:
        for u in list_of_list:
            t = Thread(target=parse_each_file, args=(u,))
            t.start()
            threadlist.append(t)
        for b in threadlist:
            b.join()

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
    new_user = session.query(User).filter(User.id == user_id).first()
    if new_user is None:
        new_user = User(id=user_id, name=user_name, screen_name=s_name)
        session.add(new_user)
        session.commit()
        #creating a profile
        create_new_profile(data, new_user)
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
    try:
        new_tweet = Tweet(id=tweet_id, tweet=tweet_text,
                    lang=language,created_at=created_at,
                    geo=geo_location, coordinates=coord,
                    user=new_user)
        session.add(new_tweet)
    except:
        import ipdb; ipdb.set_trace()
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
    #tweet
    new_tweet = create_new_tweet(data, new_user)
    create_new_mention(data, new_tweet)
    create_new_hashtags(data, new_tweet)
    create_new_urls(data, new_tweet)

def parse_each_file(onlyjson):
    """
    Insert the content of the file into the DB
    """
    #import ipdb; ipdb.set_trace()
    #for i in onlyjson:
    data = get_the_json_value(onlyjson)
    parse_value(data)

if __name__ == '__main__':
    #todo:
    ##need to add comments
    create_table('other_table.db')
    json_files = get_all_the_json_files()
    json_files = create_a_list_of_list(json_files)
    #import ipdb; ipdb.set_trace()
    send_this_data_to_the_thread_function(json_files)
    #parse_each_file(json_files)
