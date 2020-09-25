import redis
import os
import logging
import time
import random
from shutil import copy2
from khadriver import opt, executes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from xpath import read_xpath

driver = webdriver.Chrome(executable_path=r'chromedriver.exe', options = opt)
executes(driver)
driver.set_page_load_timeout(15)
driver.implicitly_wait(10)
logging.basicConfig(level=logging.INFO)

r = redis.Redis()
driver.get("https://www.instagram.com/")
while True:
    first_element=r.lindex("tocopylist", 0)
    if  first_element is not None:
        username_data = r.lindex("tocopylist", 0).decode('utf-8')
        password_data = r.get(username_data).decode('utf-8')
        
        driver.get("https://www.instagram.com")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath("login_user", "login_elem")))
            )
        except:
            logging.error(f"Login button at home page did not load.")
        else:
            login_button.click()
        try:
            #time.sleep(random.uniform(0,0.4))
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath("login_user", "input_username_XP")))
            )
        except:
            logging.error("Username input couldn't loaded")
        else:
            username.clear()
            for i in username_data:
                #time.sleep(random.uniform(0,0.4))
                username.send_keys(i)
        try:
            #time.sleep(random.uniform(0,0.4))
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath("login_user", "input_password")))
            )
        except:
            logging.error("Password input couldn't loaded")
        else:
            password.clear()
            for i in password_data:
                #time.sleep(random.uniform(0,0.8))
                password.send_keys(i)

        #time.sleep(random.uniform(0,0.8))
        driver.find_element_by_xpath("//button[@type='submit']").click()
        if driver.current_url(r"https://www.instagram.com/accounts/onetap/?next=%2F"):
            try:
                not_now = WebDriverWait(driver, 7).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "cmbtv")) #not now button
                )
            except:
                logging.info("¿¿¿Not now button did not appeared???")
            else:
                #time.sleep(random.uniform(0,2))
                not_now.click() 
                any_clicked = True
                logging.info("Clicked at 'Not now' button.")
            viewer_id = driver.execute_script(
            "return window._sharedData.config.viewerId"
            )
        if viewer_id == None:
            for i in ["try_again", "error"]:
                stop = 0
                try:
                    try_again = WebDriverWait(driver, 7).until(
                        EC.presence_of_element_located((By.XPATH, read_xpath("wrong_password", i))) #try again
                    )
                    try:
                        try_again.click()
                        r.set(username_data+"message", "Username/Password is incorrect.", 3000)
                    except:
                        pass
                    if r.get(username_data+"message") is None:
                        r.set(username_data+"message", try_again.text)
                    stop = 1
                except:
                    logging.error("")
                else:
                    print("7")
                    if stop == 1:
                        break
            r.lrem("tocopylist", 1, username_data)
            
        elif viewer_id != None:
            parent_directory = os.getcwd()
            new_directory = username_data
            new_path = os.path.join(parent_directory,new_directory)
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            copy2("utils.py", new_path)
            copy2("utils.py", new_path)
            pipe = r.pipeline()
            pipe.lrem("tocopylist", 1, username_data)
            pipe.delete(username_data)
            pipe.execute()
            driver.get(f"https://www.instagram.com/{username_data}/")
            try:
                settings_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, read_xpath("log_out", "settings")))
                )
            except:
                logging.error(f"Settings button at profile page did not load.")
            else:
                settings_button.click()

            try:
                exit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath("log_out", "exit")))
            )
            except:
                logging.error(f"Exit button at settings page did not load.")
            else:
                exit_button.click()

            try:
                exit2_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, read_xpath("log_out", "exit2")))
            )
            except:
                logging.error(f"Exit button at settings page did not load.")
            else:
                exit2_button.click()


            