import time
import json
import sys
import os
import sqlite3
from sqlite3 import Error
sys.path.append(os.path.dirname(os.getcwd()))

import random
from decorators import run_again
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

#logging.basicConfig(filename='sample.log')
logging.basicConfig(level=logging.INFO)
driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options = opt)
executes(driver)
driver.set_page_load_timeout(15)
driver.implicitly_wait(5)

post_pool=[]

time_list = [1,1,1,1,2,2,2,2,2,2,3,3,3,3,4,4,5,5,5,5,6,6,7,8]

DB_PATH= os.path.join(os.path.abspath("../.."), "insta.db")
FOLDER_NAME = os.getcwd().split("\\")[-1]
print(DB_PATH)
print(FOLDER_NAME)
with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute(f"SELECT username, password FROM account WHERE username='{FOLDER_NAME}'")
    ACCOUNT = cur.fetchall()
    print(ACCOUNT)
    USERNAME = ACCOUNT[0][0]
    PASSWORD = (Fernet(os.getenv("INSTA_KEY")).decrypt(ACCOUNT[0][1].encode())).decode('utf-8')
    print(USERNAME)
    print(PASSWORD)

query_hash = "bfa387b2992c3a52dcbe447467b4b771"

def go(url):
    logging.info(f"Loading {url}")
    try:
        driver.get(url)
    except:
        logging.error(f"Could not load {url}. Trying again...")
        driver.get("https://www.google.com")
        try:
            driver.get(url)
        except:
            logging.warning(f"Can not load {url}. Contact with support please.")
            return False
    time.sleep(random.uniform(1,2))
    scroll_down()  
    return True

def is_logged_in():
    viewer_id = driver.execute_script(
        "return window._sharedData.config.viewerId"
    )
    if viewer_id is not None:
        viewer = driver.execute_script(
            "return window._sharedData.config.viewer.username"
        )

        if viewer != USERNAME: return False
        return True
    else:
        logging.warning(f"User {USERNAME} is not logged in.")
        return False

def check_spam(wait_for = 10):
    try:
        driver.find_element_by_xpath(read_xpath(check_spam.__name__, "report_button"))
        logging.info(f"Caught on spam protections. Waiting for {wait_for/60} minutes")
        time.sleep(wait_for)
        return True
    except:
        return False

def is_page_loaded():
    second,is_loaded = 0, False
    while not is_loaded and second<5:
        page_state = driver.execute_script('return document.readyState;')
        is_loaded = True if page_state == 'complete' else time.sleep(1)
        second += 1
    return is_loaded
"""
def with_loaded(driver, func): # .get function waits for page load. then performs next function
    if is_page_loaded(driver) == True: # checks if page loaded
        return func(driver)  
    else:
        return False, func.__name__
"""
@run_again # runs twice if return is false
def check_action(func, pic_id=""):
    if is_logged_in:
        if func.__name__ == "like_a_pic":
            if not func(pic_id): # checks if gets error while performing action
                logging.info("GOT ERROR!!!!!")
                check_popup_buttons() # then checks for any popup button
                if not func(pic_id): return False  # then tries again
        else:
            if not func(): # checks if gets error while performing action
                check_popup_buttons() # then checks for any popup button
                if func(): return False  # then tries again
    else:
        login_user()
        return False # not logged in or page could not loaded

def wait_random(): #waits for random amount of time between 1 and 10 seconds
    random_float = float(str(random.choice(time_list))+ "." + str(random.choice(time_list)))
    print(f"Waiting for {random_float} seconds.")
    time.sleep(random_float)

def scroll_down():
    driver.execute_script("window.scrollBy(0, Math.floor(Math.random() * 1000) + 1000);")
    time.sleep(random.uniform(0,0.5))
    driver.execute_script("window.scrollBy(0, -10000);")
    time.sleep(random.uniform(0,0.5))

def check_popup_buttons():
    logging.info("Checking popup buttons...")
    any_clicked=False
    try:
        not_now = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cmbtv")) #not now button
        )
    except:
        logging.info("¿¿¿Not now button did not appeared???")
    else:
        time.sleep(random.uniform(0,2))
        not_now.click() 
        any_clicked = True
        logging.info("Clicked at 'Not now' button.")
    

    for i in ("Add home", "Notifications not now"):
        try:
            add_home_cancel = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]")) 
            ) # add to home page button
        except:
            logging.info(f"¿¿¿{i} button did not appeared???")
        else:
            time.sleep(random.uniform(0,2))
            add_home_cancel.click()
            any_clicked = True
            logging.info(f"Clicked {i}")
    return any_clicked

########################################################################################################

def login_user():
    if go("https://www.instagram.com"):
        logging.info(f"Logging in for {USERNAME}")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button'))
            )
        except:
            logging.error(f"Login button at home page did not load.")
        else:
            login_button.click()
        try:
            time.sleep(random.uniform(0,0.4))
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath(login_user.__name__, "input_username_XP")))
            )
        except:
            logging.error("Username input couldn't loaded")
        else:
            username.clear()
            for i in USERNAME:
                time.sleep(random.uniform(0,0.4))
                username.send_keys(i)
        try:
            time.sleep(random.uniform(0,0.4))
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='loginForm']/div[1]/div[4]/div/label/input"))
            )
        except:
            logging.error("Password input couldn't loaded")
        else:
            password.clear()
            for i in PASSWORD:
                time.sleep(random.uniform(0,0.8))
                password.send_keys(i)

        time.sleep(random.uniform(0,0.8))
        driver.find_element_by_xpath("//button[@type='submit']").click()
        if is_logged_in(): logging.info(f"LOGGED AS {USERNAME}")
        check_popup_buttons()

