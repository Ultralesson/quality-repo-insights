from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
HUGGINGFACE_HUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
