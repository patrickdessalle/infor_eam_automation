# -*- coding: utf-8 -*-
from __future__ import print_function
__author__ = "Patrick Dessalle <https://patrick.dessalle.be>"
__copyright__ = "Copyright (c) 2020 Sourcefully SPRL"

import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CMMS(object):
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def request_login(self):
        self.driver.get(self.url)
        
        try:
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Work"))
            )
            print("User has logged on")
            if self.driver.find_element(By.ID, "eammsgbox-1010"):
                print("Dismissing the other session warning")
                self.driver.find_element(By.CSS_SELECTOR, "#eammsgbox-1010 #button-1013").click()
            time.sleep(5)
        except:
            print("Error : Timeout or other", sys.exc_info())
            self.driver.quit()
            raise("Could not login to CMMS")
            
            
    def wait_mask(self, wait=1):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body.x-masked"))
            )
        except:
            pass
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body:not(.x-masked)"))
        )
        time.sleep(wait)
        
    def open_menu(self, items):
        for item in items:
            try:
                self.find_element(By.LINK_TEXT, item).click()
            except:
                raise("Error: Menu '" + item + "' was not found", sys.exc_info())
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, items[0]))
        )
        self.wait_mask()
        time.sleep(5)
                
    def make_search(self, placeholder, value):
        try:
            self.driver.switch_to.frame(0)
        except: # User doesn't have frame
            pass
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='" + placeholder + "']"))
        )
        self.find_element(By.CSS_SELECTOR, "input[placeholder='" + placeholder + "']").clear()
        self.find_element(By.CSS_SELECTOR, "input[placeholder='" + placeholder + "']").send_keys(value)
        self.find_element(By.XPATH, "//td/input[@placeholder='" + placeholder + "']/parent::td/following-sibling::td/div[contains(@class, 'x-form-search-trigger')]").click()
        
        
        self.wait_mask()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='" + placeholder + "']"))
        )
        # Check results
        results = self.driver.find_elements(By.XPATH, "//td/input[@placeholder='Search within All PMs']/ancestor::div[starts-with(@id, 'gridsummary-')]/div[contains(@class, 'x-panel-body')]//div[contains(@class, 'gsMain')]")
        return results #[r.text for r in results]
       
        
    def click_button(self, label):
        self.find_element(By.LINK_TEXT, label).click()
        
    def click_toolbar_save(self):
        ''' Clicks on "Save Record (Ctrl+S) in the main toolbar '''
        self.click_toolbar("Save Record (Ctrl+S)")
        time.sleep(5)
        
    def click_toolbar_new(self):
        ''' Clicks on "New Record (Ctrl+N) in the main toolbar '''
        self.click_toolbar("New Record (Ctrl+N)")
        time.sleep(5)
        
    def click_toolbar(self, qtip):
        ''' Clicks on an element in the main toolbar '''
        try:
            self.driver.switch_to.frame(0)
        except: # User doesn't have frame
            pass
        self.find_element(By.CSS_SELECTOR, "div.x-toolbar[id^='maintoolbar-'] a[data-qtip='" + qtip + "']").click()
        self.wait_mask()
        
    def click_subtoolbar(self, qtip):
        ''' Clicks on an element in a toolbar (not main, likely lower on the page) '''
        try:
            self.driver.switch_to.frame(0)
        except: # User doesn't have frame
            pass
        self.find_element(By.CSS_SELECTOR, "div.x-toolbar[id^='toolbar-'] a[data-qtip='" + qtip + "']").click()
        self.wait_mask()
        
    def click_tab(self, label):
        ''' Clicks on the top tabbar on the screen'''
        try:
            self.driver.switch_to.frame(0)
        except: # User doesn't have frame
            pass
        self.find_element(By.XPATH, "//div[contains(@class, 'x-tab-bar-top']//a[text()='" + label + "']").click()
        self.wait_mask()
        
    def filter_tab(self, field, value):
        ''' Do a simple filtering (one field, one value). Does only support contains for now '''
        input_field = self.find_element(By.CSS_SELECTOR, "div.x-toolbar-dataspy input[name='filterfields']")
        input_field.clear()
        input_field.send_keys(field)
        
        input_value = self.find_element(By.CSS_SELECTOR, "div.x-toolbar-dataspy input[name='selfiltervaluectrl']")
        input_value.clear()
        input_value.send_keys(value)
        
        #Click run
        self.find_element(By.CSS_SELECTOR, "div.x-toolbar-dataspy a.uft-id-run").click()
        self.wait_mask()
        
        # Return the results
        return self.driver.find_elements(By.CSS_SELECTOR, "div.x-grid>div.x-panel-body>div>table>tbody>tr")
        
    def select_tab_result(self, index):
        self.driver.find_elements(By.CSS_SELECTOR, "div.x-grid>div.x-panel-body>div>table>tbody>tr")[index].click()
        self.wait_mask()
    
    def click_bottom_tab(self, label):
        ''' Clicks on the bottom tabs, if the user has the option. Not available for all users '''
        // Never click on the iframe
        self.find_element(By.XPATH, "//div[contains(@class, 'x-tab-bar-bottom']//a[text()='" + label + "']").click()
        self.wait_mask()
        
    def fill_input(self, label, value, index=0):
        input = self.driver.find_elements(By.XPATH, "//label[text()='"  + label + "']/parent::td/following-sibling::td//input")[index]
        input.clear()
        time.sleep(0.5)
        input.send_keys(value)
        time.sleep(0.5)
        
    def fill_textarea(self, label, value):
        input = self.find_element(By.XPATH, "//label[text()='"  + label + "']/parent::td/following-sibling::td//textarea")
        input.clear()
        time.sleep(0.5)
        input.send_keys(value)
        time.sleep(0.5)
                
    def find_element(self, by, expression):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, expression))
        )
        return self.driver.find_element(by, expression)