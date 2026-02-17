from selenium import webdriver
import threading
import time

# ==============================
# BROWSERSTACK CREDENTIALS
# ==============================
BROWSERSTACK_USERNAME = "akashsatpute_PANn9k"
BROWSERSTACK_ACCESS_KEY = "yixkVJ53HVNuM3PGzZpN"

BS_URL = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# ==============================
# BROWSER CONFIGURATIONS (5)
# ==============================
capabilities_list = [
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Chrome Windows Test"
        }
    },
    {
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "Firefox Windows Test"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "Safari macOS Test"
        }
    },
    {
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "realMobile": "true",
            "osVersion": "13",
            "sessionName": "Android Mobile Test"
        }
    },
    {
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "realMobile": "true",
            "osVersion": "16",
            "sessionName": "iOS Mobile Test"
        }
    }
]

# ==============================
# TEST FUNCTION
# ==============================
def run_test(capabilities):
    options = webdriver.ChromeOptions()
    options.set_capability("browserName", capabilities["browserName"])
    options.set_capability("browserVersion", capabilities["browserVersion"])
    options.set_capability("bstack:options", capabilities["bstack:options"])

    driver = webdriver.Remote(
        command_executor=BS_URL,
        options=options
    )

    try:
        driver.get("https://elpais.com/opinion/")
        time.sleep(5)

        title = driver.title
        print(f"✅ {capabilities['bstack:options']['sessionName']} | Title: {title}")

        # ==============================
        # ✅ ADD PASS / FAIL STATUS HERE
        # ==============================
        if "Opinión" in title or "EL PAÍS" in title:
            driver.execute_script(
                'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"passed","reason":"Page loaded successfully"}}'
            )
        else:
            driver.execute_script(
                'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"failed","reason":"Unexpected page title"}}'
            )

    except Exception as e:
        driver.execute_script(
            'browserstack_executor: {"action":"setSessionStatus","arguments":{"status":"failed","reason":"Exception occurred during test"}}'
        )
        print(e)

    finally:
        driver.quit()


# ==============================
# PARALLEL EXECUTION
# ==============================
threads = []

for caps in capabilities_list:
    t = threading.Thread(target=run_test, args=(caps,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n✅ All BrowserStack tests completed")
