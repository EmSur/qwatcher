'''
Created on 6 Apr 2015

@author: Michal Surowiec
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from datetime import datetime, date
from time import sleep
from getpass import getpass
from sys import exit, exc_info

class ServiceCloud():
     
    
    def __init__(self, scurl = 'https://login.salesforce.com', update_freq = 20):
        '''prepares the actual landing/logon page for SC'''
        self.isSConline = False # flag - is the user logged into SC?
        self.browser = None # the actual browser window in which the app is being render
        self.update_freq = 20  # how often the update loop is being run     
        
        print('Launching browser...')
        self.browser = webdriver.Chrome(service_args=["--verbose", "--log-path=qc1.log"])
        self.browser.get('https://login.salesforce.com')

        
        
    def login(self, creds):
        print('Logging into SC...')
        login = self.browser.find_element(By.XPATH, "//input[@type='email']")
        login.send_keys(creds[0])
        passw = self.browser.find_element(By.XPATH, "//input[@type='password']")
        passw.send_keys(creds[1])
        login_butt = self.browser.find_element(By.XPATH, "//button[@id='Login']")
        login_butt.click()
        sleep(15)
        try:
            print('Displaying HD Queue only...\n')
            self.browser.get("https://na2.salesforce.com/apex/MyQueueCases")
        except WebDriverException:
            pass
        self.isSConline = True
        
        
    def logoff(self):
        # TODO to be implemented
        pass
    
    
    def main_loop(self):
        while True:
            sleep(self.update_freq)
            
            # entering the main loop first thing to check is whether it is workinghours
            # if we have working hours we go on with our job:
            if self._isWorkhours(datetime.now()):    
                # checking if we are still online
                if self.isSConline == False:
                    self.login(creds)
                self.refresh()
            # if we are outside of working hours we calculate how long we hall put the algorithm to sleep
            # until the next loop is started
            else:
                # TODO implement calculating algorithm 
                sleep(self.update_freq)
                
            
    
    def refresh(self):
        ## this is actually the point where we check the status of the queue and extract neccessary 
        # information for further work
        print('last refresh on {0}'.format(datetime.now()))
        #refresh_button = browser.find_element_by_xpath("//input[@value='Refresh']")
        #refresh_button.click()
        self.browser.refresh()
        
    
    # def get_frequency():
    #     freq = input('Please type in the refresh frequency in seconds or hit [Enter] for the default 60 seconds interval:')
    #     if freq == '':
    #         freq = 20
    #     print ('\nRefresh frequency set to {0} sec'.format(freq))
    #     return freq
    
    
    def _isWorkhours(self, dt):
        ''' checks if the loop should proceed with checking whether status of the q
        if the datetime is in the range of the working weekdays and woeking hours of
        the q than the fynction returns 'True'
        '''
        if dt.isoweekday() == 6 or dt.isoweekday() == 7:
            return False
        if dt.hour > 18 and dt.hour < 8:
            return False
        else:
            return True


def get_login():
    login = raw_input('Please type in your username [name.lastname] : ')
    if login == '':
        login = 'michal.surowiec'
    login += '@thomsonreuters.com'
    password= getpass('Please type in your SC password: ')
    return login, password


if __name__ == "__main__":
    try:
        creds = get_login()
        sc = ServiceCloud()
        sc.login(creds)
        sc.main_loop() #starting to iterate over the main loop
        
    except EOFError:
        pass
    
    # except WebDriverException, e:
    #     print('chromedriver encountered and issue with SC has been closed. Exiting QWatcher...')
    #     print exc_info()[0]
        
    finally:
        sleep(5)
        exit(1)

    
    



# start_loop()

