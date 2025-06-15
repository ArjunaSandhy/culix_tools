import asyncio
import os
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from utils import Display
from telegram import TelegramHandler
import aioconsole

async def wait_for_enter():
    """Wait for Enter key and clear screen"""
    await aioconsole.ainput("\n→ Press Enter to return to main menu...")
    os.system('cls' if os.name == 'nt' else 'clear')
    Display.print_banner()

async def main():
    Display.print_banner()
    
    # Initialize Telegram client
    telegram = TelegramHandler()
    if not await telegram.initialize():
        Display.print_error("Failed to initialize Telegram client")
        return

    while True:
        choice = await inquirer.select(
            message="SELECT AN OPTION:",
            choices=[
                Choice("1", "→ [SCRAPER] COLLECT MEMBERS FROM GROUP"),
                Choice("2", "→ [ADDER] ADD MEMBERS TO YOUR GROUP"),
                Choice("3", "→ [FILTER] CHECK MEMBERS NOT IN TARGET GROUP"),
                Choice("4", "→ [LOGS] VIEW LAST 100 ACTIVITIES"),
                Choice("5", "→ [SHUTDOWN] STOP APPLICATION")
            ],
            default="1"
        ).execute_async()

        if choice == "1":
            group_username = await inquirer.text(
                message="Enter source group username (without @):",
                validate=lambda x: len(x) > 0
            ).execute_async()
            
            await telegram.scrape_members(group_username)
            await wait_for_enter()

        elif choice == "2":
            # Get available CSV files
            csv_files = [f for f in os.listdir('output') if f.endswith('.csv')]
            if not csv_files:
                Display.print_error("No member lists available. Please collect members first")
                await wait_for_enter()
                continue

            csv_file = await inquirer.select(
                message="Select members list:",
                choices=csv_files
            ).execute_async()

            group_username = await inquirer.text(
                message="Enter destination group username (without @):",
                validate=lambda x: len(x) > 0
            ).execute_async()

            await telegram.add_members(group_username, f"output/{csv_file}")
            await wait_for_enter()

        elif choice == "3":
            # Get available CSV files
            csv_files = [f for f in os.listdir('output') if f.endswith('.csv')]
            if not csv_files:
                Display.print_error("No member lists available. Please collect members first")
                await wait_for_enter()
                continue

            csv_file = await inquirer.select(
                message="Select members list to filter:",
                choices=csv_files
            ).execute_async()

            group_username = await inquirer.text(
                message="Enter target group username (without @):",
                validate=lambda x: len(x) > 0
            ).execute_async()

            await telegram.filter_members(group_username, f"output/{csv_file}")
            await wait_for_enter()

        elif choice == "4":
            await telegram.view_logs()
            await wait_for_enter()

        else:  # Exit
            Display.print_success("Thank you for using CULIX-TOOLS")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Display.print_warning("\nApplication closed by user") 