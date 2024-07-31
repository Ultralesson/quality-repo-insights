from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
