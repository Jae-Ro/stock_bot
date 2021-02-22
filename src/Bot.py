from selenium import webdriver
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import json

class StockBot():
    def __init__(self, site, username, password, website_dict, product_dict, logger, cvv_code, dt_str, max_price=550.00, headless=False, test_mode=True):
        self.site_name = site
        self.username = username
        self.password = password
        self.product = product_dict
        self.website = website_dict
        self.logging = logger
        self.test_mode = test_mode
        self.cvv_code = str(cvv_code)
        self.max_price = float(max_price)
        self.dt_str = dt_str
        # options = webdriver.ChromeOptions()
        # self.driver = webdriver.Chrome(chrome_options=options)
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.http.pipelining", True)
        profile.set_preference("network.http.proxy.pipelining", True)
        profile.set_preference("network.http.pipelining.maxrequests", 8)
        profile.set_preference("content.notify.interval", 500000)
        profile.set_preference("content.notify.ontimer", True)
        profile.set_preference("content.switch.threshold", 250000)
        profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
        profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
        profile.set_preference("loop.enabled", False)
        profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
        profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
        profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
        profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
        profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
        profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
        profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
        profile.set_preference("browser.shell.checkDefaultBrowser", False)
        profile.set_preference("browser.startup.homepage", "about:blank")
        profile.set_preference("browser.startup.page", 0) # blank
        profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
        profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
        profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
        profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
        profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
        profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
        profile.set_preference("extensions.checkUpdateSecurity", False)
        profile.set_preference("extensions.update.autoUpdateEnabled", False)
        profile.set_preference("extensions.update.enabled", False)
        profile.set_preference("general.startup.browser", False)
        profile.set_preference("plugin.default_plugin_disabled", False)
        profile.set_preference("permissions.default.image", 2) # Image load disabled again
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"
        self.driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=caps, options=options)
        # self.driver.maximize_window()
        self.start = None
    
    def run(self):
        try:
            self.start = time.time()
            # Logging and Storing Cookies so we don't have to login again
            if not os.path.exists(os.path.join(os.getcwd(), f"{self.site_name}_cookies.json")):
                self.navigate(self.website['login_url'])
                self.login(self.website['username_field_obj'], self.website['password_field_obj'], self.website['login_submit_btn_obj'])
                raise ValueError
            
            # Once we have the login cookies we can go directly to the product page and restore our session with our saved cookies
            self.navigate(self.product['product_url'])
            with open(f"{self.site_name}_cookies.json", 'r') as cookiesfile:
                cookies = json.load(cookiesfile)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            
            self.add_to_cart(self.website['cart_btn_obj'], self.website['product_price_obj'], self.max_price)
            self.navigate(self.website['cart_url'])
            self.checkout(
                self.website['checkout_btn_obj'],
                self.website['delivery_date_continue_btn_obj'],
                self.website['confirm_delivery_address_continue_btn_obj'],
                self.website['cvv_security_field_obj'],
                self.cvv_code,
                self.website['review_order_btn_obj'],
                self.website['place_order_btn_obj'])
            self.finish()
        except Exception as e:
            print(e)
            self.finish()

    def login(self, username_obj, password_obj, submit_obj):
        self.logging.info('Starting to Login to Walmart Account')
        self.wait_type(username_obj, self.username)
        self.wait_type(password_obj, self.password)
        self.wait_click(submit_obj)
        self.logging.info(f'Successfully Logged into {self.site_name} Account')
        time.sleep(5)
        # Store cookies
        with open(f"{self.site_name}_cookies.json", 'w') as filehandler:
            json.dump(self.driver.get_cookies(), filehandler)
        return

    def add_to_cart(self, selector_obj, price_selector_obj, max_price):
        self.logging.info(f"Checking Price of {self.product['name']}")
        price = self.get_dom_obj(price_selector_obj).get_attribute(price_selector_obj["attribute"])
        if self.site_name == "walmart":
            price = price.split("\n")[0].split("$")[-1]
        elif self.site_name == "bestbuy":
            price = price.split("$")[-1]
        price = float(price)
        self.logging.info(f"Price of {self.product['name']}: ${price}")
        if price > max_price:
            self.logging.info(f" Current Product Price: ${price} > Max Price Limit: ${max_price}. Exiting Program.")
            raise ValueError
        self.logging.info(f"Current Product Price: ${price} < Max Price Limit: ${max_price}. LET'S GOOOOO!")
        self.logging.info(f"Adding {self.product['name']} to Cart")
        self.wait_click(selector_obj, refresh=True)
        return

    def checkout(self, checkout_btn, fulfillment_btn, confirm_delivery_btn, security_code_field, 
                security_code, confirm_payment_btn, place_order_btn):
        self.logging.info(f"Starting Checkout of {self.product['name']}")
        self.wait_click(checkout_btn, step_name="checkout")
        if self.site_name =="walmart":
            self.wait_click(fulfillment_btn)
            self.wait_click(confirm_delivery_btn)
            self.wait_type(security_code_field, security_code)
            self.wait_click(confirm_payment_btn)
        elif self.site_name == "bestbuy":
            if self.wait_type(self.website['password_field_obj'], self.password, max_count=5):
                self.wait_click(self.website['login_submit_btn_obj'], max_count=1)
            self.wait_type(security_code_field, security_code)
        if not self.test_mode:
            self.wait_click(place_order_btn)
            self.logging.info(f"Your order of {self.product['name']} was succesfully placed. MISSION COMPLETE!!!!")
        else:
            self.logging.info(f"This is the end of the line for the --test_mode. Wait 10 seconds and program will terminate.")
            self.logging.info(f"Total Run Time: {time.time()-self.start}s")
            time.sleep(10)
        return

    def finish(self):
        self.logging.info(f"Finishing {self.site_name} Webdriver")
        self.driver.close()
        return
    
    def navigate(self, url):
        self.logging.info(f"Navigating to {url} ")
        self.driver.get(url)
        return

    def get_dom_obj(self, selector_obj, timeout=1, poll_freq=0.0001):
        if selector_obj['selector_type'] == "css_selector":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "id":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.ID, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "class_name":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.CLASS_NAME, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "xpath":
            dom_obj = self.driver.find_element_by_xpath(selector_obj['selector'])
        return dom_obj
    
    def wait_click(self, selector_obj, max_count=None, refresh=False, step_name=""):
        count = 0
        while True:
            try:
                btn = self.get_dom_obj(selector_obj)
                btn.click()
                break
            except:
                self.logging.info(f"Didnt Find Selector {selector_obj['name']} to Click")
                if count % 1000 == 0 and count != 0 and refresh:
                    self.logging.info("Refreshing Page")
                    self.driver.refresh()
                elif count % 100 == 0 and count != 0 and not os.path.exists(f"../screenshots/{step_name}_click_error.png"):
                    self.logging.info("Taking Screenshot")
                    self.driver.get_screenshot_as_file(f"../screenshots/{self.dt_str}/{step_name}_click_error.png")

            if max_count and count == max_count:
                return False
            count +=1
        self.logging.info(f'Successfully Clicked {selector_obj["name"]}')
        return True
    
    def wait_type(self, selector_obj, text, max_count=None, refresh=False):
        count = 0
        while True:
            try:
                field = self.get_dom_obj(selector_obj)
                field.send_keys(text)
                break
            except:
                self.logging.info(f"Didnt Find Selector {selector_obj['name']} to Fill In")
                if count % 1000 == 0 and count != 0 and refresh:
                    self.logging.info("Refreshing Page")
                    self.driver.refresh()
            if max_count and count == max_count:
                return False
            count +=1
        self.logging.info(f'Successfully Filled in {selector_obj["name"]}')
        return True