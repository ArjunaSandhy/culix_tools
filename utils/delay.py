import random
import time
import asyncio
from rich.progress import Progress
from .display import Display

class BatchDelay:
    def __init__(self, batch_size=5):
        self.successful_count = 0
        self.batch_size = batch_size

    async def handle_batch_delay(self):
        """Handle delay with batch counter logic"""
        self.successful_count += 1
        
        # Every batch_size successful operations, add a longer delay
        if self.successful_count % self.batch_size == 0:
            Display.print_warning(f"{self.batch_size} operations completed. Taking a longer break (10-15 minutes)...")
            await Delay.random_delay(600, 900, use_spinner=True)  # 10-15 minutes
        else:
            # Random delay between 120-180 seconds for each operation
            await Delay.random_delay(120, 180, use_spinner=True)  # 2-3 minutes

class Delay:
    @staticmethod
    async def spinner_countdown(seconds, message="Waiting"):
        """Display a spinner with countdown"""
        spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        for i in range(seconds, 0, -1):
            for char in spinner_chars:
                print(f"\r{char} {message} {i}s...", end='', flush=True)
                await asyncio.sleep(0.1)
        print('\r' + ' ' * 50 + '\r', end='', flush=True)

    @staticmethod
    async def random_delay(min_seconds=30, max_seconds=60, use_spinner=True):
        """Generate random delay between min_seconds and max_seconds"""
        delay = random.randint(min_seconds, max_seconds)
        
        if use_spinner:
            await Delay.spinner_countdown(delay)
        else:
            Display.print_success(f"Waiting for {delay} seconds...")
            with Progress() as progress:
                task = progress.add_task("[green]Waiting...", total=delay)
                for _ in range(delay):
                    await asyncio.sleep(1)
                    progress.update(task, advance=1)

    @staticmethod
    async def verify_delay():
        """Short delay for verifying member addition (2-5 seconds)"""
        await Delay.random_delay(2, 5, use_spinner=True)

    @staticmethod
    async def skip_delay(use_spinner=True):
        """Handle delay after skipping a user (60-90 seconds)"""
        await Delay.random_delay(60, 90, use_spinner)  # Increased from 30-60 to 60-90

    @staticmethod
    async def flood_wait(seconds, use_spinner=True):
        """Handle flood wait error"""
        if use_spinner:
            await Delay.spinner_countdown(seconds, "FloodWait")
        else:
            Display.print_error(f"FloodWaitError: Must wait {seconds} seconds")
            with Progress() as progress:
                task = progress.add_task("[red]Flood wait...", total=seconds)
                for _ in range(seconds):
                    await asyncio.sleep(1)
                    progress.update(task, advance=1) 