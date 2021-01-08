# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:32:30 2020

@author: user
"""
import tkinter as tk
import time
import threading
import plyer
import datetime
import sys



import requests
import bs4 


def get_html_data(url):
    data = requests.get(url)
    return data

def get_corona_detail_of_india():
    url = "https://www.worldometers.info/coronavirus/country/india/"
    html_data = get_html_data(url)            #here html_data are in response type 
    #print(html_data.text)                 # but here we print the  text type of the html_data
    bs = bs4.BeautifulSoup(html_data.text,"html.parser")       
    #  print(bs.prettify())    # this will print all the html datas in text form in a pretty & beautiful order
    info_div = bs.find("div",class_ ="content-inner").find_all("div",id ="maincounter-wrap")
    all_details = ""
    for block in info_div:
        info = block.find("div",class_ = "maincounter-number").find("span").get_text()         #here we fatch the total count of cases
        txt=block.find("h1").get_text()      #here we fatch the corresponding datas
        #print(text+"  :  "+ count )
        all_details = all_details + txt + "   "+ info+"\n"
    return all_details

#creating GUI for our apk

def notification(stop):
    while True:
        plyer.notification.notify(
            title = "COVID-19 LIVE STATUS of INDIA",
            message = get_corona_detail_of_india(),
            timeout=20,
            app_icon="./file/covid_19.ico"
        )
        if stop(): 
                break
        time.sleep(60)
        

def clock(stop): 
    while True:
        now = datetime.datetime.now()
        string_time = now.strftime('Date :     %d-%m-%Y \t\t Time :     %H:%M:%S  %p')
       # string_date = now.strftime("%d-%m-%Y")
        lbl_time["text"]=string_time
        #lbl_time.after(1000, clock) 
        if stop(): 
            break



def refresh():
    newdata=get_corona_detail_of_india()
    print(" nice")
    mainlable["text"]=newdata




root= tk.Tk()
root.geometry( "500x450")
root.iconbitmap("./file/covid_19.ico")
root.title("COVID-19 LIVE DATA TRACKER")
root.config(bg="pink")

banner = tk.PhotoImage(file="./file/covs.png")
bannerlable= tk.Label(root,image = banner,bg="pink")
bannerlable.pack()

IND=tk.Label(root,text="COVID_19 LIVE STATUS OF INDIA",font=("Algerian",20,"bold"),bg="pink",fg="brown")
IND.pack()


f=("poppins",20,'bold')

l=("poppins",10)
lbl_time=tk.Label(root,text="",font=l,fg="purple",bg="pink")
lbl_time.pack(anchor="center")


mainlable = tk.Label(root,text=get_corona_detail_of_india(),font=f,bg="pink",fg="blue")
mainlable.pack(pady ="20")



rebtn = tk.Button(root,text="REFRESH" ,bg="red" ,fg="white",command = refresh)
rebtn.pack(pady="15")

stop_threads = False
stop_threads_1 = False

#create a new thread for clock
th2 = threading.Thread(target=clock,args =(lambda : stop_threads_1, ))
th2.isDaemon()
th2.setDaemon(True)
th2.start()


#create a new thread for notification

th1 = threading.Thread(target=notification,args =(lambda : stop_threads, ))
th1.isDaemon()
th1.setDaemon(True)
th1.start()


root.mainloop()

#print(th1.isAlive())
stop_threads = True
stop_threads_1 = True
th1.join() 
#th2.join()
#print('thread killed')

#print(th1.isAlive())
#print("gggggggggggggggggggggggggggggggggggggggggggg")   

sys.exit()






