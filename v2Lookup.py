#!/usr/bin/env python3

import time
import logging
from lxml import html
from random import randint
import cfscrape


print("\n\nLookup keys @RANDOM via bitcoinlist.io!")
print("---------------------------------------")
print("---------------------------------------")

scraper = cfscrape.create_scraper()
iterating = 0
napLength = 15 # time in seconds to sleep for
iterLimits = 7 # how many API lookups till we take a Nap

from smtplib import SMTP_SSL as SMTP
from time import sleep

host        = "smtp.ymail.com" 
usrnme      = "myemail@yahoomail.com" 
pswd        = "myFancyPantsPasswording"
subject = "check this private key pls"

def send_email(from_addr, to_addr, body_text):
    """
    Send an Email
    """

    msg_body = ""
    parts = ["From: %s" % from_addr,
            "To: %s" % to_addr,
            "MIME-Version: 1.0",
            "Content-type: text/html",
            "Subject: %s" % subject,
            "",
            body_text
            , "\r\n"]
    msg_body = "\r\n".join(parts)
    server = SMTP(host, 465)
    # server.set_debuglevel(1)
    server.ehlo()
    server.login(usrnme,pswd)
    server.sendmail(from_addr, to_addr, msg_body)
    server.quit()



def generatePage():
    return randint(0,904625697166532776746648320380374280100293470930272690489102837043110636675)



def grabPks(pageNum):
    # cloudflare blocks bots...use scraper library to get around this or build your own logic to store and use a manually generated cloudflare session cookie... I don't care 😎
    # req = requests.get("https://www.bitcoinlist.io/"+str(pageNum))
    req = scraper.get("https://www.bitcoinlist.io/"+str(pageNum)).content
    if(req == b'Rate Limit Exceeded'):
        print("adjust the rate limiting because they're blocking us :(")
        manPenalty = napLength * 3
        print("manually sleeping for {} seconds".format(manPenalty))
        time.sleep(manPenalty)
        print("okay let's try again... NOW SERVING {}".format(pageNum))
        return grabPks(pageNum)
    else:
        tree = html.fromstring(req)
        pk = tree.xpath("/html/body/div[1]/div[3]/div[4]/div/div/div[2]/table/tbody/tr/td[1]/small/text()")
        resCmpress = tree.xpath("/html/body/div[1]/div[3]/div[4]/div/div/div[2]/table/tbody/tr/td[3]/small/a//text()")
        resXtend = tree.xpath("/html/body/div[1]/div[3]/div[4]/div/div/div[2]/table/tbody/tr/td[2]/small/a//text()")
        balance = tree.xpath("/html/body/div[1]/div[3]/div[4]/div/div/div[2]/table/tbody/tr/td[4]/font//text()")
        return pk, resCmpress, resXtend, balance



while True:
    muhPage = generatePage()
    if (iterating >= iterLimits):
        print("\ntaking a {0} second Nap..ZZZzzzzz".format(napLength))
        time.sleep(napLength)
        iterating = -1
    iterating +=1
    print ("\nNOW SERVING {}\n".format(muhPage))
    pkArray = grabPks(muhPage)
    for i in range(len(pkArray[0])):
        thisBalance = pkArray[3][i]
        print( "PK: {0} Addr: {1}  Balance: {2}".format(pkArray[0][i][-10:], pkArray[1][i][:7], thisBalance))
        if(thisBalance == ' 0'):
            continue
        else:
            print ("balance = " + thisBalance)
            print("We may have found something! check out Private Key {0}, for compressed Address {1}".format(pkArray[0][i], pkArray[1][i]))
            send_email("myemail@gmail.com", "myemail@gmail.com", "check out Private Key {0}, for Adress {1}, and {2}. Found a balance of {3}".format(pkArray[0][i], pkArray[1][i], pkArray[2][i], thisBalance ))
            raise SystemExit
    # print ("Ext: {0}, Stndrd {1}".format(endExt, endCmp))


''' HEY THERE PIRATE!

THIS IS A 2017... no... 2018 FACELIFT TO THE TOY APP POOR MANS MINING.
HUNT THEM 2010 ERA COINS!!!!  Currently the Script uses Directory.IO
and blockchain.info to parse (at random) the entire sha256 keylist page by page
256 different lookups per page (1 for compressesed public address one for standard.
Feel Free to checkout Line 63 IF YOU REALLY WANT TO KNOW HOW BIG THIS IS...
and impractical mind you!  This script may be your friend if you - can setup
and distribute this, like a botnet so that its scanning all the time from different
machines and ultimately pinging you on anything found.  You are literally stealing
someone else's private key - if the BTC utxo's are OLD like 2010 old you may be
able to comformably claim those - if the funds are a couple months old however,
you may need to consider returning a large portion if not all of them back to the
rightful owner.  Just like with my PK generator/checker tool this is literally for
enteratinment purposes and not designed for extended real world use.  Your IP
Address may become blocked from using this toy extensively, proceed with caution.
If you DO actually happen to find a collision (ie someone else's private key),
pat yourself on the back because that's supposed to not be possible...and maybe
send a few duckets my way: 18ZVx4i7FKYj6GYa1XgBM2ZfQdjE6nUMgt

'''
