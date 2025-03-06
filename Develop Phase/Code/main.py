import re
import time
from bs4 import BeautifulSoup
from seleniumbase import Driver
import pandas as pd


def main():
    # Error check variables
    user_keywords = "ERR"
    user_location = "ERR"
    job_title = "ERR"
    job_location = "ERR"
    company_name = "ERR"
    query = "ERR"
    csv_file_path = "ERR"
    base_url = "ERR"
    apply_link = "ERR"
    search_url = "ERR"
    jobs_html = []
    date_posted = "ERR"
    jobs_list = []
    soup = "ERR"
    data_frame = []

    # Grab user search parameters
    user_keywords, user_location = general_check(lambda: get_user_input(), "Unable to grab search parameters...")

    # Google
    do_google_helper(user_keywords, user_location, query, data_frame)

    # Indeed
    do_indeed_helper(user_keywords, user_location, query, data_frame)

    # Ziprecruiter
    do_career_builder_helper(user_keywords, user_location, query, data_frame)

    # Final CSV
    final_csv_helper()


# Final CSV helper that concatenates all three csvs together and prints a pretty terminal output.
def final_csv_helper():
    # Reads all the csvs respectively.
    read_google = general_check(lambda: pd.read_csv('google_jobs_listings.csv', index_col="Job Title", na_values=0), "Could not open Google Job Listings...")
    read_indeed = general_check(lambda: pd.read_csv('indeed_job_listings.csv', index_col="Job Title", na_values=0), "Could not open Indeed Job Listings...")
    read_career_builder = general_check(lambda: pd.read_csv('career_builder_job_listings.csv', index_col="Job Title", na_values=0), "Could not open Career Builder Job Listings...")

    # Combines all the csvs and removes the duplicates if applicable.
    final_csv = pd.concat([read_career_builder, read_indeed, read_google]).drop_duplicates(keep='first')
    final_csv_dropped_duplicates = final_csv[~final_csv.index.duplicated(keep='first')]
    final_csv_dropped_duplicates.to_csv('final_csv', index=False)

    # Prints the final csv as a "to string" to get every column in the terminal
    print(final_csv_dropped_duplicates.to_string())


# Make a function that validates strings
def input_valid_str(input_check):
    check = False
    for char in input_check:
        if char.isalpha() or char == '+':
            pass
        else:
            check = True
    if check:
        return False
    else:
        return True


# Make a function that checks if a statement executes properly, throws specified error statement otherwise
def general_check(statement, err_statement):
    bool_check = True
    try:
        check = statement()
    except:
        print(err_statement)
        bool_check = False

    if bool_check:
        return check


