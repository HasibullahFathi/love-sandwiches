# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')



def get_sales_data():
    """
    get sales data from user
    """
    print("Please enter your sales data from the last market.")
    print("Entered sales data should be six digits separated by commas.")
    print("Example: 23, 24, 25, 14, 31, 10\n")

    data_str = input("Please enter the data: ")
    sales_data = data_str.split(",")

    validate_data(sales_data)

def validate_data(values):
    """
    validate sales data, inside try statement converting data into integers 
    raise ValueError if values are not covertable to integers or it is not exactly six.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Sales data should contain exactly 6 values you provided {len(values)}"
                )
    except ValueError as e:
        print(f"Invalid data {e}, please try again!")
    


get_sales_data()

