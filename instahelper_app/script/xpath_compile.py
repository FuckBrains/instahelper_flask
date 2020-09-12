xpath = {}

xpath["login_user"] = {
    "login_elem" : '//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button',
    "input_username_XP" : '//input[@name="username"]',
    "input_password" : '//*[@id="loginForm"]/div[1]/div[4]/div/label/input',
    "add_home_cancel" : '//div[@role="presentation"]/div/div/div/div[3]/button[2]'
}

xpath["like_a_pic"] = {
    "like_button" : '//*[@id="react-root"]/section/main/div/div/article/div[3]/section[1]/span[1]/button'
}

xpath["follow_an_user"] = {
    "follow_button" : '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/div/div/div/span/span[1]/button'
}

xpath["check_spam"] = {
    "report_button" : '/html/body/div[4]/div/div/div/div[2]/button[1][contains(text(),"Report a Problem")]'
}

xpath["wrong_password"] = {
    "try_again" : '/html/body/div[4]/div/div/div/div[2]/button[contains(text(), "Try Again")]',
    "error" :   '//*[@id="slfErrorAlert"]'
}

xpath["post_comment"] = {
    "post_button" : '//*[@id="react-root"]/section/main/section/div/form/button'
}

xpath["log_out"] = {
    "settings" : '//*[@id="react-root"]/section/nav[1]/div/header/div/div[1]/button',
    "exit" : '//*[@id="react-root"]/section/nav[1]/div/section/div[3]/div/div[4]/div/div',
    "exit2" : '/html/body/div[4]/div/div/div/div[2]/button[1]'
}