import utils
import redis
from threading import Thread
import time
r = redis.Redis()
hash_bot = {}
posts_bot = {}


def start_hash_bot(username, obje):
    def finish():
        try:
            obje.quit_driver()
        except:
            pass
        r.delete(username+":hashtag:tags")
        r.delete(username+":hashtag:like")
        r.delete(username+":hashtag:comment")
        r.lrem(username, 1, ":hashtag")
        hash_bot.pop(username,None)
    try:
        tags_n = r.lrange(username+":hashtag:tags", 0, r.llen(username+":hashtag:tags"))
        like,comm = eval(r.get(username+":hashtag:like").decode("utf-8")), eval(r.get(username+":hashtag:comment").decode("utf-8"))
    except:
        try:
            finish()
        except:
            pass
    for tags in tags_n:
        tag = tags.decode('utf-8').split(":")
        if like and comm:
            if not obje.like_or_comment("cl", obje.get_tag_pics(tag[0],tag[1])):break
        elif like:
            if not obje.like_or_comment("l", obje.get_tag_pics(tag[0],tag[1])):break
        r.lrem(username+":hashtag:tags", 1, tags)
    finish()

def start_posts_bot(username, obje):
    def finish():
        try:
            obje.quit_driver()
        except:
            pass
        r.delete(username+":username:users")
        r.delete(username+":username:like")
        r.delete(username+":username:comment")
        r.lrem(username, 1, ":username")
        posts_bot.pop(username,None)
    try:
        username_n = r.lrange(username+":username:users", 0, r.llen(username+":username:users"))
        like,comm = eval(r.get(username+":username:like").decode("utf-8")), eval(r.get(username+":username:comment").decode("utf-8"))
    except:
        try:
            finish()
        except:
            pass
    for users in username_n:
        user = users.decode('utf-8').split(":")
        if like and comm:
            if not obje.like_or_comment("cl", obje.get_profile_pics(user[0],int(user[1]))):break
        elif like:
            print(user[0])
            print(int(user[1]))
            if not obje.like_or_comment("l", obje.get_profile_pics(user[0],int(user[1]))):break
        r.lrem(username+":username:users", 1, users)
    finish()

def check_new_acc():
    if r.keys("*:check"): #check login credentials
        for key in r.keys("*:check"):
            username = key.decode('utf-8').split(":")[0]
            print(username)
            if r.get(username+":check").decode('utf-8') != "True" and r.get(username+":check").decode('utf-8') != "False":
                inst = utils.insta(username, r.get(key.decode('utf-8')).decode('utf-8'))
                result = inst.login_user()
                inst.quit_driver()
                if result: r.set(username+":check", "True")
                if not result: r.set(username+":check", "False")
                time.sleep(1)
                

            

while True:
    check_new_acc()       
    if r.keys():
        for key in r.keys():
            key = key.decode('utf-8')
            if not any(x in key for x in [":tags",":comment",":like",":check", ":message"]):
                print(key)
                for bot in r.lrange(key, 0, r.llen(key)):
                    bot = bot.decode('utf-8')
                    print(bot)
                    if not hash_bot.get(key) and bot == ":hashtag": #add to hash bot list then start
                        hash_bot[key] = utils.insta(key, bot)
                        start_hash_bot(key, hash_bot.get(key))
                        break
                    if not posts_bot.get(key) and bot == ":username": #add to posts bot list then start
                        posts_bot[key] = utils.insta(key, bot)
                        start_posts_bot(key, posts_bot.get(key))
                        break
                    

            
