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

class FloodControl:
    def __init__(self):
        self.flood_count = 0
        self.last_flood_time = None
        self.cooldown_base = 900  # 15 minutes base cooldown
        self.max_retries = 3

    def record_flood(self):
        """Record a flood occurrence and get recommended wait time"""
        current_time = time.time()
        
        # Reset flood count if last flood was more than 6 hours ago
        if self.last_flood_time and (current_time - self.last_flood_time) > 21600:
            self.flood_count = 0
        
        self.flood_count += 1
        self.last_flood_time = current_time
        
        # Calculate progressive wait time
        wait_time = self.cooldown_base * (2 ** (self.flood_count - 1))
        return min(wait_time, 14400)  # Cap at 4 hours
    
    def should_stop(self):
        """Determine if we should stop the process entirely"""
        return self.flood_count >= self.max_retries

    async def handle_flood_wait(self, seconds, use_spinner=True):
        """Handle flood wait with progressive backoff"""
        wait_time = self.record_flood()
        
        if self.should_stop():
            Display.print_error("Too many flood controls triggered. Stopping for safety.")
            return False
            
        Display.print_warning(f"Flood control triggered ({self.flood_count}/{self.max_retries})")
        Display.print_warning(f"Taking an extended break: {wait_time//60} minutes")
        
        if use_spinner:
            await Delay.spinner_countdown(wait_time, "Flood cooldown")
        else:
            with Progress() as progress:
                task = progress.add_task("[yellow]Flood cooldown...", total=wait_time)
                for _ in range(wait_time):
                    await asyncio.sleep(1)
                    progress.update(task, advance=1)
        
        return True

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