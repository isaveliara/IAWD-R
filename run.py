import threading, os
from dotenv import load_dotenv
from client.client import IAWRBot
from app.app import RunIAWRFlask

if __name__ == "__main__":
    load_dotenv()
    
    flask_thread = threading.Thread(target=RunIAWRFlask, daemon=True) #Backend API
    flask_thread.start()
    
    IAWRBot.run(os.getenv("BOT_TOKEN")) #Discord Client

