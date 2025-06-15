# CULIX TOOLS

A professional CLI tool for Telegram member management with green neon aesthetics. Built with Python and Telethon.

## Features

- Member scraping from public groups
- Member adding to target groups
- Activity logging
- Professional CLI interface with progress tracking
- Smart delay system to avoid rate limits

## Docker Setup

### Prerequisites

- Docker installed on your system
- A Telegram API ID and API Hash (get from https://my.telegram.org/apps)

### Building the Docker Image

```bash
docker build -t culix-tools .
```

### Running the Container

```bash
docker run -it \
    -v $(pwd)/sessions:/app/sessions \
    -v $(pwd)/output:/app/output \
    -v $(pwd)/logs:/app/logs \
    -v $(pwd)/config:/app/config \
    culix-tools
```

The container uses volume mounts to persist data:
- `/app/sessions`: Telegram session files
- `/app/output`: Scraped member lists
- `/app/logs`: Activity logs
- `/app/config`: Configuration files

### First Run Setup

1. On first run, you'll need to enter your Telegram API credentials
2. You'll then be prompted to enter your phone number and verification code
3. After authentication, the session will be saved for future use

## Usage

The tool provides an interactive menu with the following options:

1. **[SCRAPER]** Collect members from a group
   - Enter the source group username (without @)
   - Members will be saved to a CSV file in the output directory

2. **[ADDER]** Add members to your group
   - Select a previously scraped members list
   - Enter the destination group username
   - The tool will handle delays and rate limits automatically

3. **[LOGS]** View last 100 activities
   - Shows recent operations and their results

4. **[SHUTDOWN]** Stop application

## Important Notes

- The tool implements smart delays to avoid Telegram's rate limits
- Batch delays are added every 10 successful operations
- Random delays between operations help avoid detection
- All activities are logged for monitoring

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

ARXADEV 