from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    TimeoutException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = None
wait = None
last_youtube_results = []


# ======================
# DRIVER MANAGEMENT
# ======================

def create_driver():
    global driver, wait

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 10)


def ensure_driver():
    global driver
    try:
        if driver is None:
            create_driver()
        else:
            driver.current_url  # test session
    except:
        create_driver()


def close_browser():
    global driver
    try:
        if driver:
            driver.quit()
    except:
        pass
    finally:
        driver = None
    return True


# ======================
# GOOGLE SEARCH
# ======================

def search_google(query):
    ensure_driver()

    try:
        driver.get("https://www.google.com")

        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        return True

    except Exception as e:
        print("Google search error:", e)
        return False


def open_nth_result(n=1):
    ensure_driver()

    try:
        results = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )

        if len(results) >= n:
            results[n - 1].click()
            return True

    except Exception as e:
        print("Open result error:", e)

    return False

def open_first_result():
    return open_nth_result(1)

# ======================
# YOUTUBE SECTION
# ======================

def is_youtube_active():
    try:
        return driver and "youtube.com" in driver.current_url
    except:
        return False


def play_youtube_video(query):
    global last_youtube_results
    ensure_driver()

    try:
        driver.get("https://www.youtube.com")

        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )

        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        videos = wait.until(
            EC.presence_of_all_elements_located((By.ID, "video-title"))
        )

        if videos:
            last_youtube_results = videos
            videos[0].click()
            skip_ads()
            return True

    except Exception as e:
        print("YouTube error:", e)

    return False


def play_nth_youtube(n):
    global last_youtube_results

    try:
        if len(last_youtube_results) >= n:
            last_youtube_results[n - 1].click()
            skip_ads()
            return True
    except:
        pass

    return False


# ======================
# VIDEO CONTROLS
# ======================

def toggle_play_pause():
    if is_youtube_active():
        driver.find_element(By.TAG_NAME, "body").send_keys("k")
        return True
    return False


def fullscreen_video():
    if is_youtube_active():
        driver.find_element(By.TAG_NAME, "body").send_keys("f")
        return True
    return False


def increase_volume():
    if is_youtube_active():
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_UP)
        return True
    return False


def decrease_volume():
    if is_youtube_active():
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)
        return True
    return False


def skip_ads():
    try:
        skip_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
        )
        skip_button.click()
    except:
        pass


# ======================
# NAVIGATION
# ======================

def go_back():
    try:
        driver.back()
        return True
    except:
        return False


def scroll_down():
    try:
        driver.execute_script("window.scrollBy(0, 600);")
        return True
    except:
        return False


def scroll_up():
    try:
        driver.execute_script("window.scrollBy(0, -600);")
        return True
    except:
        return False


def refresh_page():
    try:
        driver.refresh()
        return True
    except:
        return False