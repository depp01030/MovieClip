# -*- coding: utf-8 -*-
# app/config.py
import os
from dotenv import load_dotenv



#%%
load_dotenv()

ENTRANCEPOINT_URL = os.getenv("ENTRANCEPOINT_URL", "https://httpbin.org/forms/post")