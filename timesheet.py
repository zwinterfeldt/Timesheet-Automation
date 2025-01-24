# Run this program to automate filling out your timesheet
# It uses selenium to fill out the timesheet for you

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
from dotenv import load_dotenv
import os

# Set up the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the timesheet URL
driver.get("https://web.mnsu.edu/eservices/")

# Set constants for star id and password
STAR_ID = os.getenv("STAR_ID")
PASSWORD = os.getenv("PASSWORD")

# Add your code here to log in and fill out the timesheet

# Locate the username field and enter the STAR_ID
username_field = driver.find_element(By.ID, "starid")
username_field.send_keys(STAR_ID)

# Locate the password field and enter the PASSWORD
password_field = driver.find_element(By.ID, "pinnbr")
password_field.send_keys(PASSWORD)

# Locate the submit button and click it
login_button = driver.find_element(By.NAME, "Submit")
login_button.click()

# If it makes you acknowledge terms and conditions, do so
# Check if the checkboxes exist and select them if they do
try:
    accept_tuition_checkbox = driver.find_element(By.ID, "accept_tuition")
    if not accept_tuition_checkbox.is_selected():
        accept_tuition_checkbox.click()
except:
    pass

try:
    understand_drop_checkbox = driver.find_element(By.ID, "understand_drop")
    if not understand_drop_checkbox.is_selected():
        understand_drop_checkbox.click()
except:
    pass

# Locate the continue button and click it
try:
    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "emquery"))
    )
    continue_button.click()
except:
    pass

# Locate the student employment link, and click it
try:
    student_employment_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Student Employment"))
    )
    student_employment_link.click()
except:
    pass

# Select 'Enter time worked'
try:
    enter_time_worked_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Enter Time Worked"))
    )
    enter_time_worked_link.click()
except:
    pass

# Ensure it's under the "CIS Lab TA" position
# try:
#     positions = WebDriverWait(driver, 10).until(
#         EC.presence_of_all_elements_located((By.CLASS_NAME, "well.table-responsive"))
#     )
#     for position in positions:
#         if "CIS Lab TA" in position.text:
#             add_time_button = WebDriverWait(position, 10).until(
#                 EC.element_to_be_clickable((By.ID, "addTime"))
#             )
#             add_time_button.click()
#             break
# except:
#     pass

def click_add_time_button(position_name):
    try:
        positions = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "well.table-responsive"))
        )
        for position in positions:
            if position_name in position.text:
                add_time_button = WebDriverWait(position, 10).until(
                    EC.element_to_be_clickable((By.ID, "addTime"))
                )
                add_time_button.click()
                break
    except:
        pass

# Example usage

# POSITION = "CIS Lab TA"
# click_add_time_button(POSITION)

# sleep(5)

# Fill out the timesheet entry

def is_time_already_submitted(day_of_week, start_time, end_time):
    try:
        # Locate the table rows in the entries field
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr"))
        )
        
        # Iterate through the rows to check if the day of the week and time match the provided values
        for row in rows:
            date_element = row.find_element(By.XPATH, ".//a[contains(@id, 'date_')]")
            start_time_element = row.find_elements(By.XPATH, ".//td")[1]
            end_time_element = row.find_elements(By.XPATH, ".//td")[2]
            
            if day_of_week in date_element.text and start_time in start_time_element.text and end_time in end_time_element.text:
                return True
    except Exception as e:
        print(f"An error occurred while checking for existing entries: {e}")
    
    return False

def get_next_available_date(day_of_week):
    # Get the date dropdown element
    date_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "date"))
    )
    select = Select(date_dropdown)
    
    # Iterate through the options to find the first available date with the specified day of the week
    for option in select.options:
        if option.text.startswith(day_of_week):
            return option.get_attribute("value")
    
    # If no date is found, return None
    return None

def fill_out_timesheet_entry(day_of_week, start_time, end_time, comments=""):
    try:
        # Get the first available date with the specified day of the week
        date = get_next_available_date(day_of_week)
        
        # Check if the time has already been submitted
        while date and is_time_already_submitted(day_of_week, start_time, end_time):
            # Get the next available date with the same day of the week
            date = get_next_available_date(day_of_week)
        
        if not date:
            print(f"No available dates found for {day_of_week}")
            return
        
        # Select the date
        date_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "date"))
        )
        Select(date_dropdown).select_by_value(date)

        # Select the start time
        start_time_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "startTime"))
        )
        Select(start_time_dropdown).select_by_value(start_time)

        # Select the end time
        end_time_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "endTime"))
        )
        Select(end_time_dropdown).select_by_value(end_time)

        # Enter comments
        comments_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "comments"))
        )
        comments_field.send_keys(comments)

        # Submit the form using the actual submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "timeSaveOrAddId"))
        )
        submit_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
POSITION = "CIS Lab TA"


# Fill out the timesheet

MY_TIMES_WORKED = [["Sunday", "0800AM", "0900AM", "Lab prep"], ["Thursday", "0300PM", "0400PM", "Zoom lab office hours"], ["Friday", "0200PM", "0300PM", "In person lab office hours"]]

# for i in range(len(MY_TIMES_WORKED)):
#     fill_out_timesheet_entry(MY_TIMES_WORKED[i][0], MY_TIMES_WORKED[i][1], MY_TIMES_WORKED[i][2], MY_TIMES_WORKED[i][3])

for time_entry in MY_TIMES_WORKED:
    click_add_time_button(POSITION)
    fill_out_timesheet_entry(time_entry[0], time_entry[1], time_entry[2], time_entry[3])
sleep(3)