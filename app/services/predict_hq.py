import os
from dotenv import load_dotenv

#import .env
load_dotenv(os.getenv(".env"))  # print(os.getenv("PREDICT_HQ_API"))
