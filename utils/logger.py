import os
from datetime import datetime

class Logger:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.log_file = 'logs/activity.log'

    def log(self, message, level="INFO"):
        """Log a message with timestamp and level"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def log_scrape(self, group_name, total_members, valid_members):
        """Log scraping operation results"""
        self.log(f"Scraped {valid_members} valid members from {group_name} (Total: {total_members})", "SUCCESS")

    def log_invite(self, group_name, username, status, error=None):
        """Log invite activity"""
        if error:
            self.log(
                f"Failed to add {username} to {group_name}: {error}",
                "INVITE_ERROR"
            )
        else:
            self.log(
                f"Successfully added {username} to {group_name}",
                "INVITE"
            ) 