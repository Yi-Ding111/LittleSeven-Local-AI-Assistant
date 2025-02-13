from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


driver_service = Service(ChromeDriverManager().install())
driver_service.start()


def google_chrome_search(kw: str) -> str:
    import time
    import random
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    # setup chrome options
    options = Options()

    # Disguise the user agent (make Google think it's a normal user)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )

    # Open Chrome in Incognito mode
    options.add_argument("--incognito")

    # Disable Automation Flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Maximize Window
    options.add_argument("--start-maximized")

    # # start Chrome
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get("https://www.google.com")

    # wait page loading
    time.sleep(random.uniform(1, 3))

    # Find the search box
    search_box = driver.find_element(By.NAME, "q")

    # Simulate mouse movement to the search box
    action = ActionChains(driver)
    action.move_to_element(search_box).perform()

    # Enter keywords
    search_box.send_keys(kw)

    time.sleep(random.uniform(1, 2))

    # Press enter to search
    search_box.send_keys(Keys.RETURN)

    return None


def google_chrome_search_tool(kw: str) -> str:
    google_chrome_search(kw=kw)

    return "AgentFinished, you just need to response the webpage is already open."
