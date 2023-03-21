"""
Description:
 Creates the people table in the Social Network database
 and populates it with 200 fake people.

Usage:
 python create_db.py
"""
import os
import inspect
import faker                       #The faker module gets us our list of fake people
from faker import Faker
import sqlite3                       #Sqlite for creating and modifying SQL databases
import datetime                       #We need datetime in order to mark when the person's record was last created and modified


#The main function will run our subfunctions to create the database and nab our 200 fake people for us. The database will be named social_network.db and resides in the CWD. For some reason, Visual Studio was giving me errors about faker not existing when I already installed it, which could mean a corrupted installation and such.


def main():
  global db_path            #Make it global so we can use it throughout
  db_path = os.path.join(get_script_dir(), 'social_network.db') #The path itself is where the file resides, so it will create the database there later. This variable combines the working directory and the database itself to make the path
  create_people_table()
  populate_people_table()


#For the people_table, it is important to note that TEXT NOT NULL and INTEGER and such indicate what the type of data MUST be in order to be accepted into the database. For example, the name cannot be blank and the age must always be an integer.

def create_people_table():
  """Creates the people table in the database"""
  connection = sqlite3.connect(db_path)    #initiate connection
  cursor = connection.cursor()            #Initiate our cursor
  people_table = """                         
        CREATE TABLE IF NOT EXISTS ppl
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL,
            city TEXT NOT NULL,
            province TEXT NOT NULL,
            bio TEXT,
            age INTEGER,
            created_time DATETIME NOT NULL,
            updated_time DATETIME NOT NULL
        );
    """
  cursor.execute(people_table)      #Execute the given table above to add our content
  connection.commit()           #commit the changes, similar to Git's 'commit'
  connection.close()          #and close the connection
  return


def populate_people_table():
  """Populates the people table with 200 fake people"""
  connection = sqlite3.connect('social_network.db') #Initiate connection with the database (must do this to modify contents inside)
  #If the database mysteriously already does not exist, it will create it.
  cursor = connection.cursor()

  add_people = """
        INSERT INTO ppl
        (
            name,
            email,
            address,
            city,
            province,
            bio,
            age,
            created_time,
            updated_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
  
  #The VALUES field serves as a tuble of wildcards that could apply to any information given to it. The ? means anything that is entered as the value it corresponds with.abs. For us, the only two fields that are relevant is the name and age, which we use later on.
  
  fake = Faker("en_CA")               #Select fake canadian residents
  fake_american = Faker("en_US")      #For the bio field, we can use common American English sentences, hence why we have this variable.
  for i in range(200):                           #We need 200 people
    add_person = (fake.name(), fake.free_email(), fake.street_address(),
                  fake.city(), fake.administrative_unit(),
                  fake_american.sentence(nb_words=9), fake.random_int(1, 99),
                  datetime.now(), datetime.now())
                  #The age itself is a random number from 1 to 99, while the rest of the random information comes from the various functions within Faker
    cursor.execute(add_people, add_person)  #Execute our query
  connection.commit() #Commit and exit
  connection.close()
  return


def get_script_dir():
  """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
  script_path = os.path.abspath(
    inspect.getframeinfo(inspect.currentframe()).filename)
  return os.path.dirname(script_path)


if __name__ == '__main__':
  main()
