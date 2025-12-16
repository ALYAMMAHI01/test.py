# This function returns the current time and date in the format (SS:MM:HH , DD/MM/YYYY)
# where SS is seconds, MM is minutes, HH is hours, DD is day, MM is month, and YYYY is year.
# For example: (45:30:14 , 25/12/2024)
# The function can be imported and used in other modules as needed.

from datetime import datetime

def get_today_date():
    now = datetime.now()
    return f"({now.strftime('%S:%M:%H')} , {now.strftime('%d/%m/%Y')})"

# Example usage
if __name__ == "__main__":
    print(get_today_date())

# Note: The time format is in 24-hour format.













