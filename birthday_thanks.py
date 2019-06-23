from selenium import webdriver

import csv
name=[]
#opening the list of csv file and appending to name 
with open('Friends_hai.csv') as csvfile:
    readCSV=csv.reader(csvfile,delimiter=',')
    print(readCSV)
    for row in readCSV:
        name.append(row[0])

#add the path to chromedriver 
driver = webdriver.Chrome('chromedriver.exe')#here
driver.get('https://web.whatsapp.com/')

#input the grp name here
string = input('enter anything after scannig qr code')
input("enter anything")
user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(string))
user.click()

#plz check find_element_by_xpath it changes most of the time
msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

j=0
for i in name:
    #here we say thank you and the name of ur friend
    msg_box.send_keys("thank you",name[j])
    #this class name is the send button
    button = driver.find_element_by_class_name('_35EW6')
    button.click()
    j+=1
