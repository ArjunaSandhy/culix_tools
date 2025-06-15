import pandas as pd
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import FloodWaitError
from utils import Display, Logger, Delay
import asyncio
import os
from datetime import datetime

class Filter:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or Logger()
        self.consecutive_errors = 0
        self.current_delay = 1  # Initial delay in seconds

    async def is_user_in_group(self, user_username, target_group):
        """Check if user is already in the group"""
        try:
            participants = await self.client(GetParticipantsRequest(
                target_group, ChannelParticipantsSearch(user_username), offset=0, limit=1, hash=0
            ))
            self.consecutive_errors = 0  # Reset error counter on success
            return len(participants.users) > 0
        except FloodWaitError as e:
            self.consecutive_errors += 1
            wait_time = e.seconds
            log_msg = f"FloodWaitError: Wait for {wait_time} seconds"
            Display.print_warning(log_msg)
            self.logger.log(log_msg, "WARNING")
            
            # If wait time is reasonable, wait it out
            if wait_time <= 300:  # 5 minutes max
                await Delay.spinner_countdown(wait_time, "Waiting for flood wait")
                return await self.is_user_in_group(user_username, target_group)
            else:
                raise  # Re-raise if wait time is too long
        except Exception:
            return False

    async def filter_members(self, input_csv, group_username):
        """Filter members that are not in target group"""
        try:
            # Read members from CSV
            Display.print_info("Reading members from CSV...")
            df = pd.read_csv(input_csv)
            total = len(df)
            
            if total == 0:
                Display.print_error("CSV file is empty!")
                return
            
            target_group = await self.client.get_entity(group_username)
            
            # Create output directory if not exists
            os.makedirs('output', exist_ok=True)
            
            # Prepare output file
            input_filename = os.path.splitext(os.path.basename(input_csv))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"output/{input_filename}_filtered_{timestamp}.csv"
            
            # Lists to store filtered results
            not_in_group = []
            
            Display.print_info(f"Start filtering {total} members...")
            Display.print_info(f"Target group: {group_username}")
            print() # Add space before progress starts
            
            current = 0
            for index, user in df.iterrows():
                current += 1
                try:
                    if not await self.is_user_in_group(user['username'], target_group):
                        not_in_group.append(user)
                        log_msg = f"User {user['username']} not in group [{current}/{total}]"
                    else:
                        log_msg = f"User {user['username']} in group [{current}/{total}]"
                    
                    Display.print_info(log_msg)
                    self.logger.log(log_msg, "INFO")

                    # 1 second delay every 10 users
                    if current % 30 == 0 and current < total:
                        print() # Add space before warning
                        Display.print_warning(f"Checked {current} users. Taking a break...")
                        await Delay.spinner_countdown(18, "Cooling down")
                        print() # Add space after countdown
                    
                except FloodWaitError as e:
                    if e.seconds <= 300:  # 5 minutes max
                        Display.print_warning(f"FloodWaitError: Waiting for {e.seconds} seconds...")
                        await Delay.spinner_countdown(e.seconds, "Flood wait")
                        # Retry current user
                        current -= 1
                        continue
                    else:
                        Display.print_error(f"FloodWaitError too long ({e.seconds} seconds). Saving progress...")
                        break
                        
                except Exception as e:
                    log_msg = f"Error checking {user['username']}: {str(e)} [{current}/{total}]"
                    Display.print_error(log_msg)
                    self.logger.log(log_msg, "ERROR")
                    continue
            
            print() # Add space after progress ends
            
            # Save filtered results
            if not_in_group:
                filtered_df = pd.DataFrame(not_in_group)
                filtered_df.to_csv(output_file, index=False)
                
                # Show statistics
                stats = {
                    "Total Members": total,
                    "Total Checked": current,
                    "Not in Group": len(not_in_group),
                    "In Group": current - len(not_in_group),
                    "Result File": output_file
                }
                Display.print_stats("Hasil Filter", stats)
                self.logger.log(str(stats), "SUMMARY")
                Display.print_success("Filter process completed!")
                Display.print_info(f"Result filter saved in: {output_file}")
            else:
                Display.print_warning("No member to filter - all members are in the group")
            
        except Exception as e:
            Display.print_error(f"Error in filter process: {str(e)}")
            self.logger.log(f"Error in filter_members: {str(e)}", "ERROR") 