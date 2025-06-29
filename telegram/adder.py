import pandas as pd
import time
import sys
import asyncio
import random
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.types import InputPeerUser, ChannelParticipantsSearch
from telethon.errors import (
    FloodWaitError, 
    PeerFloodError, 
    UserPrivacyRestrictedError,
    UserNotMutualContactError,
    ChatWriteForbiddenError,
    UserAlreadyParticipantError
)
from utils import Display, Logger, Delay, BatchDelay, FloodControl
from datetime import datetime

class Adder:
    def __init__(self, client, logger=None):
        self.client = client
        self.logger = logger or Logger()
        self.batch_delay = BatchDelay(batch_size=5)
        self.flood_control = FloodControl()

    async def is_user_in_group(self, user_username, target_group):
        """Check if user is already in the group"""
        try:
            participants = await self.client(GetParticipantsRequest(
                target_group, ChannelParticipantsSearch(user_username), offset=0, limit=1, hash=0
            ))
            return len(participants.users) > 0
        except Exception:
            return False

    async def add_members(self, group_username, csv_file):
        """Add members to target group"""
        try:
            # Read members from CSV
            Display.print_info("Reading members data...")
            df = pd.read_csv(csv_file)
            target_group = await self.client.get_entity(group_username)
            
            success = 0
            failed = 0
            skipped = 0
            total = len(df)
            current = 0

            Display.print_info(f"Starting to add {total} members to {group_username}")
            Display.print_warning("Using random delay between 120-180 seconds per user")
            Display.print_warning("Additional 10-15 minutes delay every 5 successful additions")
            Display.print_warning("Taking initial warm-up delay (5 minutes)...")
            await Delay.random_delay(300, 300, use_spinner=True)  # 5 minutes warm-up
            print()  # Add space before progress starts

            for index, user in df.iterrows():
                current += 1
                try:
                    # Check if user is already in group
                    if await self.is_user_in_group(user['username'], target_group):
                        skipped += 1
                        log_msg = f"Skipped {user['username']} - Already in group [{current}/{total}]"
                        self.logger.log(log_msg, "INFO")
                        Display.print_info(log_msg)
                        await Delay.skip_delay()
                        continue

                    user_to_add = InputPeerUser(user['user_id'], user['access_hash'])
                    
                    # Try to add member
                    await self.client(InviteToChannelRequest(target_group, [user_to_add]))
                    
                    # Verify if user was actually added
                    await Delay.verify_delay()
                    if await self.is_user_in_group(user['username'], target_group):
                        success += 1
                        log_msg = f"Successfully added {user['username']} to {group_username} [{current}/{total}]"
                        self.logger.log(log_msg, "SUCCESS")
                        Display.print_success(log_msg)
                        
                        # Handle delay after successful addition
                        await self.batch_delay.handle_batch_delay()
                    else:
                        failed += 1
                        log_msg = f"Failed to add {user['username']} - Addition reported success but user not found in group [{current}/{total}]"
                        self.logger.log(log_msg, "FAILED")
                        Display.print_warning(log_msg)
                        continue

                except UserAlreadyParticipantError:
                    skipped += 1
                    log_msg = f"Skipped {user['username']} - Already in group [{current}/{total}]"
                    self.logger.log(log_msg, "INFO")
                    Display.print_info(log_msg)
                    await Delay.skip_delay()
                    continue

                except UserPrivacyRestrictedError:
                    failed += 1
                    log_msg = f"Failed to add {user['username']} to {group_username} - Privacy settings restricted [{current}/{total}]"
                    self.logger.log(log_msg, "FAILED")
                    Display.print_warning(log_msg)
                    await Delay.skip_delay()
                    continue
                    
                except PeerFloodError:
                    log_msg = f"Flood control triggered - attempting recovery"
                    self.logger.log(log_msg, "WARNING")
                    Display.print_warning(log_msg)
                    
                    # Handle with flood control system
                    can_continue = await self.flood_control.handle_flood_wait(300)  # Start with 5 minutes
                    if not can_continue:
                        log_msg = "Too many flood controls - stopping for safety"
                        self.logger.log(log_msg, "ERROR")
                        Display.print_error(log_msg)
                        break
                    continue
                    
                except FloodWaitError as e:
                    wait_time = e.seconds
                    log_msg = f"FloodWaitError: Need to wait {wait_time} seconds"
                    self.logger.log(log_msg, "WARNING")
                    Display.print_warning(log_msg)
                    
                    # Use flood control system for handling
                    can_continue = await self.flood_control.handle_flood_wait(wait_time)
                    if not can_continue:
                        log_msg = "Too many flood controls - stopping for safety"
                        self.logger.log(log_msg, "ERROR")
                        Display.print_error(log_msg)
                        break
                    continue
                    
                except (UserNotMutualContactError, ChatWriteForbiddenError) as e:
                    failed += 1
                    error_msg = str(e.__class__.__name__)
                    log_msg = f"Failed to add {user['username']} to {group_username} - {error_msg} [{current}/{total}]"
                    self.logger.log(log_msg, "FAILED")
                    Display.print_warning(log_msg)
                    continue
                    
                except Exception as e:
                    failed += 1
                    log_msg = f"Failed to add {user['username']} to {group_username} - {str(e)} [{current}/{total}]"
                    self.logger.log(log_msg, "FAILED")
                    Display.print_error(log_msg)
                    continue

            print()  # Add space after progress ends

            # Show final statistics
            stats = {
                "Total Members": total,
                "Successfully Added": success,
                "Failed": failed,
                "Skipped (Already in Group)": skipped,
                "Success Rate": f"{(success/(total-skipped)*100):.1f}%" if total > skipped else "0%"
            }
            Display.print_stats("Addition Results", stats)
            self.logger.log(str(stats), "SUMMARY")
            Display.print_success("Member addition process completed")

        except Exception as e:
            Display.print_error(f"Error adding members: {str(e)}")
            self.logger.log(f"Error in add_members: {str(e)}", "ERROR") 