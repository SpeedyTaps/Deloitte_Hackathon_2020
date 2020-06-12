
from database import database, phone_numbers
from datetime import datetime
import pandas as pd
import subprocess
from msgclient import send_messages
'''
Database format:
[
    {'Postcode': 2010, 'Suburb': 'Hurstville', 'CaseCount': 3}
]
Phone Numbers format:
[
    {
        'Postcode': ,
        'Phone Numbers': []
    },
]

'''
def get_data():
	global database
	return database

def get_phone_numbers():
	global phone_numbers
	return phone_numbers



def compare_lengths():



    print("a")
    old_test = open("old.csv", "r")
    if(old_test == None):
        return {}
    print(old_test)
    print("\n\n")
    old = pd.read_csv("old.csv")
    oldlen = len(old)

    new = pd.read_csv("data.csv")
    newlen = len(new)

    if newlen > oldlen:
        #remove
        subprocess.call("bash remove_old.sh", shell=True)
        database.clear()
        todays_data()

    else:
        print("HERE\n\n")
        subprocess.call("bash remove_old.sh", shell=True)
        database.clear()






def add_number(number, postcode):
    phone_numbers = get_phone_numbers()
    postcode_exists = False
    for area in phone_numbers:
        if area['Postcode'] is postcode:
            postcode_exists = True
            area['Phone Numbers'].append(number)
            break
    if postcode_exists is False:
        new_postcode = {
            'Postcode': postcode,
            'Phone Numbers': [number],
        }
        phone_numbers.append(new_postcode)

    return {}

#Function that given a date in the format 'YYYY-MM-DD', will return that day's data
def date_data(date):
    formatted = get_data()
    all_data = pd.read_csv("old.csv")
    day_data = all_data.loc[all_data['notification_date'] == date]
    for case in day_data.itertuples():
        suburb = case.lga_name19
        postcode = case.postcode

        suburb_exists = False
        for area in formatted:
            if area['Suburb'] == suburb:

                suburb_exists = True
                area['CaseCount'] += 1
        if not suburb_exists:

            new_suburb = {
                'Postcode': str(int(postcode)),
                'Suburb': suburb,
                'CaseCount': 1
            }
            formatted.append(new_suburb)
            
    print(formatted)
    send_messages()


# Function that returns the current date data
def todays_data():
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    date_data(date)


if __name__ == '__main__':
    compare_lengths()
