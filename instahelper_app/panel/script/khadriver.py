from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
opt = Options()
opt.add_argument("start-maximized")
opt.add_argument("disable-popup-blocking")
#opt.add_argument("headless")
#opt.add_argument('user-data-dir=C:/Users/kaanh/Desktop/User Data')
opt.add_argument(f'user-agent={user_agent}')
#get full height of website with headed chrome and below code
#height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
#opt.add_argument(f"--window-size=375, 812")
#opt.add_argument("--hide-scrollbars")

opt.add_experimental_option("excludeSwitches", [
            "enable-automation",
            "disable-background-networking",
            "disable-client-side-phishing-detection",
            "disable-default-apps",
            "disable-hang-monitor",
            "disable-popup-blocking", 
            "disable-prompt-on-repost",
            "disable-sync",
            "enable-blink-features",
            "enable-logging",
            "log-level",
            "no-first-run",
            "password-store",
            "remote-debugging-port",
            "test-type",
            "use-mock-keychain",
            ])

opt.add_experimental_option('prefs', {
        'credentials_enable_service': False,
    'profile': {
        'password_manager_enabled': False
    }
})

opt.add_experimental_option("mobileEmulation", {"deviceName" : "iPhone X"})
opt.add_experimental_option("useAutomationExtension", False)


def executes(driver):
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
    Object.defineProperty(window, 'navigator', {
        value: new Proxy(navigator, {
            has: (target, key) => (key === 'webdriver' ? false : key in target),
            get: (target, key) =>
            key === 'webdriver'
                ? undefined
                : typeof target[key] === 'function'
                ? target[key].bind(target)
                : target[key]
        })
    })
                """
        },
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
        // overwrite the `languages` property to use a custom getter
    Object.defineProperty(navigator, 'languages', {
        get: function() {
            return ['en-US', 'en'];
        },
            });

        // overwrite the `plugins` property to use a custom getter
    Object.defineProperty(navigator, 'plugins', {
        get: function() {
            // this just needs to have `length > 0`, but we could mock the plugins too
            return [1, 2, 3, 4, 5];
        },
        });

    const getParameter = WebGLRenderingContext.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // UNMASKED_VENDOR_WEBGL
    if (parameter === 37445) {
        return 'Intel Open Source Technology Center';
    }
    // UNMASKED_RENDERER_WEBGL
    if (parameter === 37446) {
        return 'Mesa DRI Intel(R) Ivybridge Mobile ';
    }

    return getParameter(parameter);
    };
                """
        },
    )
    original_user_agent_string = driver.execute_script(
        "return navigator.userAgent"
    )
    driver.execute_cdp_cmd(
        "Network.setUserAgentOverride",
        {
            "userAgent": original_user_agent_string.replace("Headless", ""),
            "platform": "iPhone",
        },
    )
