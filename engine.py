import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from input_details import *
import time
import random
# import csv
import pandas as pd
import logging


def input_values(ele, value):
    ele.click()
    ele.send_keys(Keys.CONTROL,'a')
    ele.send_keys(value)

def random_time(start, end):
    return random.randint(start,end)
def sign_in(driver,username, password):
    delay=5
    try:
        driver.find_element_by_xpath('/html/body/nav/a[3]').click()
        time.sleep(random_time(3,5))

        username_ele = driver.find_element_by_id('username')
        pass_ele = driver.find_element_by_id('password')


        input_values(username_ele,username)
        logging.info('Login Username Entered.')
        input_values(pass_ele, password)
        logging.info('Login Password Entered.')

        submit_button = driver.find_element_by_class_name('login__form_action_container')
        submit_button.click()

        logging.info('Submitted Login information to Linkedin Server.')


        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        logging.info('Login Successful.')

    except Exception as e:
        print(e)
        logging.info(f'Login failed due to following exception: {e}')
        driver.close()

def open_all_emp_page(driver):
    see_all_emp_ele_list2 = driver.find_elements_by_class_name("link-without-visited-state")

    for ele in see_all_emp_ele_list2:
        val = ele.get_attribute('data-control-name')
        if val == 'topcard_see_all_employees':
            req_ele = ele
        else:
            continue

    req_ele.click()
    time.sleep(random_time(0,3))

def get_username(profile_url):
    sub_str = 'https://www.linkedin.com/in/'
    if sub_str in profile_url:
        username = profile_url.replace(sub_str,'')
        return (username.strip('/'))
    else:
        return None

def parse_person_data(person_ele):

    name = get_text_val(person_ele,'actor-name')
    role = get_text_val(person_ele, 'subline-level-1')
    location = get_text_val(person_ele,'subline-level-2')
    profile_link_ele = find_sub_ele_val(person_ele, 'search-result__result-link')
    if profile_link_ele==None:
        profile_link_text=None
    else:
        profile_link_text = profile_link_ele.get_attribute('href')

    username=get_username(profile_link_ele.get_attribute('href'))

    return [name, role, location,username,profile_link_text]

def find_sub_ele_val(ele,name_of_ele):
    try:
        sub_ele = ele.find_element_by_class_name(name_of_ele)
        return sub_ele
    except Exception as e:
        logging.info(f'Failed to find element {name_of_ele} for {ele}: {e}.')
        return None

def get_text_val(ele, name_of_ele):
    return_ele = find_sub_ele_val(ele, name_of_ele)
    if return_ele == None:
        return None
    else:
        return (return_ele.text)