# Career builder helper that grabs all the functions together and makes the actual csv file for career builder website.
def do_career_builder_helper(user_keywords, user_location, query, data_frame):
    base_url_zip_recruiter = 'https://www.careerbuilder.com/jobs?company_request=false&company_name=&company_id=&keywords='
    search_url_career_builder = general_check(
        lambda: create_user_search_parameters_career_builder(user_keywords, user_location, base_url_zip_recruiter,
                                                             query), "Unable to generate search...")

    # Soup grabs the actual HTMl of the website itself
    soup = general_check(lambda: get_html_code_indeed(search_url_career_builder), "Unable to load soup...")
    jobs_list = general_check(lambda: jobs_list_create_helper(soup, 'data-results-title dark-blue-text b'),
                              "Unable to generate jobs list...")

    # All of these find_job_data's grab the actual data, Job Title, Company, etc... and put it into job_list at the respective index.
    general_check(
        lambda: find_job_data_career_builder(soup, jobs_list, 'data-results-title dark-blue-text b', 0, 'div'),
        "Unable to initialize job search...")
    general_check(lambda: find_job_data_career_builder(soup, jobs_list, 'data-details', 1, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_career_builder(soup, jobs_list, 'data-details', 2, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_career_builder(soup, jobs_list, 'data-results-publish-time', 3, 'div'),
                  "Unable to initialize job search...")

    # Exports it into a csv file with its respective csv file name.
    csv_file_path = 'career_builder_job_listings.csv'
    convert_to_csv(jobs_list, csv_file_path, data_frame)


# Indeed helper that grabs all the functions together and makes the actual csv file for indeed website.
def do_indeed_helper(user_keywords, user_location, query, data_frame):
    base_url_indeed = "https://www.indeed.com/jobs"
    search_url_indeed = general_check(
        lambda: create_user_search_parameters_indeed(user_keywords, user_location, base_url_indeed, query),
        "Unable to generate search...")

    # Soup grabs the actual HTMl of the website itself
    soup = general_check(lambda: get_html_code_indeed(search_url_indeed), "Unable to load soup...")
    jobs_list = general_check(lambda: jobs_list_create_helper(soup, 'css-pt3vth e37uo190'),
                              "Unable to generate jobs list...")

    # All of these find_job_data's grab the actual data, Job Title, Company, etc... and put it into job_list at the respective index.
    general_check(lambda: find_job_data_indeed(soup, jobs_list, 'css-pt3vth e37uo190', 0, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_indeed(soup, jobs_list, 'css-1h7lukg eu4oa1w0', 1, 'span'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_indeed(soup, jobs_list, 'css-1restlb eu4oa1w0', 2, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_indeed(soup, jobs_list, 'css-1yxm164 eu4oa1w0', 3, 'span'),
                  "Unable to initialize job search...")

    # Exports it into a csv file with its respective csv file name.
    csv_file_path = 'indeed_job_listings.csv'
    general_check(lambda: convert_to_csv(jobs_list, csv_file_path, data_frame), 'Could not convert to CSV...')


# Google helper that grabs all the functions together and makes the actual csv file for Google website.
def do_google_helper(user_keywords, user_location, query, data_frame):
    base_url_google = "https://www.google.com/search"
    search_url_google = general_check(
        lambda: create_user_search_parameters_google(user_keywords, user_location, base_url_google, query),
        "Unable to generate search...")

    # Soup grabs the actual HTMl of the website itself
    soup = general_check(lambda: get_html_code_google(search_url_google), "Unable to load soup...")
    jobs_list = general_check(lambda: jobs_list_create_helper(soup, 'tNxQIb PUpOsf'), "Unable to generate jobs list...")

    # All of these find_job_data's grab the actual data, Job Title, Company, etc... and put it into job_list at the respective index.
    general_check(lambda: find_job_data_google(soup, jobs_list, 'tNxQIb PUpOsf', 0, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_google(soup, jobs_list, 'wHYlTd MKCbgd a3jPc', 1, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_google(soup, jobs_list, 'wHYlTd FqK3wc MKCbgd', 2, 'div'),
                  "Unable to initialize job search...")
    general_check(lambda: find_job_data_google(soup, jobs_list, 'gmxZue', 3, 'span'),
                  "Unable to initialize job search...")

    # Exports it into a csv file with its respective csv file name.
    csv_file_path = 'google_jobs_listings.csv'
    general_check(lambda: convert_to_csv(jobs_list, csv_file_path, data_frame), 'Could not convert to CSV...')


# Function that grabs user input and returns both the user_keyword and user_location.
def get_user_input():
    # Grabs the user input for the keyword
    print("Please enter any keyword that you would like with the spaces being replaced by +")
    print("\tExample: Data+Scientist, Computer+Science, etc..")
    user_keywords = input("\tEnter: ")

    # User input validation
    while True:
        check = input_valid_str(user_keywords)
        if check:
            break
        else:
            user_keywords = input("\tInvalid Input...\n\tEnter: ")

    # Grabs the user input for the location
    print("\nPlease enter any location that you would like with the spaces being replaced by +")
    print("\tExample: Kearney+Nebraska, Manhattan+New+York, etc...")
    user_location = input("\tEnter: ")

    # User input validation
    while True:
        check = input_valid_str(user_location)
        if check:
            break
        else:
            user_location = input("\tInvalid Input...\n\tEnter: ")

    # Return both the user_keyword and user_location
    return user_keywords, user_location


# Function that creates the user search url based off the keywords, location, base url, and query given for Google.
def create_user_search_parameters_google(user_keywords, user_location, base_url_google, query):
    # Creates the query by adding user_keyword and user_location with the rest of the query
    query = f"?q={user_keywords}+jobs+in+{user_location}&ibp=htl;jobs"

    # Creates the search url by adding the base url and the query
    search_url = base_url_google + query

    # Prints the URL and returns
    print("Search URL Google:", search_url)
    return search_url


# Function that creates the user search url based off the keywords, location, base url, and query given for Indeed.
def create_user_search_parameters_indeed(user_keywords, user_location, base_url_indeed, query):
    # Creates the query by adding user_keyword and user_location with the rest of the query
    query = f"?q={user_keywords}+&l=+{user_location}&radius=100&from=searchOnHP&vjk=95f6d1a03732205d"

    # Creates the search url by adding the base url and the query
    search_url = base_url_indeed + query

    # Prints the URL and returns
    print("\nSearch URL Indeed:", search_url)
    return search_url


# Function that creates the user search url based off the keywords, location, base url, and query given for Career Builder.
def create_user_search_parameters_career_builder(user_keywords, user_location, base_url_zip_recruiter, query):
    # Creates the query by adding user_keyword and user_location with the rest of the query
    query = f"{user_keywords}+&location=+{user_location}+%2C+&pay=&emp=&cb_veterans=false&cb_workhome=all&sort=date_desc"

    # Creates the search url by adding the base url and the query
    search_url = base_url_zip_recruiter + query

    # Prints the URL and returns
    print("\nSearch URL Zip Recruiter:", search_url)
    return search_url


# Function that grabs all the HTML code for the Google jobs page.
def get_html_code_google(search_url):
    # Creates a selenium driver to mimic an actual browser
    driver = general_check(lambda: Driver(browser="Chrome", uc=True, headless=False), "Unable to load driver...")
    general_check(lambda: driver.get(search_url), "Unable to load webpage...")
    bottom_height = general_check(lambda: driver.execute_script("return document.body.scrollHeight"),
                                  "Unable to execute script...")
    # Scroll down to the bottom until there is nothing left
    while True:
        general_check(lambda: driver.execute_script("window.scrollTo(0, document.body.scrollHeight);"),
                      "Unable to execute script...")
        time.sleep(.5)
        new_height = general_check(lambda: driver.execute_script("return document.body.scrollHeight"),
                                   "Unable to execute script...")

        # Once there is nothing left, save all the HTML data into "soup" and return
        if new_height == bottom_height:
            soup = general_check(lambda: BeautifulSoup(driver.page_source, 'html.parser'), "Unable to parse webpage...")
            return soup
        bottom_height = new_height


# Function that grabs all the HTML code for the first page of indeed search (because relevancy)
def get_html_code_indeed(search_url):
    # Creates a selenium driver to mimic an actual browser
    driver = general_check(lambda: Driver(browser="Chrome", uc=True, headless=False), "Unable to load driver...")
    general_check(lambda: driver.get(search_url), "Unable to load webpage...")

    # Allow the bot to mimic a real browser and bypass Cloudflare.
    time.sleep(2)

    # Save all the HTML data into "soup" and return
    soup = general_check(lambda: BeautifulSoup(driver.page_source, 'html.parser'), "Unable to parse webpage...")
    return soup


# Function that grabs all the HTML code for career builder
def get_html_code_career_builder(search_url):
    # Creates a selenium driver to mimic an actual browser
    driver = general_check(lambda: Driver(browser="Chrome", uc=True, headless=False), "Unable to load driver...")
    general_check(lambda: driver.get(search_url), "Unable to load webpage...")

    # Save all the HTML data into "soup" and return
    soup = general_check(lambda: BeautifulSoup(driver.page_source, 'html.parser'), "Unable to parse webpage...")
    return soup


# Function that creates the original size of the list itself for each website provided.
def jobs_list_create_helper(soup, class_name):
    job_cards = general_check(lambda: soup.find_all('div', class_=f'{class_name}'), "Unable to find class name...")
    rows, cols = (len(job_cards), 4)
    jobs_list = [[0 for i in range(cols)] for j in range(rows)]
    return jobs_list


# Function that grabs the actual job data from the HTML code, Job Title, Company, etc... for Google.
def find_job_data_google(soup, jobs_list, class_name, index, header):
    # Grabs all the HTML code specifically giving the header ('div','span, etc..) and class_name
    job_cards = general_check(lambda: soup.find_all(f'{header}', class_=f'{class_name}'),
                              "Unable to find class name...")

    # Counter to traverse through jobs_list
    counter = 0

    # Grabs the last two data types since they're together, splits, and inserts into respective indexes.
    if class_name == 'gmxZue':
        for every in job_cards:
            results = every.text.replace("ShareFacebookWhatsAppXEmailClick to copy linkShare linkLink copied", "")
            temp = results.split('via')
            last_two = temp[1].split("           ")
            stripped = last_two[1].split('ago', 1)[0]
            if 'days' in last_two[1]:
                jobs_list[counter][index] = stripped + 'ago'
            counter += 1

        # Return the job list once updated
        return jobs_list

    # For everything else proceed normally and insert into respective indexes
    for equipment_type in job_cards:
        jobs_list[counter][index] = equipment_type.text
        counter += 1

    # Return the job list once updated
    return jobs_list


# Function that grabs the actual job data from the HTML code, Job Title, Company, etc... for Indeed.
def find_job_data_indeed(soup, jobs_list, class_name, index, header):
    # Grabs all the HTML code specifically giving the header ('div','span, etc..) and class_name
    job_cards = general_check(lambda: soup.find_all(f'{header}', class_=f'{class_name}'),
                              "Unable to find class name...")

    # Counter to traverse through jobs_list
    counter = 0

    # For everything else proceed normally and insert into respective indexes
    for equipment_type in job_cards:
        jobs_list[counter][index] = equipment_type.text

        # For the Location & via class type, insert via. Indeed
        if class_name == 'css-1restlb eu4oa1w0':
            new_text = equipment_type.text + " via. Indeed"
            jobs_list[counter][index] = new_text

        # Date Posted had "Employer" in front of it, remove it from the string and insert into respective indexes
        if 'Employer' in equipment_type.text:
            new_text = equipment_type.text.replace('Employer', '')
            jobs_list[counter][index] = new_text
        counter += 1

    # Return the job list once updated
    return jobs_list


# Function that grabs the actual job data from the HTML code, Job Title, Company, etc... for Career Builder.
def find_job_data_career_builder(soup, jobs_list, class_name, index, header):
    # Grabs all the HTML code specifically giving the header ('div','span, etc..) and class_name
    job_cards = general_check(lambda: soup.find_all(f'{header}', class_=f'{class_name}'),
                              "Unable to find class name...")
    # Counter to traverse through jobs_list
    counter = 0

    # Proceed through the joc_cards and assign indexes according to if statement.
    for equipment_type in job_cards:

        # If class is for the Job Title, proceed normally
        if class_name == 'data-results-title dark-blue-text b':
            jobs_list[counter][index] = equipment_type.text
            counter += 1

        # If class is for the Date Posted, proceed normally
        if class_name == 'data-results-publish-time':
            jobs_list[counter][index] = equipment_type.text
            counter += 1

        # If strings are in text, take the Company and Location and put into respective indexes.
        if 'Full-Time' in equipment_type.text:
            data_list = re.split('\n', equipment_type.text)
            jobs_list[counter][index] = data_list[index]
            counter += 1
        if 'Part-Time' in equipment_type.text:
            data_list = re.split('\n', equipment_type.text)
            jobs_list[counter][index] = data_list[index]
            counter += 1
        if 'Intern' in equipment_type.text:
            data_list = re.split('\n', equipment_type.text)
            jobs_list[counter][index] = data_list[index]
            counter += 1

    # Return the job list once updated
    return jobs_list


# Converts all the data given and creates a CSV for each of the websites given.
def convert_to_csv(jobs_list, csv_file_path, data_frame):
    # Creates a pandas dataframe with the columns given.
    data_frame = general_check(lambda: pd.DataFrame(jobs_list, columns=['Job Title', 'Company', 'Location & via.', 'Date Posted']), 'Could not convert to DataFrame...')

    # Converts it into a csv
    general_check(lambda: data_frame.to_csv(f'{csv_file_path}', index=False), 'Could not convert to CSV...')


if __name__ == '__main__':
    main()
