import os,time,csv,clipboard,sys,inquirer
from selenium import webdriver
from modules.driveHelp import DriveHelp
from modules.driveHelp import GREATERTHANFOLLOWERS
from modules.driveHelp import docsMessage
from selenium.webdriver.common.keys import Keys

todo = input("hey press ENTER to run daily msg else press 'w' weekly msgs " )
doc = docsMessage()
today="15/06/2020"
member=doc.getwholedata()
driver=None

# print(member)
# functions
def getready():
    global driver 
    driver = webdriver.Chrome('chromedriver.exe')#here
    driver.get('https://web.whatsapp.com/')
    # wait till we get the access to search bar
    print("waiting for u to scan QR code ")
    while(doc.check_exists_by_xpath(driver,'//*[@id="side"]/div[1]/div/label/div/div[2]')):
        time.sleep(3)
    print("-"*20,"important log","-"*20)




# weeekly messages script
if todo =="w":
    membername=[m['Name'] for m in member if m['send']=='TRUE']
    membername=[i for i in membername if i != '']
    print("sending messages to ",membername)
    weekmsg=doc.getWeekMessage()
    if membername !=None:
        getready()
        for i in membername:
            # select search bar 
            search=driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
            search.click()
            # select search bar

            # enter name of user
            search.send_keys(i)
            search.send_keys(Keys.ENTER)
            #  enter name of user           
            try:
                # get the name of that user page
                titlename=driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text.lower()
                # check if we are in that user page
                if titlename == i.lower():
                   
                    msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

                    msg=weekmsg

                    clipboard.copy(msg)

                    time.sleep(0.1)

                    msg_box.send_keys(Keys.CONTROL, 'v')
                    msg_box.send_keys(Keys.ENTER)
                    print(f"Successfully sended message to {i}")
                else:
                    print(f"{i} can't find on whatsapp")
            except Exception as e:
                print(f"{i} whatsapp error ")


            # first clear search bar for every user
            search.send_keys(Keys.CONTROL,'a',Keys.BACKSPACE)
            # first clear search bar for every user

        print("-"*20,"my work is done master","-"*20)
        input()
    else:
        input("users are not selected")
        sys.exit()
    sys.exit()








getready()
noramlmsg=doc.getnormalmessage()
member=[i for i in member if i["Name"]!='']
for i in member:
    # select search bar 
    search=driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    search.click()
    # select search bar 

    if today in i and i[today]!="" and type(i[today])==int:
        if doc.checkingfollow(i[today]):      #check for followers
            
            # enter name of user
            search.send_keys(i["Name"])
            search.send_keys(Keys.ENTER)
            #  enter name of user
            try:
                # get the name of that user page
                titlename=driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text.lower()
                # check if we are in that user page
                if titlename == i["Name"].lower():

                    msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

                    msg =doc.replaceText(noramlmsg,i["Name"],today,str(i[today]))

                    clipboard.copy(msg)

                    time.sleep(0.1)

                    msg_box.send_keys(Keys.CONTROL, 'v')
                    msg_box.send_keys(Keys.ENTER)
                    print(f"Successfully sended message to {i['Name']}")
                else:
                    print(f"{i['Name']} can't find on whatsapp")
            except Exception as e:
                print(f"{i['Name']} can't find on whatsapp error {e}")
        else:
            print(f"{i['Name']} has followers {i[today]} <= {GREATERTHANFOLLOWERS}")
        
    # first clear search bar for every user
    search.send_keys(Keys.CONTROL,'a',Keys.BACKSPACE)
    # first clear search bar for every user
    




print("-"*20,"hey my work is done master","-"*20)
input()