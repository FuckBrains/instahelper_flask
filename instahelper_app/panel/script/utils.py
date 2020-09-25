import time
import json
import sys
import os
import sqlite3
from sqlite3 import Error
sys.path.append(os.path.dirname(os.getcwd()))
import redis
import random

import logging
import urllib.parse # to encode url 

from cryptography.fernet import Fernet
from khadriver import opt,executes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xpath import read_xpath
from decorators import run_again

"""#logging.basicConfig(filename='sample.log')
logging.basicConfig(level=logging.INFO)
driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options = opt)
executes(driver)
driver.set_page_load_timeout(15)
driver.implicitly_wait(5)

r = redis.Redis()"""
post_pool=[]

time_list = [1,1,1,1,2,2,2,2,2,2,3,3,3,3,4,4,5,5,5,5,6,6,7,8]




class insta:
    def __init__(self, username, botname, password="N"):
        self.USERNAME = username
        self.botname = botname
        #self.driver = webdriver.Chrome(executable_path=r'instahelper_app/panel/script/chromedriver.exe', options = opt)
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options = opt)
        executes(self.driver)
        self.driver.set_page_load_timeout(15)
        self.driver.implicitly_wait(5)
        self.r = redis.Redis()
        #self.DB_PATH = os.path.join(os.path.abspath("../.."), "insta.db")
        #self.FOLDER_NAME = os.getcwd().split("\\")[-1]
        logging.basicConfig(filename='sample.log')
        logging.basicConfig(level=logging.INFO)
        if password == "N":
            with sqlite3.connect(r"C:\Users\kaanh\GitRepos\instahelper-flaskapp\instahelper_app\insta.db") as conn:
                cur = conn.cursor()
                #cur.execute(f"SELECT username, password FROM account WHERE username='{self.FOLDER_NAME}'")
                cur.execute(f"SELECT username, password, cookies FROM account WHERE username='{self.USERNAME}'")
                print("1")
                account2 = cur.fetchall()
                print("2")
                #self.USERNAME = account2[0][0]
                self.PASSWORD = (Fernet(os.getenv("INSTA_KEY")).decrypt(account2[0][1].encode())).decode('utf-8')
                print("3")
                #if account2[0][2] is None and not self.is_logged_in():self.login_user()
                if account2[0][2] is not None and not self.is_logged_in(False):
                    for cookie in json.loads(account2[0][2]):
                        self.driver.add_cookie(cookie)
                    self.driver.refresh()
                else:
                    self.login_user()

        else:
            self.USERNAME = username
            self.PASSWORD = password

        self.query_hash = "bfa387b2992c3a52dcbe447467b4b771"


        #self.login_user()

        
        
            
    def go(self, url):
        logging.info(f"Loading {url}")
        try:
            self.driver.get(url)
        except:
            logging.error(f"Could not load {url}. Trying again...")
            self.driver.get("https://www.google.com")
            try:
                self.driver.get(url)
            except:
                logging.warning(f"Can not load {url}. Contact with support please.")
                self.r.set(f"{self.USERNAME}{self.botname}:message", "A network problem occured")
                self.driver.quit()
                return False
        time.sleep(random.uniform(1,2))
        self.scroll_down()  
        return True

    def is_logged_in(self,ilk=True):
        if "instagram.com" not in self.driver.current_url:
            self.go("https://www.instagram.com")

        try:
            viewer_id = self.driver.execute_script(
                "return window._sharedData.config.viewerId"
            )
        except:
            return False
        if viewer_id is not None:
            viewer = self.driver.execute_script(
                "return window._sharedData.config.viewer.username"
            )
            if viewer != self.USERNAME: return False
            return True
        elif viewer_id is None and ilk == True:
            for i in ["try_again", "error"]:
                stop = 0
                try:
                    try_again = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, read_xpath("wrong_password", i))) #try again
                    )
                    try:
                        try_again.click()
                        self.r.set(self.USERNAME+":message", "Username/Password is incorrect.", 3000)
                    except:
                        pass
                    if self.r.get(self.USERNAME+":message") is None:
                        self.r.set(self.USERNAME+":message", try_again.text)
                    stop = 1
                except:
                    logging.error("")
                else:
                    if stop == 1:
                        break
            logging.warning(f"User {self.USERNAME} is not logged in.")
            return False

    def check_spam(self, wait_for = 10):
        try:
            self.driver.find_element_by_xpath(read_xpath(check_spam.__name__, "report_button"))
            logging.info(f"Caught on spam protections. Waiting for {wait_for/60} minutes")
            time.sleep(wait_for)
            return True
        except:
            return False


    @run_again # runs twice if return is false
    def check_action(self, func, pic_id=""):
        if self.is_logged_in():
            if func.__name__ == "like_a_pic":
                if not func(pic_id): # checks if gets error while performing action
                    logging.info("GOT ERROR!!!!!")
                    self.check_popup_buttons() # then checks for any popup button
                    if not func(pic_id): return False  # then tries again
            else:
                if not func(): # checks if gets error while performing action
                    self.check_popup_buttons() # then checks for any popup button
                    if func(): return False  # then tries again
        else:
            self.login_user()
            return False # not logged in or page could not loaded

    def wait_random(self): #waits for random amount of time between 1 and 10 seconds
        random_float = float(str(random.choice(time_list))+ "." + str(random.choice(time_list)))
        print(f"Waiting for {random_float} seconds.")
        time.sleep(random_float)

    def scroll_down(self):
        self.driver.execute_script("window.scrollBy(0, Math.floor(Math.random() * 1000) + 1000);")
        time.sleep(random.uniform(0,0.5))
        self.driver.execute_script("window.scrollBy(0, -10000);")
        time.sleep(random.uniform(0,0.5))

    def check_popup_buttons(self):
        logging.info("Checking popup buttons...")
        any_clicked=False
        try:
            not_now = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cmbtv")) #not now button
            )
            time.sleep(random.uniform(0,2))
            not_now.click() 
        except:
            logging.info("¿¿¿Not now button did not appeared???")
        else:
            any_clicked = True
            logging.info("Clicked at 'Not now' button.")
        for i in ("Add home", "Notifications not now"):
            try:
                add_home_cancel = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]")) 
                ) # add to home page button
                time.sleep(random.uniform(0,0.2))
                add_home_cancel.click()
            except:
                logging.info(f"¿¿¿{i} button did not appeared???")
            else:

                any_clicked = True
                logging.info(f"Clicked {i}")
        return any_clicked


    ########################################################################################################

    def login_user(self):
        if self.go("https://www.instagram.com"):
            logging.info(f"Logging in for {self.USERNAME}")
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button'))
                )
            except:
                logging.error(f"Login button at home page did not load.")
            else:
                login_button.click()
            try:
                time.sleep(random.uniform(0,0.2))
                username = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, read_xpath(self.login_user.__name__, "input_username_XP")))
                )
            except:
                logging.error("Username input couldn't loaded")
            else:
                username.clear()
                for i in self.USERNAME:
                    time.sleep(random.uniform(0,0.2))
                    username.send_keys(i)
            try:
                time.sleep(random.uniform(0,0.2))
                password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div[1]/div[4]/div/label/input"))
                )
            except:
                logging.error("Password input couldn't loaded")
            else:
                password.clear()
                for i in self.PASSWORD:
                    time.sleep(random.uniform(0,0.2))
                    password.send_keys(i)

            time.sleep(random.uniform(0,0.2))
            self.driver.find_element_by_xpath("//button[@type='submit']").click()
            self.check_popup_buttons()
            if not self.is_logged_in():return False
            
            return True

    def get_tag_pics(self, tag, post_num, type="n"):
        """
        type= "t" for only top posts, "n" for only normal posts, "all" for all of them
        post_num= how many posts to make action
        """
        global post_pool
        posts_ids=[]

        self.go(f"https://www.instagram.com/explore/tags/{tag}/?__a=1")
        try:
            json_data = json.loads(self.driver.find_element_by_tag_name("pre").text)
            if type=="t" or type=="all":
                for i in json_data["graphql"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]:
                    if int(post_num) == len(posts_ids): break
                    posts_ids.append(i["node"]["shortcode"])

            if type=="n" or type=="all":
                for i in json_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
                    if int(post_num) == len(posts_ids): break
                    posts_ids.append(i["node"]["shortcode"])
        except:
            return []
        #post_pool.extend(posts_ids)
        return posts_ids

    def get_profile_pics(self, username, post_num):
        global post_pool
        if not self.is_logged_in():
            self.login_user()
        if self.go(f"https://www.instagram.com/{username}"):
            total_posts = self.driver.execute_script(
                "return window._sharedData.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.count"
                )
            liste = self.driver.find_elements_by_tag_name("a")
            posts_ids = []
            if total_posts > 0:
                for i in liste:
                    if "/p/" in i.get_attribute("href"):
                        posts_ids.append(i.get_attribute("href").rsplit("/")[-2])
                        print(posts_ids)
                    if post_num <= total_posts:
                        if len(posts_ids) == post_num: break
                    else:
                        if len(posts_ids) == total_posts: break
                #post_pool.extend(posts_ids)
                return posts_ids
            return False
        """
        user_id = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.id")
        end_cursor = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.page_info.end_cursor")
        print(user_id, end_cursor)
        pics_url = urllib.parse.quote('{"id":"' + f'{user_id}' + '","first":50,"after":"'+ f'{end_cursor}''"}')
        go(f"https://instagram.com/graphql/query/?query_hash={query_hash}&variables=" + pics_url)
        json_data = json.loads(driver.find_element_by_tag_name("pre").text)
        print(json_data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"])"""
        
        

    def like_a_pic(self, pic_id):
        try:
            like_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, read_xpath(self.like_a_pic.__name__, "like_button")))
            )
            print("woıejq")
        except:
            logging.error(f"Could not like {pic_id}")
            return False
        else:
            self.wait_random()
            like_button.click()
            logging.info(f"Liked {pic_id}")
            return True

    def post_comment(self, pic_id):
        self.go(f"https://www.instagram.com/p/{pic_id}/comments")
        try:
            post_button = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, read_xpath(self.post_comment.__name__, "post_button")))
            )
            area = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )
        except:
            logging.error(f"Could not post comment for {pic_id}")
            return False
        else:
            self.wait_random()
            area.clear()
            area.send_keys("❤️")
            post_button.click()
            logging.info(f"Comment posted at {pic_id}")
            return True

    def like_or_comment(self,command, postpool, if_liked_dontcomment=False):
        if postpool == False:
            return False
        liked_posts = []
        commented_posts = []
        print(postpool)
        try:
            logging.info(f"Going to like {len(postpool)} pics.{postpool}")
            for postid in postpool:
                if self.botname.encode() not in self.r.lrange(self.USERNAME, 0, self.r.llen(self.USERNAME)):
                    print("23223")
                    return False
                try:
                    self.go(f"https://www.instagram.com/p/{postid}/")
                    is_liked = self.driver.execute_script(f"return window.__additionalData['/p/{postid}/'].data.graphql.shortcode_media.viewer_has_liked")
                    if command=="cl" or command=="l":
                        if not is_liked:
                            if self.like_a_pic(postid): liked_posts.append(postid)
                        else:
                            logging.info(f"{postid} already has been liked.")
                    if command == "cl" or command=="c":
                        if not (is_liked and if_liked_dontcomment):
                            if self.post_comment(postid): commented_posts.append(postid)
                        else:
                            logging.info(f"Did not post comment. Because post liked before.")
                    
                        
                except Exception as e:
                    print(e)
                    logging.error(f"Problem occured while liking/commenting post.")
                    continue
                
        except:
            if command=="cl" or command=="l":
                logging.error(f"Liked {len(liked_posts)}/{len(postpool)}")
                logging.error(f"Could not like these: {[x for x in postpool if x not in set(liked_posts)]}")
            if command=="cl" or command=="c":
                logging.error(f"Liked {len(commented_posts)}/{len(postpool)}")
                logging.error(f"Could not like these: {[x for x in postpool if x not in set(commented_posts)]}")
        else:
            if command=="cl" or command=="l":
                logging.info(f"Liking posts are done. Liked {len(liked_posts)}/{len(postpool)}")
            if command=="cl" or command=="l":
                logging.info(f"Liking posts are done. Commented {len(commented_posts)}/{len(postpool)}")
        return True

    def follow_an_user(self,username):
        user_url = f"https://www.instagram.com/{username}/"
        self.go(user_url)
        if user_url == self.driver.current_url:
            try:
                self.driver.execute_script(
                    'window._sharedData.entry_data["HttpErrorPage"]["length"];'
                    )
                logging.error(f"{username} is not exist.")
                return False
            except:
                followed_by = self.driver.execute_script(
                    "return window._sharedData.entry_data.ProfilePage[0].graphql.user.followed_by_viewer;"
                    )
                if not followed_by:
                    try:
                        if not self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.is_private"):
                            follow_button = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/div/div/span/span[1]/button' )))
                        
                        else:
                            follow_button = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/div/button' )))
                        follow_button.click()
                    except:
                        if self.go(user_url):
                            try:
                                print(read_xpath(self.follow_an_user.__name__, "follow_button"))
                                follow_button = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, read_xpath(self.follow_an_user.__name__, "follow_button")))
                                )
                                follow_button.click()
                            except:
                                logging.warning(f"Can not follow {username}. Contact with support.")
                        else:
                            logging.error(f"Could not reach {user_url}")
                        return False
                elif followed_by:
                    logging.info(f"Already following {username}")
                
        else:
            logging.error(f"Could not reach {username} profile.")
            return False
        self.check_spam()

    def get_followers(self, username, follower_count=30):
        self.r.set("hakan", "haha")
        logging.warning("0")
        try:
            self.driver.execute_script('window._sharedData.entry_data["HttpErrorPage"]["length"];')
            logging.error(f"{username} is not exist.")
            logging.warning("1")
            return False
        except:         
            query_hash="c76146de99bb02f6415203be841dd25a"
            user_url = f"https://www.instagram.com/{username}"
            self.driver.get(user_url)
            is_private = self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.is_private")
            is_followed = self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.followed_by_viewer")
            if not (is_private and not is_followed):
                user_id = self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.id")
                total_follower = self.driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.edge_followed_by.count")
                if total_follower > 0:
                    if total_follower < follower_count: follower_count = total_follower
                    followerlist_url = urllib.parse.quote(f'{{"id":"{user_id}","include_reel":true,"fetch_mutual":true,"first":100}}')
                    self.driver.get(f"https://instagram.com/graphql/query/?query_hash={query_hash}&variables=" + followerlist_url)
                    follow_pool = []
                    json_data = json.loads(self.driver.find_element_by_tag_name("pre").text)
                    for user in json_data['data']['user']['edge_followed_by']['edges']:
                        if user['node']['followed_by_viewer']:continue
                        follow_pool.append(user['node']['username'])
                        if len(follow_pool) == follower_count:break
                    
                    return follow_pool



    def quit_driver(self):
        self.go("https://www.instagram.com")
        if self.is_logged_in():
            with sqlite3.connect(r"C:\Users\kaanh\GitRepos\instahelper-flaskapp\instahelper_app\insta.db") as conn:
                cur = conn.cursor()
                cur.execute(f"UPDATE account SET cookies = '{json.dumps(self.driver.get_cookies())}' WHERE username='{self.USERNAME}'")
        self.driver.quit()

"""go("https://www.instagram.com/")
if not is_logged_in():
    login_user()"""

"""print(bool(r.get(USERNAME+"like").decode('utf-8')))  
while True:
    command = r.lindex(USERNAME, 0)
    
    if command is not None:
        
        if command.decode('utf-8') == "hashtag":
            tags = r.lrange(USERNAME+"tags", 0, r.llen(USERNAME+"tags"))
            for tag in tags:
                tag2 = tag.decode('utf-8').split(":")
                r.lpush(USERNAME+"pool", *get_tag_pics(tag2[0], tag2[1]))
                r.lrem(USERNAME+"tags", 1, tag)
                
                if bool(r.get(USERNAME+"like").decode('utf-8')) and bool(r.get(USERNAME+"comment").decode('utf-8')):
                    like_or_comment("cl", r.lrange(USERNAME+"pool", 0, r.llen(USERNAME+"pool")))
                elif bool(r.get(USERNAME+"like").decode('utf-8')):
                    like_or_comment("l", r.lrange(USERNAME+"pool", 0, r.llen(USERNAME+"pool")))
                #r.get(USERNAME+"follow")
                print(post_pool)
            
        if command.decode('utf-8') == "target":
            pass
"""