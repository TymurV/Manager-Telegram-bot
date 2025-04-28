import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
DATABASE = os.getenv('DATABASE')
images = os.getenv('images')
chat_id = os.getenv('chat_id')