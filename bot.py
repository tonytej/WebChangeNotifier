# -*- coding: utf-8 -*-
import time
import requests
import smtplib
from config import *
from datetime import datetime

url = ["https://tonytej.github.io/"]
wait_time = 1
user = "antonytej@gmail.com"
pwd = "lysamjdltnnsckid"
recipient = "antonytej@gmail.com"



def send_email(user, pwd, recipient, site): #snippet courtesy of david / email sending function
    SUBJECT             = 'SITE UPDATED' #message subject
    body                = 'CHANGE AT ' + str(site) #message body
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    TEXT = "Streetwear x Comp Sci fucbois detected a change at " + str(site)
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #start smtp server on port 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd) #login to gmail server
        server.sendmail(FROM, TO, message) #actually perform sending of mail
        server.close() #end server
        print '[+]Successfully sent email notification' #alert user mail was sent
    except Exception, e: #else tell user it failed and why (exception e)
        print "[-]Failed to send notification email, " +str(e)

def main():
    print "[+]Starting up monitor on "
    for e in url:
        print e + " "
    
    with requests.Session() as c:
        try:
            page1 = []
            for e in url:
                page1.append(c.get(e))
            #page1 = c.get(url) #base page that will be compared against
        except Exception, e:
            print "[-]Error Encountered during initial page retrieval: " + str(e)
        while True:
            time.sleep(wait_time)
            try:
                page2 = []
                for e in url:
                    page2.append(c.get(e))
                #page2 = c.get(url) #page to be compared against page1 / the base page
            except Exception, e:
                print "[+]Error Encountered during comparison page retrieval: " + str(e)

            for i in range(len(page1)):
                if page1[i].content == page2[i].content: #if else statement to check if content of page remained same
                    print '[-]No Change Detected on ' +str(url[i])+ "\n" +str(datetime.now())
                else:
                    status_string = 'Change Detected at ' +str(url[i])+ "\n" +str(datetime.now())
                    message = status_string
                    print "[+]"+status_string
                    send_email(user, pwd, recipient, url[i]) #send notification email
                    
            
                    print '\n[+]Retrieving new base page and restarting\n'
                    main()

if __name__ == "__main__":
    main()