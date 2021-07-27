
#Import Libraries
import requests
import json
import time
from mailjet_rest import Client
import ssl
import os
api_key = ''
api_secret = ''
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

#Define Constants
PINCODE = "770036" #Example 600040
DISTRICT_CODE = 453
MY_EMAIL = {"Email": "adildilhussain03@gmail.com", "Name": "Adil" } #From this mail id, the alerts will be sent
RECIPIENT_EMAILS= [{"Email": "adil.cs.work@gmail.com", "Name": "Adil"},{"Email": "nishadfatma25@gmail.com", "Name": "Nishad"}]


today = time.strftime("%d/%m/%Y")
MSG_SUBJECT = f"Subject: {today}'s Alert'!! \n\n "

#Derive the date and url
#url source is Cowin API - https://apisetu.gov.in/public/api/cowin

url_by_pin = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"
url_by_state = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICT_CODE}&date={today}"
context = ssl.create_default_context()

#Write a loop which checks for every 1000 seconds
    #Start a session
with requests.session() as session:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    response = session.get(url_by_state, headers=headers)
    #Receive the response
    response = response.json()
    message_string=''
    message_string1=''
    message_string2=''

    for center in response['centers']:
        for session in center['sessions']:
            #For Age not equal to 45 and capacity is above zero
            if (session['min_age_limit'] != 45) & (session['available_capacity_dose1'] > 0):
                message_string1 +=f"Available - <b>{session['available_capacity_dose1']}<b> dose 1 in <b>{center['name']}<b> on {session['date']} for the age {session['min_age_limit']} <br><br>"
            if (session['min_age_limit'] != 45) & (session['available_capacity_dose2'] > 0):
                message_string2 +=f"Available - {session['available_capacity_dose2']} dose 2 in {center['name']} on {session['date']} for the age {session['min_age_limit']} <br><br>"
    if message_string1:
        message_string += '''<h1> Dose 1 </h1> <br>''' + message_string1
    else:
         message_string +=  '<h1> No Dose 1 available </h1> <br>'

    if message_string2:
        message_string += '''<br><h1> Dose 2 </h1> <br>''' + message_string2
    else:
         message_string =  '<h1> No Dose 2 available </h1> <br>'
    if(message_string!=''):
        email = {
            'subject': 'Cowin Alert',
            'html': message_string,
            'text': message_string,
            'from': MY_EMAIL,
            'to': RECIPIENT_EMAILS,
        }
        data = {
            'Messages': [
                {
                "From": MY_EMAIL,
                "To": RECIPIENT_EMAILS,
                "Subject": MSG_SUBJECT,
                "TextPart": message_string,
                "HTMLPart": message_string,
                "CustomID": "AppGettingStartedTest"
                }
            ]
        }
        try:
            result = mailjet.send.create(data=data)
            print(result.status_code)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
