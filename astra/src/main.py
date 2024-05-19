from dotenv import load_dotenv
from utils.client import AstraNet
import discord

load_dotenv()
AstraNet(command_prefix=">", intents=discord.Intents.all()).setup()
