from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from utils import Display, Logger
from .scraper import Scraper
from .adder import Adder
from .filter import Filter
import json
import os

class TelegramHandler:
    def __init__(self):
        self.client = None
        self.logger = Logger()
        
    async def initialize(self):
        """Initialize Telegram client"""
        try:
            # Load config
            if not os.path.exists('config/config.json'):
                Display.print_error("Config file not found!")
                return False
                
            with open('config/config.json') as f:
                config = json.load(f)
            
            # Create session directory if not exists
            os.makedirs('session', exist_ok=True)
            
            # Initialize client
            self.client = TelegramClient(
                'session/culix', 
                config['api_id'],
                config['api_hash']
            )
            
            await self.client.start()
            
            if not await self.client.is_user_authorized():
                phone = input("Enter phone number: ")
                await self.client.send_code_request(phone)
                code = input("Enter the code you received: ")
                try:
                    await self.client.sign_in(phone, code)
                except SessionPasswordNeededError:
                    password = input("Enter your 2FA password: ")
                    await self.client.sign_in(password=password)
            
            Display.print_success("Successfully connected to Telegram!")
            return True
            
        except Exception as e:
            Display.print_error(f"Error initializing client: {str(e)}")
            self.logger.log(f"Error in initialize: {str(e)}", "ERROR")
            return False
    
    async def scrape_members(self, group_username):
        """Scrape members from group"""
        scraper = Scraper(self.client, self.logger)
        await scraper.scrape_members(group_username)
    
    async def add_members(self, group_username, csv_file):
        """Add members to group"""
        adder = Adder(self.client, self.logger)
        await adder.add_members(group_username, csv_file)
    
    async def filter_members(self, group_username, csv_file):
        """Filter members not in group"""
        filter = Filter(self.client, self.logger)
        await filter.filter_members(csv_file, group_username)  # Parameters in correct order
    
    async def view_logs(self):
        """Display recent log contents (last 100 lines)"""
        try:
            with open("logs/activity.log", "r", encoding="utf-8") as f:
                # Get last 100 non-empty lines
                lines = [line.strip() for line in f.readlines() if line.strip()]
                recent_logs = lines[-100:] if len(lines) > 100 else lines

            if recent_logs:
                print("\nRecent Logs (Last 100 entries):")
                print("=" * 50)
                for line in recent_logs:
                    if "ERROR" in line:
                        Display.print_error(line)
                    elif "SUCCESS" in line:
                        Display.print_success(line)
                    elif "WARNING" in line:
                        Display.print_warning(line)
                    else:
                        Display.print_info(line)
                print("=" * 50)
            else:
                Display.print_error("No logs found!")
        except FileNotFoundError:
            Display.print_error("Log file not found!") 