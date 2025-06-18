# Tefillin Tracker

A simple command-line application to help you track when you put on Tefillin and to provide a daily reminder.

## Features

- Record the date you put on Tefillin.
- View a history of recorded dates.
- Set a daily morning reminder.

## Requirements

- Python 3.x
- The `schedule` library for the reminder feature.

## Installation

1.  Clone this repository or download the source code.
2.  Install the `schedule` library:
    ```bash
    pip install schedule
    ```

## Usage

The application is controlled via command-line arguments.

### Record Tefillin Date

To record that you put on Tefillin today:

```bash
python tefillin_tracker.py --record
```
This will save the current date to `tefillin_dates.json`.

### View Tefillin History

To view all recorded dates:

```bash
python tefillin_tracker.py --view
```

### Start Daily Reminder

To start the daily reminder service (this will run in the foreground):

```bash
python tefillin_tracker.py --start-reminder
```
The default reminder time is 08:00 (8 AM). You can specify a different time using the `--time` option:
```bash
python tefillin_tracker.py --start-reminder --time HH:MM
```
For example, for 7:30 AM:
```bash
python tefillin_tracker.py --start-reminder --time 07:30
```

### Display Help

To see the available commands:
```bash
python tefillin_tracker.py --help
```

## Running the Reminder in the Background

The `--start-reminder` command keeps the script running in your terminal. To have the reminder run automatically every day without needing to manually start it and keep a terminal open, you should use your operating system's task scheduler:

### Linux/macOS (using cron)

1.  Open your crontab for editing:
    ```bash
    crontab -e
    ```
2.  Add a line to run the script at your desired reminder time. For example, to run it daily at 8:00 AM (replace `/path/to/your/tefillin_tracker.py` with the actual absolute path to the script):
    ```cron
    0 8 * * * /usr/bin/python3 /path/to/your/tefillin_tracker.py --start-reminder --time 08:00
    ```
    *   **Note on background execution for cron**: The current `schedule_daily_reminder` function has an infinite loop (`while True`) which is fine for foreground execution but might not be ideal for a simple cron job that expects a script to perform a task and exit. For cron, a better approach would be to modify the script so that `--start-reminder` (when run by cron) just sends one notification if it's the right time, rather than scheduling and looping. However, for simplicity of the current application, we'll keep the loop and assume the user might run it in a detached session (e.g., using `nohup` or `screen`) if they don't use cron for the notification part itself but rather for launching the script.
    *   Alternatively, a more robust approach for cron would be to have a separate script that, when run by cron, checks if tefillin has been recorded for the day and sends a notification if not. This current script's reminder is more of a continuous scheduler.

    **A simpler cron setup for a *check* rather than a persistent scheduler:**
    If you want cron to just *trigger a check/notification* once at a specific time, you'd modify the script to have a mode that just sends the reminder and exits. For now, the README will describe running the existing scheduler.

### Windows (using Task Scheduler)

1.  Open Task Scheduler.
2.  Click "Create Basic Task..."
3.  Name: "Tefillin Reminder"
4.  Trigger: "Daily", set your desired start time.
5.  Action: "Start a program"
6.  Program/script: `python` or `pythonw` (if you don't want a console window)
7.  Add arguments: `C:\path\to\your\tefillin_tracker.py --start-reminder --time HH:MM` (use the actual path and desired time).
8.  Finish.

## Data Storage

Recorded dates are stored in a JSON file named `tefillin_dates.json` in the same directory as the script.