def get_tag_pics(tag, post_num, type="n"):
    """
    type= "t" for only top posts, "n" for only normal posts, "all" for all of them
    post_num= how many posts to make action
    """
    global post_pool
    posts_ids=[]
    
    go(f"https://www.instagram.com/explore/tags/{tag}/?__a=1")
    json_data = json.loads(driver.find_element_by_tag_name("pre").text)
    if type=="t" or type=="all":
        for i in json_data["graphql"]["hashtag"]["edge_hashtag_to_top_posts"]["edges"]:
            if post_num == len(posts_ids): break
            posts_ids.append(i["node"]["shortcode"])

    if type=="n" or type=="all":
        for i in json_data["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]:
            if post_num == len(posts_ids): break
            posts_ids.append(i["node"]["shortcode"])
    post_pool.extend(posts_ids)
    #return True, posts_ids

def get_profile_pics(username, post_num):
    global post_pool
    if go(f"https://www.instagram.com/{username}"):
        total_posts = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.count")
        liste = driver.find_elements_by_tag_name("a")
        posts_ids = []
        if total_posts > 0:
            for i in liste:
                if "/p/" in i.get_attribute("href"):
                    posts_ids.append(i.get_attribute("href").rsplit("/")[-2])
                if post_num <= total_posts:
                    if len(posts_ids) == post_num: break
                else:
                    if len(posts_ids) == total_posts: break
            post_pool.extend(posts_ids)
    """
    user_id = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.id")
    end_cursor = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.edge_owner_to_timeline_media.page_info.end_cursor")
    print(user_id, end_cursor)
    pics_url = urllib.parse.quote('{"id":"' + f'{user_id}' + '","first":50,"after":"'+ f'{end_cursor}''"}')
    go(f"https://instagram.com/graphql/query/?query_hash={query_hash}&variables=" + pics_url)
    json_data = json.loads(driver.find_element_by_tag_name("pre").text)
    print(json_data["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"])"""
    
    

def like_a_pic(pic_id):
    try:
        like_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, read_xpath(like_a_pic.__name__, "like_button")))
        )
    except:
        logging.error(f"Could not like {pic_id}")
        return False
    else:
        wait_random()
        like_button.click()
        logging.info(f"Liked {pic_id}")
        return True

def post_comment(pic_id):
    go(f"https://www.instagram.com/p/{pic_id}/comments")
    try:
        post_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, read_xpath(post_comment.__name__, "post_button")))
        )
        area = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
    except:
        logging.error(f"Could not post comment for {pic_id}")
        return False
    else:
        wait_random()
        area.clear()
        area.send_keys("❤️")
        post_button.click()
        logging.info(f"Comment posted at {pic_id}")
        return True

def like_or_comment(command, if_liked_dontcomment=False):
    global post_pool
    liked_posts = []
    commented_posts = []
    try:
        logging.info(f"Going to like {len(post_pool)} pics.{post_pool}")
        for i in post_pool:
            try:
                go(f"https://www.instagram.com/p/{i}/")
                is_liked = driver.execute_script(f"return window.__additionalData['/p/{i}/'].data.graphql.shortcode_media.viewer_has_liked")
                if command=="cl" or command=="l":
                    if not is_liked:
                        if like_a_pic(i): liked_posts.append(i)
                    else:
                        logging.info(f"{i} already has been liked.")
                if command == "cl" or command=="c":
                    if not (is_liked and if_liked_dontcomment):
                        if post_comment(i): commented_posts.append(i)
                    else:
                        logging.info(f"Did not post comment. Because post liked before.")
            except:
                logging.error(f"Problem occured while liking/commenting post.")
                continue
    except:
        if command=="cl" or command=="l":
            logging.error(f"Liked {len(liked_posts)}/{len(post_pool)}")
            logging.error(f"Could not like these: {[x for x in post_pool if x not in set(liked_posts)]}")
        if command=="cl" or command=="c":
            logging.error(f"Liked {len(commented_posts)}/{len(post_pool)}")
            logging.error(f"Could not like these: {[x for x in post_pool if x not in set(commented_posts)]}")
    else:
        if command=="cl" or command=="l":
            logging.info(f"Liking posts are done. Liked {len(liked_posts)}/{len(post_pool)}")
        if command=="cl" or command=="l":
            logging.info(f"Liking posts are done. Commented {len(commented_posts)}/{len(post_pool)}")


def follow_an_user(username):
    user_url = f"https://www.instagram.com/{username}/"
    go(user_url)
    if user_url == driver.current_url:
        try:
            driver.execute_script('window._sharedData.entry_data["HttpErrorPage"]["length"];')
            logging.error(f"{username} is not exist.")
        except:
            followed_by = driver.execute_script("return window._sharedData.entry_data.ProfilePage[0].graphql.user.followed_by_viewer;")
            if not followed_by:
                try:
                    follow_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, read_xpath(follow_an_user.__name__, "follow_button")))
                    )
                    follow_button.click()
                except:
                    if go(user_url):
                        try:
                            print(read_xpath(follow_an_user.__name__, "follow_button"))
                            follow_button = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, read_xpath(follow_an_user.__name__, "follow_button")))
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
    check_spam()





def quit_driver():
    driver.quit()


"""def get_pics_from_tag(driver):
    pass
    
    def new_tab(url='https://www.google.com/'):
        list.append(driver.current_window_handle)
        driver.execute_script("window.open('url','_blank')")
    new_tab()
    list.append(driver.current_window_handle)
    driver.switch_to.window(driver.window_handles[1])
    list.append(driver.current_window_handle)
    driver.close()
    """