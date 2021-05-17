
#Import Libraries
import requests
import json
import time
import smtplib
import ssl


#Define Constants


PINCODE = "" #Example 600040
DISTRICT_CODE = 0
MY_EMAIL = "" #From this mail id, the alerts will be sent
MY_PASSWORD = "" #Enter the email id's password
RECIPIENT_EMAILS= [""]
SMTP_SERVER="smtp.gmail.com"
port = 465  # For SSL

today = time.strftime("%d/%m/%Y")
MSG_SUBJECT = f"Subject: {today}'s Alert'!! \n\n "

#Derive the date and url
#url source is Cowin API - https://apisetu.gov.in/public/api/cowin

url_by_pin = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"
url_by_state = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DISTRICT_CODE}&date={today}"
context = ssl.create_default_context()

#Write a loop which checks for every 1000 seconds
while True:
    #Start a session
    with requests.session() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url_by_state, headers=headers)
        #Receive the response
        response = response.json()
        message_string=MSG_SUBJECT
        for center in response['centers']:
            for session in center['sessions']:
                #For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                    message_string +=f"Available - {session['available_capacity']} in {center['name']} on {session['date']} for the age {session['min_age_limit']} \n\n"

                    #Configure GMAIL settings
        if(message_string!=MSG_SUBJECT):
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", port,context=context) as connection:
                    connection.login(MY_EMAIL, MY_PASSWORD)
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=RECIPIENT_EMAILS, #for multiple receipients, add another email id after a comma in the list
                        msg=message_string
                    )
            except Exception as e:
                # Print any error messages to stdout
                print(e)
        time.sleep(1000)
