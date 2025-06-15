import json
import os
from telethon.sync import TelegramClient
from utils import Display, Logger
from .scraper import Scraper
from .adder import Adder

class TelegramHandler:
    def __init__(self):
        self.config = self.load_config()
        self.client = None
        self.logger = Logger()
        self.scraper = None
        self.adder = None

    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config/config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "api_id": "",
                "api_hash": "",
                "session_name": "session/culix_session"
            }

    def save_config(self):
        """Save configuration to config.json"""
        os.makedirs('config', exist_ok=True)
        with open('config/config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    async def initialize(self):
        """Initialize Telegram client"""
        if not self.config['api_id'] or not self.config['api_hash']:
            self.config['api_id'] = input(f"\nEnter your Telegram API ID: ")
            self.config['api_hash'] = input("Enter your Telegram API Hash: ")
            self.save_config()

        self.client = TelegramClient(
            self.config['session_name'],
            self.config['api_id'],
            self.config['api_hash']
        )
        await self.client.start()
        
        # Initialize components
        self.scraper = Scraper(self.client, self.logger)
        self.adder = Adder(self.client, self.logger)
        
        return True

    async def scrape_members(self, group_username):
        """Scrape members from a public group"""
        return await self.scraper.scrape(group_username)

    async def add_members(self, group_username, csv_file):
        """Add members to target group"""
        await self.adder.add_members(group_username, csv_file)

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