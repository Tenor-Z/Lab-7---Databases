"""
Description:
 Prints the name and age of all people in the Social Network database
 who are age 50 or older, and saves the information to a CSV file.

Usage:
 python old_people.py
"""
import os
import inspect
import sqlite3             #Need sqlite to interact with the db
import pandas as pd           #Pandas to write to csv later

def main():
    global db_path
    script_dir = get_script_dir()
    db_path = os.path.join(script_dir, 'social_network.db') #Get the local path to the database in question

    # Get the names and ages of all old people
    old_people_list = get_old_people()

    # Print the names and ages of all old people
    print_name_and_age(old_people_list)

    # Save the names and ages of all old people to a CSV file
    old_people_csv = os.path.join(script_dir, 'old_people.csv')
    save_name_and_age_to_csv(old_people_list, old_people_csv)

def get_old_people():
    """Queries the Social Network database for all people who are at least 50 years old.

    Returns:
        list: (name, age) of old people 
    """
    con = sqlite3.connect(db_path)    #Connect to the db
    cur = con.cursor()              #initate the cursor

    #We must craft a query that will look for ONLY people that are equal to or above the age of 50 years. We can use more than one variable in the SELECT field to make our search more easier. ppl is the table that was created in the db
  
    search_old_people = """
        SELECT name, age FROM ppl
        WHERE age >= 50;
    """
  
    cur.execute(search_old_people)     #Execute our query  
    result = cur.fetchall()             #The result variable will hold everything that matches our query
    con.close() #once it finishes, close the connection
    return result      #pass the results over

def print_name_and_age(name_and_age_list):
    """Prints name and age of all people in provided list

    Args:
        name_and_age_list (list): (name, age) of people
    """
    # TODO: Create function body
    for person in name_and_age_list:
      print(f'{person[0]} is {person[1]} years old.')
    return

def save_name_and_age_to_csv(name_and_age_list, csv_path):
    """Saves name and age of all people in provided list

    Args:
        name_and_age_list (list): (name, age) of people
        csv_path (str): Path of CSV file
    """
    report_df = pd.DataFrame(name_and_age_list)
    report_header = ('name', 'age')
    report_df.to_csv('old_fake_people.csv', index=False, header=report_header)
    return csv_path

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)


if __name__ == '__main__':
   main()