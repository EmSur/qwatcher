'''
Created on 6 Apr 2015

@author: Michal Surowiec
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from datetime import datetime
from time import sleep
from getpass import getpass
from sys import exit, exc_info


def start_loop(browser, freq=20):
    while True:
        sleep(freq)
        refresh(browser)
        

def refresh(browser):
    print('last refresh on {0}'.format(datetime.now()))
    #refresh_button = browser.find_element_by_xpath("//input[@value='Refresh']")
    #refresh_button.click()
    browser.refresh()
    

def get_login():
    login = raw_input('Please type in your username [name.lastname] : ')
    if login == '':
        login = 'michal.surowiec'
    login += '@thomsonreuters.com'
    password= getpass('Please type in your SC password: ')
    return login, password

# def get_frequency():
#     freq = input('Please type in the refresh frequency in seconds or hit [Enter] for the default 60 seconds interval:')
#     if freq == '':
#         freq = 20
#     print ('\nRefresh frequency set to {0} sec'.format(freq))
#     return freq


def loginSC(creds):
    print('Launching browser...')
    browser = webdriver.Chrome(service_args=["--verbose", "--log-path=qc1.log"])
    print('Logging into SC...')
    browser.get('https://login.salesforce.com')
    login = browser.find_element(By.XPATH, "//input[@type='email']")
    login.send_keys(creds[0])
    passw = browser.find_element(By.XPATH, "//input[@type='password']")
    passw.send_keys(creds[1])
    login_butt = browser.find_element(By.XPATH, "//button[@id='Login']")
    login_butt.click()
    sleep(15)
    try:
        print('Displaying HD Queue only...\n')
        browser.get(browser.get("https://na2.salesforce.com/apex/MyQueueCases"))
    except WebDriverException:
        pass
    return browser 


try:
    
    creds = get_login()
    sc = loginSC(creds)
    start_loop(sc, 20)
    
except EOFError:
    pass

# except WebDriverException, e:
#     print('chromedriver encountered and issue with SC has been closed. Exiting QWatcher...')
#     print exc_info()[0]
    
finally:
    sleep(5)
    exit(1)

    
    



# start_loop()

