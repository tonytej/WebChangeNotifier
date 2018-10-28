# -*- coding: utf-8 -*-
import time
import requests
import requests_toolbelt.adapters.appengine
import smtplib
from config import *
from datetime import datetime
from flask import Flask
from slackclient import SlackClient
import logging
import os
import cloudstorage as gcs
import webapp2
import urllib
from bs4 import BeautifulSoup
from google.appengine.api import app_identity
app = Flask(__name__)
requests_toolbelt.adapters.appengine.monkeypatch()

url = ["https://www.walmart.com/ip/Funko-POP-Games-Fortnite-S1-Crackshot/343459071"]
wait_time = 1

def slack_message(message, channel):
    token = ''
    sc = SlackClient(token)
    sc.api_call('chat.postMessage', channel=channel, 
                text=message, username='My Sweet Bot',
                icon_emoji=':robot_face:')

def send_email(user, pwd, recipient): #snippet courtesy of david / email sending function
    SUBJECT             = 'SITE UPDATED' #message subject
    body                = 'CHANGE AT ' + str(url) #message body
    gmail_user = userz
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

def create_file(self, filename):
  gcs_file = gcs.open(filename,
                      'w',
                      content_type='text/plain',
                      options={'x-goog-meta-foo': 'foo',
                               'x-goog-meta-bar': 'bar'},
                      retry_params=write_retry_params)
  gcs_file.write('abcde\n')
  gcs_file.write('f'*1024*4 + '\n')
  gcs_file.close()
  self.tmp_filenames_to_clean_up.append(filename)

def read_file(self, filename):

  gcs_file = gcs.open(filename)
  contents = gcs_file.read()
  gcs_file.close()
  self.response.write(contents)

@app.route('/')
def run():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    for i in range(len(url)): 
        response = requests.get(url[i], headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        lst = soup.findAll("span", {"display-block-xs font-bold"})
        if len(lst) == 1:
            #out of stock
            return 'Still out of stock', 200
        else:
            #in stock
            slack_message("Item in stock. " + url[i], "CDN9NKVU5")
            return 'In stock, sent slack message', 200
            


        '''
    bucket_name = os.environ.get('BUCKET_NAME', 'swxcs-220501.appspot.com')
    c = requests.Session()
    page1 = []
    try:
        for i in range(len(url)):
            gcs_file = gcs.open('/'+bucket_name + '/' + urllib.quote_plus(url[i]) + '.txt')
            content = gcs_file.read()
            page1.append(content)
            gcs_file.close()
    except Exception, e:
        for i in range(len(url)):
            gcs_file = gcs.open('/'+bucket_name + '/' + urllib.quote_plus(url[i]) + '.txt',
                      'w',
                      content_type='text/plain')
            gcs_file.write(c.get(url[i]).content)
            gcs_file.close()
        return 'New website detected.'

    #print page1[0]
    page2 = []
    for e in url:
        page2.append(c.get(e).content)

    for i in range(len(page1)):
        if page1[i] == page2[i]:
            #print '[-]No Change Detected on ' +str(url[i])+ "\n" +str(datetime.now())
            gcs_file = gcs.open('/'+bucket_name + '/' + urllib.quote_plus(url[i]) + '.txt',
                          'w',
                          content_type='text/plain')
            gcs_file.write(c.get(url[i]).content)
            gcs_file.close()
            print '[-]No Change Detected on ' +str(url[i])+ "\n" +str(datetime.now())
            
        else:
            #status_string = 'Change Detected at ' +str(url[i])+ "\n" +str(datetime.now())
            #message = status_string
            #print "[+]"+status_string
            #slack_message("CHANGE DETECTED AT " + url[i], "CDN9NKVU5")
            gcs_file = gcs.open('/'+bucket_name + '/' + urllib.quote_plus(url[i]) + '.txt',
                              'w',
                              content_type='text/plain')
            gcs_file.write(c.get(url[i]).content)
            gcs_file.close()
            print 'Change Detected at ' +str(url[i])+ "\n" +str(datetime.now())

    return 'OK', 200
    '''