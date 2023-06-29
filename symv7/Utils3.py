import requests
import time
import json
import openai
import schedule
import subprocess
import nltk
from datetime import datetime, time as dt_time



openai.api_key = "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"
# List of applications
applications = [
    {
        'name': 'chrome',
        'path': '"C:\Program Files\Google\Chrome\Application\chrome.exe" --profile-directory="Profile 1"',
        'description': 'This is Application 1.',
    },
    {
        'name': 'whatsapp',
        'path': 'C:/Program Files/Application2/application2.exe',
        'description': 'This is Application 2.',
    },
]
txtmsg = ""


def query_extract(text):
    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)
    # Perform POS tagging
    pos_tags = nltk.pos_tag(tokens)
    query = ''
    # Extract the query based on POS tags, excluding "send" and "give me"
    for word, tag in pos_tags:
        if tag == 'NN' or tag.startswith('VB'):
            if word.lower() not in ['send', 'give', 'me']:
                query += word + ' '
    return query.strip()

def image_engine(q):
    url = "https://joj-image-search.p.rapidapi.com/v2/"
    querystring = {f"q":{q},"hl":"en"}
    headers = {
        "X-RapidAPI-Key": "704d5c2221msh1b8993145546ac3p1ae21ajsn48ae9a8e7fae",
        "X-RapidAPI-Host": "joj-image-search.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    response_data =  response.json()
    # Retrieve the first image URL from the response
    if 'response' in response_data and 'images' in response_data['response']:
        images = response_data['response']['images']
        if images:
            image_url = images[0]['image']['url']  # Use the image URL from the response
            image_filename = 'new_img.jpg'  # Filename to save the image as
            # Download the image
            response = requests.get(image_url)
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"Image downloaded and saved as {image_filename}")
        else:
            print("No images found in the response.")
    else:
        print("Invalid response data.")

def remind_me():
    task = ""
    now = datetime.now()
    print("Sending a reminder")
    morning_start = dt_time(9, 0, 0)
    morning_end = dt_time(12, 0, 0)
    evening_end = dt_time(21, 0, 0)
    night_time = dt_time(23, 0, 0)

    if morning_start <= now.time() < dt_time(10, 0, 0):
        task = "Hey Leed did you wake up on time today? 🌅"
    elif dt_time(10, 0, 0) <= now.time() < morning_end:
        task = "It's Anki session Time. Get those falshcards done! 🃏 "
    elif evening_end <= now.time() < night_time:
        task = "It's workout session Time. Push yourself to new limits! 🏋️‍♂️"
    else:
        task = "Reminding you that you're probably the coolest person on earth!"
        
    send_message("212672916435@c.us", task)

def schedule_reminder():
    print("inside the schedule reminder")
    reminder_times = ["09:00:00", "10:00:00", "21:00:00"]
    for reminder_time in reminder_times:
        schedule.every().day.at(reminder_time).do(remind_me)
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_media(chat_id):
    idInstance = "1101829018"
    apiTokenInstance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881" 
    url = f"https://api.green-api.com/waInstance{idInstance}/sendFileByUpload/{apiTokenInstance}"
    payload = {'chatId': chat_id,
    'caption': 'Here you go!'}
    files = [
    ('file', ('new_img.jpg', open(r"C:\Users\hp\Downloads\LeedMakesStuff\symv\new_img.jpg",'rb'),'image/jpeg'))
    ]
    headers= {}
    response = requests.request("POST", url, headers = headers, data = payload, files = files)
    print(response.text.encode('utf8'))
    if response.ok:
        print("File sent successfully!")
    
    else:
        print("Failed to send the file.") 

def launch_application(application):
    try:
        subprocess.Popen(application['path'])
        print(f"Application launched: {application['name']}")
    except FileNotFoundError:
        print(f"Application not found: {application['name']}")

def turbo_categorizes(prompt,chat_id):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"to what category does the following prompt belong, answer just the categories given with no additional words : {prompt} : [launch a browser,send an image,send a song, none]"}
            ]
        )
        result = completion.choices[0].message["content"].lower().strip()
        print(result)
        if result == "none":
            return False
        elif result == "launch a browser":
            launch_application(applications[0])
            return True
        elif result == "send an image":
            q = query_extract(prompt)
            image_engine(q)
            send_media(chat_id)
            return True 
        else :
            return False

def turbo_responds(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message["content"]
    except:
        return "Overloaded, please wait a moment."



# Whatsapp GREEN API
def send_message(chat_id, message):
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881"
    url = f"https://api.green-api.com/waInstance{id_instance}/sendMessage/{api_token_instance}"
    payload = {
        "chatId": chat_id,
        "message": message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    if response.ok:
        print("Message sent successfully!")
        print("Message:", message)
    else:
        print("Failed to send the message.")


def delete_notification(id):
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881" 
    url = f"https://api.green-api.com/waInstance{id_instance}/deleteNotification/{api_token_instance}/{id}"
    response = requests.delete(url)
    result = json.loads(response.text)['result']
    if result == False:
        print("Empty Handed")
        return
    print("Cleaning...")


def receive_notification():
    global txtmsg
    id_instance = "1101829018"
    api_token_instance = "5c4dafe85d314497bc3d90876de869e488e3bb82a45d433881" 
    url = f"https://api.green-api.com/waInstance{id_instance}/receiveNotification/{api_token_instance}"
    response = requests.get(url)
    if response.status_code == 200:
        response_text = response.text
        print(response_text.encode('utf8'))
        if response_text != "null":
            response_data = json.loads(response_text)
            receipt_id = response_data.get('receiptId')
            body_data = response_data.get('body', {})
            webhook_type = body_data.get('typeWebhook')
            if webhook_type == 'incomingMessageReceived':
                message_data = body_data.get('messageData', {})
                if message_data.get('typeMessage') == 'textMessage':
                    text_message = message_data.get('textMessageData', {}).get('textMessage')
                    txtmsg = text_message.strip()
                    print(text_message)
                elif message_data.get('typeMessage') == 'extendedTextMessage':
                    text_message = message_data.get('extendedTextMessageData', {}).get('text')
                    txtmsg = text_message.strip()
                    print(text_message)
                sender_data = response_data.get('body', {}).get('senderData', {})
                sender_name = sender_data.get('senderName')
                sender_number = sender_data.get('sender')
                print("Sent by:", sender_number, ", AKA:", sender_name)
                if turbo_categorizes(txtmsg,sender_number) == True:
                    delete_notification(receipt_id)
                    return
                reply = turbo_responds(txtmsg)
                print(reply)
                send_message(sender_number, reply)
            delete_notification(receipt_id)
        else:
            print("Still Waiting...")
    else:
        print("No notification yet. Waiting...")
        time.sleep(1)
