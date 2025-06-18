# Tefillin Tracker
# This program helps users track their daily tefillin usage.

# --- Imports ---
import json
import datetime
import schedule
import time
import argparse

# --- Constants ---
# (No constants needed for this initial version)

# --- Functions ---

def tefillin_reminder():
  """Prints a reminder message for tefillin."""
  print("Good morning! Remember to put on tefillin today.")

def schedule_daily_reminder(time_str='08:00'):
  """Schedules the tefillin reminder daily at the specified time."""
  schedule.every().day.at(time_str).do(tefillin_reminder)
  print(f"Tefillin reminder scheduled daily at {time_str}.")
  while True:
    schedule.run_pending()
    time.sleep(1)

def record_tefillin_date(data_file='tefillin_dates.json'):
  """Records the current date for tefillin usage."""
  today = datetime.date.today()
  date_str = today.strftime('%Y-%m-%d')

  dates = []
  try:
    with open(data_file, 'r') as f:
      try:
        dates = json.load(f)
      except json.JSONDecodeError:
        # File is empty or not valid JSON, start with an empty list
        pass
  except FileNotFoundError:
    # File doesn't exist yet, will be created
    pass

  if date_str not in dates:
    dates.append(date_str)
    dates.sort() # Keep dates sorted
    with open(data_file, 'w') as f:
      json.dump(dates, f, indent=2)
    print(f"Tefillin recorded for {date_str}.")
  else:
    print(f"Tefillin already recorded for {date_str}.")

def view_tefillin_history(data_file='tefillin_dates.json'):
  """
  Retrieves the user's tefillin usage history.
  Returns a list of date strings or a message string if no history.
  """
  try:
    with open(data_file, 'r') as f:
      try:
        dates = json.load(f)
        if dates:
          return dates
        else:
          return "No tefillin dates recorded yet."
      except json.JSONDecodeError:
        return "No tefillin dates recorded yet (file is empty or corrupted)."
  except FileNotFoundError:
    return "No tefillin dates recorded yet (data file not found)."

# def get_streak():
#   """Calculates the current tefillin usage streak."""
#   pass

# --- Main Program ---
# if __name__ == "__main__":
#   # Main program logic will go here
#   # Example usage:
#   # record_tefillin_date()
#   # view_tefillin_history()
#   # To run the scheduler (this will block):
#   # schedule_daily_reminder(time_str='08:00')
  pass

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Tefillin Tracker CLI")
  parser.add_argument(
      "--record",
      action="store_true",
      help="Record tefillin usage for the current day."
  )
  parser.add_argument(
      "--view",
      action="store_true",
      help="View tefillin usage history."
  )
  parser.add_argument(
      "--start-reminder",
      action="store_true",
      help="Start the daily tefillin reminder. Default time is 08:00."
  )
  parser.add_argument(
      "--time",
      type=str,
      default="08:00",
      help="Specify the reminder time in HH:MM format (e.g., '09:30'). Used with --start-reminder."
  )

  args = parser.parse_args()

  if args.record:
    record_tefillin_date()
  elif args.view:
    history = view_tefillin_history()
    if isinstance(history, list):
      print("\nTefillin Dates Recorded:")
      for date_str in history:
        print(f"- {date_str}")
    else:
      print(history)
  elif args.start_reminder:
    schedule_daily_reminder(time_str=args.time)
  else:
    # If no arguments are provided, print help
    import sys
    if len(sys.argv) == 1:
      parser.print_help(sys.stderr)
    else:
      # Handle cases where unknown arguments might have been passed
      # or if other logic needs to be here when args are present but not the specific ones.
      # For now, if specific args aren't matched, and it's not a no-arg call,
      # argparse would have already exited with an error.
      # This 'else' might be redundant if argparse handles all other error cases.
      pass
