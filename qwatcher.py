'''
Created on 6 Apr 2015

@author: Michal Surowiec
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from datetime import *
from getpass import getpass
import requests
from bs4 import BeautifulSoup as bs
import time



class ServiceCloud():
     
    
    def __init__(self, creds, update_freq = 3):
        '''prepares the actual landing/logon page for SC'''
        self.isSConline = False # flag - is the user logged into SC?
        self.browser = None # the actual browser window in which the app is being render
        self.update_freq = 20  # how often the update loop is being run 
        self.creds = creds
        
        self.case_queue = {} #all the current cases in the queue
        
        self.loginurl  = 'https://login.salesforce.com'
        self.logouturl = 'https://na2.salesforce.com/secur/logout.jsp'
        self.myqueueurl = "https://na2.salesforce.com/apex/MyQueueCases"
        
        print('Launching browser...')
        self.browser = webdriver.Chrome(service_args=["--verbose", "--log-path=qc1.log"])
        
          
    def login(self):
        print('Logging into SC...')
        self.browser.get(self.loginurl)
        login = self.browser.find_element(By.XPATH, "//input[@type='email']")
        login.send_keys(Keys.F11)
        print "done"
        login.send_keys(self.creds[0])
        passw = self.browser.find_element(By.XPATH, "//input[@type='password']")
        passw.send_keys(self.creds[1])
        login_butt = self.browser.find_element(By.XPATH, "//button[@id='Login']")
        login_butt.click()
        time.sleep(15)
        try:
            print('Displaying HD Queue only...\n')
            self.browser.get(self.myqueueurl)
        except WebDriverException:
            pass
        self.isSConline = True
        
        
    def logoff(self):
        print('Logging off of SC...')
        self.browser.get(self.logouturl)
        
    
    def main_loop(self):
        while True:
            time.sleep(self.update_freq)
            
            # entering the main loop first thing to check is whether it is workinghours
            # if we have working hours we go on with our job:
            print (self.isWorkhours(datetime.now()))
            if self.isWorkhours(datetime.now()):    
                # checking if we are still online
                if self.isSConline == False:
                    self.login(self.creds)
                self.refresh() # refreshing the html so that agents can see an updated view of the q
                fresh_cases = self._read_case_list()    # reading all the cases that have been displayed after refresh
                self._raise_alerts(fresh_cases)     # raising alerts on new cases in queue or breached cases
                self.case_queue = fresh_cases       # updating status of queue
            # if we are outside of working hours we calculate how long we shall put the algorithm to sleep
            # until the next loop is started
            else:
                # but first we need to logoff from SC  
                if self.isSConline == True:
                    self.logoff()
                    self.isSConline = False # because we haved logged of we need to change the flag
                # wait till next standard heartbeat
                time.sleep(self.update_freq)
                # TODO implement calculating algorithm
                    
    
    def refresh(self):
        '''refreshes the html page view '''
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
    
    
    def isWorkhours(self, dt):
        ''' checks if the loop should proceed with checking whether status of the q
        if the datetime is in the range of the working weekdays and woeking hours of
        the q than the fynction returns 'True'
        '''
#         print (dt)
#         if dt.isoweekday() == 6 or dt.isoweekday() == 7:
#             return False
#         print (dt.hour)
#         if dt.hour > 18 or dt.hour < 8:
#             return False
#         else:
#             return True
        return True
        
    def _next_heartbeat(self):
        ''' calculates how much time in seconds will need to pass between now and the 
        neraest opening of the queue (nearest working hour starting time)
        
        returns sleep_for - (int) seconds to nearest opening of the queue
        '''
        # TODO _next_heartbeat to be implemented
        now = datetime.now()
          
        
    def _read_case_list(self):
        ''' reads all cases displayed in the teams case queue
        returns - dictionary of all cases after the last update of the SC webpage
        '''
        fresh_case_queue = {}
#         case_list = self.browser.find_elements(By.XPATH, '//td//tr/td[2]')      # pulls the column with the case numbers
#         opened = self.browser.find_elements(By.XPATH, '//td//tr/td[4]')         # r[1] column with the opened date
#         responset_list = self.browser.find_elements(By.XPATH, '//td//tr/td[6]') # r[2] column with the response time
#         status_list = self.driver.find_elements(By.XPATH, '//td//tr/td[10]')    # r[3] column with the current working status
#         severity_list= self.driver.find_elements(By.XPATH, '//td//tr/td[11]')   # r[4] column with severity
#         # all above columns will be transposed and put into a dictionary of cases
#         # first w zip the columns into tuples - each tuple representing one row/case of the list)
#         allcolumns = zip(case_list, opened, responset_list, status_list, severity_list )
#         for row in allcolumns:
#             nextCase = Case(row[0]) # instantiating a case object with its case number
#             # filling out the neccessary fields       
#             nextCase.details['Date/Time Opened'] = row[1]
#             nextCase.details['Response Time'] = row[2]
#             nextCase.details['Severity'] = row[3]
#             nextCase.details['Impact'] = row[4]
#             # adding the case to the case dictionary with the case number as key
#             fresh_case_queue[row[0]] = nextCase
        return fresh_case_queue
        
#         for row in allcolumns:
#             case_number = row[0] #this is the case number
#             if case_number in self.case_queue: # checking if the case has already been listed previously
#                 # TODO need to check whether fields of case haven't changed since last heartbeat
#                 self._compare_case_fields(case_number, row)
#                 
#             else:
#                 # TODO we need to sound the alarm if the case has status 'new'
#                 ### BEEEEP
#                 # and now add the case to the case 
#                 self.case_queue[case_number] = [row[1], row[2], row[3], row[3], row[4]]
    def _raise_alerts(self, fresh_cases):
        ''' takes action by raising alerts or sending e-mails to relevant people if cases hit the queue or 
        get breached. 
        '''
#         ## TODO - finish alerts
#         for case_number in fresh_cases:
#             if case_number in self.case_queue:
#                 pass           
        pass
    
    
    def _is_severity_alert(self, case):
        ''' checks '''
        ## TODO - finish sev alert
    
    def _is_breach_alert(self, case):
        ## TODO - finish sev alert
        pass        
    
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
        sc = ServiceCloud(creds)
        if sc.isWorkhours(datetime.now()) == False:
            print ("its {0} - no working hours - exiting now".format(datetime.now()))
            exit(1)
        sc.login()
        sc.main_loop() #starting to iterate over the main loop
        
    except EOFError:
        pass
    
    # except WebDriverException, e:
    #     print('chromedriver encountered and issue with SC has been closed. Exiting QWatcher...')
    #     print exc_info()[0]
        
    finally:
        time.sleep(5)
        exit(1)

    
    



# start_loop()

