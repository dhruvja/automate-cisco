import subprocess
from selenium import webdriver
import time
from datetime import datetime
import schedule
import pyttsx3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver import ActionChains
# driver code
  
# create object and assign voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
  
# changing index changes voices but ony
# 0 and 1 are working here
engine.setProperty('voice', voices[0].id)
engine.runAndWait()
print("")
print("")
print("Let's Create a bot to attend meetings for me")
pyttsx3.speak("Let's Create a bot to attend meetings for me")
i = 0
browser = webdriver.Safari()
browser.maximize_window()
def automate(i,browser):
    if i==0:
        browser.get('https://sses.webex.com/meet/tc-1')
        print("Got into https://sses.webex.com/meet/tc-1")
    if i==-1:
        browser.get('https://sses.webex.com/sses/j.php?MTID=m378f1ced361dead27b31af0b04dab2e2')
        print("Got into https://sses.webex.com/sses/j.php?MTID=m378f1ced361dead27b31af0b04dab2e2")
        #browser.get('https://sses.webex.com/sses/j.php?MTID=md013bbe77ec46f52b3777d407a2011d1')
    try:
        obj = browser.switch_to.alert
        message=obj.text
        print ("Alert shows following message: "+ message )

        time.sleep(2)

        obj.dismiss()
        pyttsx3.speak("Dismissed the alert box")
        time.sleep(5)
        button = browser.find_elements_by_tag_name('a')
        print("Buttons on start screens are " + str(len(button)))
        button[3].click()
    except:
        time.sleep(10)
        button = browser.find_elements_by_tag_name('a')
        print("Buttons on start screens are " + str(len(button)))
        button[2].click()
    #finds the elements and clicks to open it from the browser
    

    pyttsx3.speak("Joining the meeting from the browser")

    time.sleep(10)
    cred = 0
    #enter the credentials to login 
    while True:
        try:
            print("Entered in credentials block")
            browser.switch_to_frame("thinIframe")
            if i == 0 or i == -1:
                elements = browser.find_elements_by_xpath("//input[@type='text']")
                elements[0].send_keys('DHRUV D JAIN')
                elements[1].send_keys('dhruvs@iamsizzling.com')
                time.sleep(5)
            pyttsx3.speak("Credentials Entered successfully")
            browser.find_element_by_id('guest_next-btn').click()
            browser.switch_to_default_content()
            time.sleep(5)
            break
        except:
            time.sleep(5)
            browser.switch_to_default_content()
            cred = cred +1
            print("Skipped Credentials block due to some error, doing it " + str(cred) + " time")
            if cred>20:
                browser.refresh()
                automate(-1,browser)
    #Choose the settings and then join the meeting
    browser.switch_to_frame("thinIframe")
    muteelement = browser.find_elements_by_xpath("//button[@data-doi='AUDIO:MUTE_SELF:MEETSIMPLE_INTERSTITIAL']")
    if len(muteelement) > 0 :
        mute = browser.find_elements_by_xpath("//button[@data-doi='AUDIO:MUTE_SELF:MEETSIMPLE_INTERSTITIAL']")
        if len(mute) > 0 :
            mute[0].click()
        time.sleep(2)
        videostop = browser.find_elements_by_xpath("//button[@data-doi='VIDEO:STOP_VIDEO:MEETSIMPLE_INTERSTITIAL']")
        if len(videostop) > 0 :
            videostop[0].click()
        browser.find_element_by_id('interstitial_join_btn').click()
        pyttsx3.speak("Meeting Joined Successfully with audio and video muted")
        s = 0
        browser.switch_to_default_content()
        time.sleep(10) 
        browser.switch_to_frame("thinIframe")
        m = 0
        while True:
            findbutton = browser.find_elements_by_xpath("//button[@title='Participants']")
            print("Participant button is " + str(len(findbutton)))
            if m>10:
                pyttsx3.speak("The host has not joined the meeting. Leaving the meeting and joining again")    
                time.sleep(3)
                browser.close()
                time.sleep(2)
                browser = webdriver.Safari()
                browser.maximize_window()
                if i==-1:
                    automate(0,browser)   
                else:
                    automate(-1,browser)            
            if len(findbutton) > 0 :
                try:
                    m += 1
                    findbutton[0].click()
                    break
                except:
                    if m == 1:
                        pyttsx3.speak("The host has not joined the meeting. Waiting for host for 100 seconds")
                    time.sleep(5)
        j = 0
        k = 0
        while True:
            participants = browser.find_elements_by_xpath("//span[contains(@title, 'Participants')]")
            if len(participants) > 0:
                participanttext = participants[0].text
            else:
                try:
                    obj = browser.switch_to.alert
                    message=obj.text
                    print ("Alert shows following message: "+ message )
                    time.sleep(2)
                    obj.accept()
                    print("The meeting has ended, so closing the browser")
                    pyttsx3.speak("The meeting has ended, so closing the browser")
                    browser.close()
                    time.sleep(2)
                    browser = webdriver.Safari()
                    browser.maximize_window()
                    if i==-1:
                        automate(0,browser)
                    else:
                        automate(-1,browser)
                except:
                    time.sleep(1)
            browser.switch_to_default_content()
            start = participanttext.find("(")
            end = participanttext.find(")")
            start = start + 1
            num = int(participanttext[start:end])
            print(" Participants are " + str(num))
            if k%50 == 0:
                pyttsx3.speak("Number of Participants are " + str(num))
            if s == 0:
                time.sleep(2)
            s = s + 1
            if num<20 and j==0:
                pyttsx3.speak("Participants are low, let's wait for 30 seconds before leaving")
            elif num<20 and j == 1 or num ==0:
                pyttsx3.speak("Participants are still low, leaving the meeting in 5 seconds")
                browser.switch_to_frame("thinIframe")
                close = browser.find_elements_by_xpath("//button[@title='Close']")
                if len(close) > 0:
                    try :
                        close[0].click()
                    except:
                        pyttsx3.speak("Close button couldnt be clicked")
                        pyttsx3.speak("I think the class has ended, so i am closing the browser")
                        time.sleep(3)
                        browser.close()
                        time.sleep(2)
                        browser = webdriver.Safari()
                        browser.maximize_window()
                        if i==-1:
                            automate(0,browser)
                        else:
                            automate(-1,browser)
                    pyttsx3.speak("Close button is clicked")
                    leave = browser.find_element_by_xpath("//button[@data-doi='MEETING:LEAVE_MEETING:MENU_LEAVE']")
                    if len(leave) >0:
                        leave[0].click()
                        pyttsx3.speak("Meeting Left Successfully, closing the browser in 5 seconds")
                        time.sleep(5)
                        browser.close()
                        break
                    else:
                        pyttsx3.speak("Leave meeting button couldnt be clicked due to some crappy error")
                else:
                    pyttsx3.speak("Close button couldnt be clicked due to some crappy error")
            if num < 20:
                j = j+1
            time.sleep(3)
            k = k +1
            browser.switch_to_frame("thinIframe")
    else:
        if i==0:
            pyttsx3.speak("The meeting has not started yet, refreshing page every 300 seconds")
        else:
            pyttsx3.speak("Refreshing the page again in 300 seconds")
        if i >= 3000:
            pyttsx3.speak("No response from the server, so the meeting might be canceled")
            time.sleep(2)
            pyttsx3.speak("Clicking exit")
            browser.find_element_by_tag_name("button").click()
            time.sleep(3)
            pyttsx3.speak("Closing the browser in 2 seconds")
            time.sleep(2)
            browser.close()
        print("The page has refreshed " + str(i) + "time")
        time.sleep(3)
        browser.switch_to_default_content()
        browser.refresh()
        i = i + 3
        automate(i,browser)   



#schedule the meetings
automate(-1,browser)
"""schedule.every().tuesday.at("14:42").do(automate(0))
while True:
    schedule.run_pending()
    time.sleep(1)"""

#pipenv run python3 automatecisco.py
