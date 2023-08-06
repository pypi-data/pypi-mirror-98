import os
from dotenv import load_dotenv

BASEDIR=os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR,'.env'))


# Add your Secrets here

DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")