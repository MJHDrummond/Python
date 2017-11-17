########################################################################## 
#
# Script to monitor an apartment rental website (www.domica.nl) that will
# send an email when the number of listings has changed.
#
# Author: McGregor Drummond
# Date: 16 July 2017
#
##########################################################################

# import required modules
import requests
import time
from bs4 import BeautifulSoup
import re
import datetime
import smtplib
from email.mime.text import MIMEText

while True: # create infinite loop until manually stopped by user

    params = {'iscustom': 'true','mustbeupholstered': 'true','orderby': '3', 'pricerange.maxprice': '800', 'pricerange.minprice': '400'} # set the search criteria for the apartments, also shown below
#iscustom=true
#mustbeupholstered=true
#orderby=3
#pricerange.maxprice=800
#pricerange.minprice=400

    r = requests.get('https://www.domica.nl/woningaanbod/huur/land-nederland/apeldoorn/type-appartement', params) # create the url and make the request to the webpage

    soup = BeautifulSoup(r.text, "lxml") # convert the txt output to lxml format
    spans = soup.find_all('span', {'class' :'sys-property-count'}) # find the line containing the property count value
    lines = [span.get_text() for span in spans] # create list of all instances of sys-property-count (should only be one)
    num_properties = [int(s) for s in re.findall(r'\d+', lines[0])] # find and save the integer values in each line, value that we require should be the first integer value: num_properties[0]

    def sendmail(): # create the function to send mail when webpage is updated
        me = 'user@mail.com'
        password = 'password'
        you = ['user@mail.com','user2@mail.com']

        with open('email.txt') as fp: # email.txt contains link to webpage
            msg = MIMEText(fp.read())

        msg['Subject'] = 'Apartment listings have been updated!'
        msg['From'] = me

        s = smtplib.SMTP('smtp-mail.outlook.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(me,password)
        s.sendmail(me, you, msg.as_string())
        s.quit()

    with open('num_properties.txt') as f: # open txt file containing dated history of property counts
        last_line = f.readlines() 
        previous_value = [int(s) for s in re.findall(r'\d+', last_line[-1])] # assign the latest property count to variable
    
    if previous_value[0] != num_properties[0]: # check if new property count has changed
        print("Listings updated!")
        sendmail() # call on function to send email
        with open('num_properties.txt', 'a') as f: # update the .txt file containing property counts
            f.write('Number of properties: %s at %s.\n' % (num_properties[0], datetime.datetime.now()))
                
    else: # if no change in property count script will sleep for set time then continue
        print('No changes as of %s' % datetime.datetime.now())
        time.sleep(1800) # wait for 30 mins
