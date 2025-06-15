import pandas as pd
import os
from datetime import datetime
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from utils import Display, Logger, Delay

class Filter:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or Logger()

    async def is_user_in_group(self, user_username, target_group):
        """Check if user is already in the group"""
        try:
            participants = await self.client(GetParticipantsRequest(
                target_group, ChannelParticipantsSearch(user_username), offset=0, limit=1, hash=0
            ))
            return len(participants.users) > 0
        except Exception:
            return False

    async def filter_members(self, group_username, csv_file):
        """Filter members that are not in target group"""
        try:
            # Read members from CSV
            Display.print_info("Reading members data...")
            df = pd.read_csv(csv_file)
            target_group = await self.client.get_entity(group_username)
            
            total = len(df)
            not_in_group = []
            in_group = 0
            current = 0
            batch_count = 0

            Display.print_info(f"Starting to check {total} members against {group_username}")
            print()

            for index, user in df.iterrows():
                current += 1
                batch_count += 1
                
                try:
                    # Check if user is in group
                    if not await self.is_user_in_group(user['username'], target_group):
                        not_in_group.append({
                            'user_id': user['user_id'],
                            'access_hash': user['access_hash'],
                            'username': user['username'],
                            'first_name': user['first_name'] if 'first_name' in df.columns else '',
                            'status': 'valid'
                        })
                        log_msg = f"User {user['username']} not in group [{current}/{total}]"
                        self.logger.log(log_msg, "INFO")
                        Display.print_info(log_msg)
                    else:
                        in_group += 1
                        log_msg = f"User {user['username']} already in group [{current}/{total}]"
                        self.logger.log(log_msg, "INFO")
                        Display.print_warning(log_msg)

                    # Add delay every 30 users
                    if batch_count >= 30:
                        Display.print_warning(f"Checked {current} members. Take a break...")
                        await Delay.random_delay(20, 20, use_spinner=True)
                        batch_count = 0

                except Exception as e:
                    log_msg = f"Error checking {user['username']}: {str(e)} [{current}/{total}]"
                    self.logger.log(log_msg, "ERROR")
                    Display.print_error(log_msg)
                    continue

            print()  # Add space after progress ends

            # Save filtered results to new CSV
            if not_in_group:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                base_name = os.path.splitext(os.path.basename(csv_file))[0]
                filename = f"output/{base_name}_filtered_{timestamp}.csv"
                
                Display.print_info("Saving filtered results to CSV...")
                filtered_df = pd.DataFrame(not_in_group)
                filtered_df.to_csv(filename, index=False)
                
                # Show statistics
                stats = {
                    "Total Members": total,
                    "Total Checked": current,
                    "Not in Group": len(not_in_group),
                    "In Group": in_group,
                    "Result File": filename
                }
                Display.print_stats("Filtering Results", stats)
                
                self.logger.log(str(stats), "SUMMARY")
                Display.print_success("Filtering completed successfully")
                return filename
            else:
                Display.print_warning("All members are already in the group!")
                return None

        except Exception as e:
            Display.print_error(f"Error filtering members: {str(e)}")
            self.logger.log(f"Error in filter_members: {str(e)}", "ERROR")
            return None 