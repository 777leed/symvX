from Utils3 import receive_notification, send_message, schedule_reminder
import threading

users = [
    {'username':'Mouad',
     'number':'212632550193@c.us'
    },
    {'username':'Leed',
     'number':'212672916435@c.us'
    }
]

def main():
    t = threading.Thread(target=schedule_reminder)
    t.start()
    for user in users:
        username = user["username"]
        send_message(user["number"], f"Hey {username} !🎶")
    while True:
        receive_notification()
        

print("Symphony is Awake...")
main()
