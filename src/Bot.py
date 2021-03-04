from selenium import webdriver
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import json
import sys, traceback
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import locale


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
        self.locale = locale
        self.locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument('window-size=1920x1480')

        profile = webdriver.FirefoxProfile()
        # profile.set_preference("network.http.pipelining", True)
        # profile.set_preference("network.http.proxy.pipelining", True)
        # profile.set_preference("network.http.pipelining.maxrequests", 8)
        # profile.set_preference("content.notify.interval", 500000)
        # profile.set_preference("content.notify.ontimer", True)
        # profile.set_preference("content.switch.threshold", 250000)
        # profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
        # profile.set_preference("browser.startup.homepage", "about:blank")
        # profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
        # profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
        # profile.set_preference("loop.enabled", False)
        # profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
        # profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
        # profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
        # profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
        # profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
        # profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
        # profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
        # profile.set_preference("browser.shell.checkDefaultBrowser", False)
        # profile.set_preference("browser.startup.homepage", "about:blank")
        # profile.set_preference("browser.startup.page", 0) # blank
        # profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
        # profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
        # profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
        # profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
        # profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
        # profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
        # profile.set_preference("extensions.checkUpdateSecurity", False)
        # profile.set_preference("extensions.update.autoUpdateEnabled", False)
        # profile.set_preference("extensions.update.enabled", False)
        # profile.set_preference("general.startup.browser", False)
        # profile.set_preference("plugin.default_plugin_disabled", False)
        # profile.set_preference("permissions.default.image", 2) # Image load disabled again
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"
        self.driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=caps, options=options)
        self.driver.set_window_size(1920, 1080)
        self.start = None
    
    def run(self):
        finish = False
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
            # if self.site_name=="bandh":
            #     self.beat_bandh_bot_challenge()
            self.add_to_cart(self.website['cart_btn_obj'], self.website['product_price_obj'], self.max_price)
            self.navigate(self.website['cart_url'])
            self.checkout(self.website['checkout_btn_obj'], self.website['cvv_security_field_obj'], self.cvv_code, self.website['place_order_btn_obj'])
            self.finish()
            finish = True
        except Exception as e:
            self.logging.debug(f"{traceback.print_exc()}")
            self.finish()
        
        return finish

    def login(self, username_obj, password_obj, submit_obj):
        self.logging.info(f'Starting to Login to {self.site_name} Account')
        wait_time = 5
        if self.site_name == "newegg":
            self.wait_click(self.website['signin_btn_obj'], step_name="signin-btn")
            self.wait_type(username_obj, self.username, step_name="login-username-field")
            self.wait_click(submit_obj, step_name="login-submit-btn")
            # self.wait_type(password_obj, self.password)
            # self.wait_click(submit_obj)
            wait_time = 35
        else:
            self.wait_type(username_obj, self.username, step_name="login-username-field")
            self.wait_type(password_obj, self.password, step_name="login-password-field")
            self.wait_click(submit_obj, step_name="login-submit-btn")
        self.logging.info(f'Successfully Logged into {self.site_name} Account')
        time.sleep(wait_time)
        # Store cookies
        with open(f"{self.site_name}_cookies.json", 'w') as filehandler:
            json.dump(self.driver.get_cookies(), filehandler)
        return

    def price_check(self, kwarg_dict):
        try:
            price_selector_obj, max_price = kwarg_dict['price_selector_obj'], kwarg_dict['max_price']
            self.logging.info(f"Checking Price of {self.product['name']}")
            price = self.query_selector(price_selector_obj, timeout=5).get_attribute(price_selector_obj["attribute"])
            if self.site_name == "walmart":
                price = price.split("\n")[0].split("$")[-1]
            else:
                price = price.split("$")[-1]
            price = self.locale.atof(price)
            self.logging.info(f"Price of {self.product['name']}: ${price}")
            if price > max_price:
                self.logging.info(f" Current Product Price: ${price} > Max Price Limit: ${max_price}. Exiting Program.")
                raise ValueError
            self.logging.info(f"Current Product Price: ${price} < Max Price Limit: ${max_price}. Let's Go!")
        except:
            self.logging.info("Couldn't Complete Price Check")
            pass

        return

    def add_to_cart(self, selector_obj, price_selector_obj, max_price):
        self.logging.info(f"Adding {self.product['name']} to Cart")
        price_dict = {"price_selector_obj": price_selector_obj, "max_price": max_price}
        self.price_check(price_dict)
        if self.site_name == "bandh":
            self.wait_click(selector_obj, func=self.price_check, func_dict=price_dict, refresh=True, refresh_count=50,
                        shot_count=50, human_mode=True, step_name="addtocart-btn")
        else:
            self.wait_click(selector_obj, func=self.price_check, func_dict=price_dict, refresh=True, refresh_count=1,
                        shot_count=1000, step_name="addtocart-btn")
        return

    def find_element_with_text(self, elements, text, attribute):
        for el in elements:
            el_text = el.get_attribute(attribute)
            if text in el_text.lower():
                return el
        return None

    def checkout(self, checkout_btn, security_code_field, security_code, place_order_btn):
        self.logging.info(f"Starting Checkout of {self.product['name']}")
        shot_count, max_count = 30, 30
        # Website-sepcific Checkout Procedure
        if self.site_name =="walmart":
            self.wait_click(checkout_btn, refresh_count=1, refresh=True, shot_count=1, step_name="checkout-btn")
            self.wait_click(self.website['delivery_date_continue_btn_obj'], step_name="fulfillment-btn")
            self.wait_click(self.website['confirm_delivery_address_continue_btn_obj'], step_name="confirm-address-btn")
            self.wait_type(security_code_field, security_code, step_name="cvv-security-code-field")
            self.wait_click(self.website['review_order_btn_obj'], step_name="review-order-btn")
            
        elif self.site_name == "bestbuy":
            self.wait_click(checkout_btn, refresh_count=100, refresh=True, shot_count=20, step_name="checkout-btn")
            if self.wait_type(self.website['password_field_obj'], self.password, max_count=10, shot_count=10, human_mode=True, step_name="checkout-relogin-password-field"):
                self.wait_click(self.website['login_submit_btn_obj'], max_count=10, shot_count=10, step_name="checkout-relogin-submit-btn")
            self.wait_type(security_code_field, security_code, shot_count=30, max_count=30, step_name="cvv-security-code-field")
       
        elif self.site_name == "newegg":
            self.wait_click(checkout_btn, refresh_count=300, refresh=True, shot_count=100, step_name="checkout-btn")
            if self.wait_click(self.website['login_submit_btn_obj'], max_count=500, shot_count=500, step_name="checkout-relogin-submit-btn"):
                self.wait_type(self.website['password_field_obj'], self.password, step_name="checkout-relogin-password-field")
                self.wait_click(self.website['login_submit_btn_obj'], step_name="checkout-relogin-submit-btn")
            time.sleep(0.5)
            btn_list = self.query_selector_all(self.website['confirm_delivery_address_continue_btn_obj'], timeout=10)
            confirm_delivery_btn = self.find_element_with_text(btn_list, "continue to payment", self.website['confirm_delivery_address_continue_btn_obj']['attribute'])
            if confirm_delivery_btn:
                self.wait_click(self.website['confirm_delivery_address_continue_btn_obj'], btn=confirm_delivery_btn, step_name="confirm-delivery-btn")
            self.wait_type(security_code_field, security_code,  human_mode=True, step_name="cvv-security-code-field")
            btn_list = self.query_selector_all(self.website['confirm_delivery_address_continue_btn_obj'], timeout=10)
            review_order_btn = self.find_element_with_text(btn_list, "review your order", self.website['review_order_btn_obj']['attribute'])
            if review_order_btn:
                self.wait_click(self.website['review_order_btn_obj'], btn=review_order_btn, step_name="review-order-btn")
            shot_count, max_count = 400, 500
        
        elif self.site_name == "bandh":
            self.wait_click(checkout_btn, refresh_count=10, refresh=True, shot_count=10, human_mode=True, step_name="checkout-btn")
            if self.wait_type(self.website['username_field_obj'], self.username, max_count=3, shot_count=3, human_mode=True, step_name="login-username-field"):
                self.wait_type(self.website['password_field_obj'], self.password, step_name="login-password-field")
                self.wait_click(self.website['login_checkout_btn_obj'], step_name="login-checkout-btn")
                self.wait_click(self.website['confirm_delivery_address_continue_btn_obj'], max_count=10, shot_count=10, step_name="confirm-address-btn")
            pass

        # Place Order or end Test Mode
        if not self.test_mode:
            self.wait_click(place_order_btn, shot_count=shot_count, max_count=max_count, step_name="place_order-btn")
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

    def beat_bandh_bot_challenge(self):
        text = "Access to this page has been denied"
        elements = self.query_selector_all({"name": "", "selector": "p", "selector_type": "css_selector"})
        target = self.find_element_with_text(elements, text, "innerText")
        self.action_chain = ActionChains(self.driver)
        self.action_chain.move_to_element_with_offset(target, -1000, 20).click_and_hold().perform()
        self.action_chain.reset_actions()

    def query_selector(self, selector_obj, timeout=0.00005, poll_freq=0.000001):
        if selector_obj['selector_type'] == "css_selector":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "id":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.ID, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "class_name":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.CLASS_NAME, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "xpath":
            dom_obj = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_element_located((By.XPATH, selector_obj['selector'])))
        return dom_obj
    
    def query_selector_all(self, selector_obj, timeout=1, poll_freq=0.000001):
        if selector_obj['selector_type'] == "css_selector":
            dom_objs = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "id":
            dom_objs = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_all_elements_located((By.ID, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "class_name":
            dom_objs = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_all_elements_located((By.CLASS_NAME, selector_obj['selector'])))
        elif selector_obj['selector_type'] == "xpath":
            dom_objs = WebDriverWait(self.driver, timeout, poll_frequency=poll_freq).until(EC.presence_of_all_elements_located((By.XPATH, selector_obj['selector'])))
        return dom_objs

    def wait_click(self, selector_obj, btn=None, func=None, func_dict=None, max_count=None,
                    notif_count=10, refresh=False, refresh_count=200, shot_count=200, human_mode=False, step_name=""):
        count = 1
        while True:
            try:
                if btn is None:
                    btn = self.query_selector(selector_obj)
                if human_mode:
                    self.action_chain = ActionChains(self.driver)
                    self.action_chain.move_to_element(btn).click().perform()
                    self.action_chain.reset_actions()
                else:
                    btn.click()
                break
            except:
                time.sleep(random.uniform(0, 0.5))
                shot_condition, refresh_condition = False, False
                if count <= notif_count:
                    self.logging.info(f"Didnt Find Selector {selector_obj['name']} to Click")
                    if count == notif_count:
                        self.logging.info("...")
                if count % shot_count == 0 and count != 0 and not os.path.exists(f"../screenshots/{self.site_name}_{step_name}_clickerror_{self.dt_str}.png"):
                    self.logging.info("Taking Screenshot")
                    self.driver.get_screenshot_as_file(f"../screenshots/{self.site_name}_{step_name}_clickerror_{self.dt_str}.png")
                    if max_count and count == max_count:
                        return False
                    shot_condition = True
                if count % refresh_count == 0 and count != 0 and refresh:
                    self.logging.info("Refreshing Page")
                    time.sleep(random.uniform(0, 3))
                    self.driver.refresh()
                    if func and func_dict:
                        func(func_dict)
                    if max_count and count == max_count:
                        return False
                    refresh_condition = True
                if shot_condition or refresh_condition:
                    count = 0
            if max_count and count == max_count:
                    return False

            count +=1
        self.logging.info(f'Successfully Clicked {selector_obj["name"]}')
        return True
    
    def wait_type(self, selector_obj, text, max_count=None, notif_count=10, refresh=False, 
                    refresh_count=200, shot_count=200, step_name="",  human_mode=False):
        count = 0
        while True:
            try:
                field = self.query_selector(selector_obj)
                if human_mode:
                    self.action_chain = ActionChains(self.driver)
                    self.action_chain.click(field)
                    for char in text:
                        self.action_chain.send_keys(char)
                        time.sleep(random.uniform(0.05,0.1))
                    self.action_chain.perform()
                    self.action_chain.reset_actions()
                else:
                    field.send_keys(text)
                break
            except:
                time.sleep(random.uniform(0, 0.5))
                shot_condition, refresh_condition = False, False
                if count <= notif_count:
                    self.logging.info(f"Didnt Find Selector {selector_obj['name']} to Fill In")
                    if count == notif_count:
                        self.logging.info("...")
                if count % shot_count == 0 and count != 0 and not os.path.exists(f"../screenshots/{self.site_name}_{step_name}_typeerror_{self.dt_str}.png"):
                    self.logging.info("Taking Screenshot")
                    self.driver.get_screenshot_as_file(f"../screenshots/{self.site_name}_{step_name}_typeerror_{self.dt_str}.png")
                    if max_count and count == max_count:
                        return False
                    shot_condition = True
                if count % refresh_count == 0 and count != 0 and refresh:
                    self.logging.info("Refreshing Page")
                    self.driver.refresh()
                    time.sleep(random.uniform(0, 3))
                    if max_count and count == max_count:
                        return False
                    refresh_condition = True
                if shot_condition or refresh_condition:
                    count = 0
            
            if max_count and count == max_count:
                    return False
            count +=1
        self.logging.info(f'Successfully Filled in {selector_obj["name"]}')
        return True