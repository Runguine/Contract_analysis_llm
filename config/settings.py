import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URL = os.getenv("DB_URL")
    ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    ALCHEMY_ENDPOINT = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"
    
    APIKEY = os.getenv("APIKEY")
    BASEURL = os.getenv("BASEURL")
    PROMPT = os.getenv("PROMPT")
    MODELNAME = os.getenv("MODELNAME")

settings = Settings()