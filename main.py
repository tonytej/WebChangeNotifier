# -*- coding: utf-8 -*-
import time
import requests
import requests_toolbelt.adapters.appengine
import smtplib
from config import *
from datetime import datetime
from flask import Flask
from slackclient import SlackClient
app = Flask(__name__)
requests_toolbelt.adapters.appengine.monkeypatch()

url = ["https://tonytej.github.io/"]
wait_time = 1

def slack_message(message, channel):
    token = 'xoxp-465530631862-463393169456-465184222199-9e624060c31027aee867be7969dcf7ac'
    sc = SlackClient(token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='My Sweet Bot',
                icon_emoji=':robot_face:')

def send_email(user, pwd, recipient): #snippet courtesy of david / email sending function
    SUBJECT             = 'SITE UPDATED' #message subject
    body                = 'CHANGE AT ' + str(url) #message body
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 465) #start smtp server on port 587
        print '1'
        server.ehlo()
        print '2'
        server.starttls()
        print '3'
        server.login(gmail_user, gmail_pwd) #login to gmail server
        print '4'
        server.sendmail(FROM, TO, message) #actually perform sending of mail
        print '5'
        server.close() #end server
        print '6'
        print '[+]Successfully sent email notification' #alert user mail was sent
    except Exception, e: #else tell user it failed and why (exception e)
        print "[-]Failed to send notification email, " +str(e)

@app.route('/')
def run():
    print "[+]Starting up monitor on "
    for e in url:
        print e + " "
    with requests.Session() as c:
        try:
            page1 = []
            for e in url:
                page1.append(c.get(e))
        except Exception, e:
            print "[-]Error Encountered during initial page retrieval: " +str(e)
        while True:
            time.sleep(wait_time)
            try:
                page2 = []
                for e in url:
                    page2.append(c.get(e))
            except Exception, e:
                print "[+]Error Encountered during comparison page retrieval: " + str(e)
            for i in range(len(page1)):
                if page1[i].content == page2[i].content: #if else statement to check if content of page remained same
                    print '[-]No Change Detected on ' +str(url[i])+ "\n" +str(datetime.now())
                else:
                    status_string = 'Change Detected at ' +str(url[i])+ "\n" +str(datetime.now())
                    message = status_string
                    print "[+]"+status_string
                    #send_email(user, pwd, recipient) #send notification email
                    slack_message("CHANGE DETECTED AT " + url[i], "CDN9NKVU5")
            
                    print '\n[+]Retrieving new base page and restarting\n'
                    run()
