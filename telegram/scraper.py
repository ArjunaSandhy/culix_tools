import os
import pandas as pd
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsSearch
from utils import Display, Logger
import sys

class Scraper:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or Logger()

    async def scrape(self, group_username):
        """Scrape members from a public group"""
        try:
            Display.print_info(f"Starting to scrape members from {group_username}")
            channel = await self.client.get_entity(group_username)
            
            # Get total member count first
            full_channel = await self.client(GetFullChannelRequest(channel))
            total_participants = full_channel.full_chat.participants_count
            
            valid_members = []
            offset = 0
            limit = 200
            total_members = 0
            last_line_length = 0

            while True:
                participants = await self.client(GetParticipantsRequest(
                    channel, ChannelParticipantsSearch(''), offset, limit,
                    hash=0
                ))
                
                if not participants.users:
                    break

                total_members += len(participants.users)
                
                for user in participants.users:
                    if user.username and not user.bot and not user.deleted:
                        valid_members.append({
                            'user_id': user.id,
                            'access_hash': user.access_hash,
                            'username': user.username,
                            'first_name': user.first_name if user.first_name else '',
                            'status': 'valid'
                        })

                offset += len(participants.users)
                # Clear previous line and print new progress
                progress_msg = f"\rScraping member {total_members}/{total_participants} from {group_username}"
                sys.stdout.write(' ' * last_line_length + '\r')  # Clear previous line
                sys.stdout.write(progress_msg)
                sys.stdout.flush()
                last_line_length = len(progress_msg)

            print()  # New line after scraping complete
            
            # Save to CSV
            if valid_members:
                os.makedirs('output', exist_ok=True)
                filename = f"output/{group_username}_{len(valid_members)}.csv"
                
                Display.print_info("Saving results to CSV...")
                df = pd.DataFrame(valid_members)
                df.to_csv(filename, index=False)
                
                # Show statistics
                stats = {
                    "Total Members": total_members,
                    "Valid Members": len(valid_members),
                    "Output File": filename
                }
                Display.print_stats("Scraping Results", stats)
                
                self.logger.log_scrape(group_username, total_members, len(valid_members))
                Display.print_success("Scraping completed successfully")
                return filename
            else:
                Display.print_error("No valid members found!")
                return None

        except Exception as e:
            Display.print_error(f"Error scraping members: {str(e)}")
            self.logger.log(f"Error scraping {group_username}: {str(e)}", "ERROR")
            return None 