# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("Please enter your sales data from the last market.")
        print("Entered sales data should be six digits separated by commas.")
        print("Example: 23, 24, 25, 14, 31, 10\n")

        data_str = input("Please enter the data: ")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Valid data!!!")
            break
    return sales_data

def validate_data(values):
    """
    run a while loop to validate sales data, inside try statement converting data into integers 
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
        return False

    return True
    

def update_sales_worksheet(data):
    """
    update sales data in a new row in the google sheet
    """
    print("Update Sales worksheet.\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Data entered in sales successfully!\n")

def update_surplus_worksheet(data):
    """
    update surplus data in a new row in the google sheet
    """
    print("Update Surplus worksheet.\n")
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print("Data entered in the surplus successfully!\n")

def calculate_surplus_data(sales_row):
    """
    compare stock data with sales and calculates the surplus for each item.
    if the number of items is positive then the we have waste
    if the number of items is negative it means that made extra items when the stock was sold out.
    """
    print("calculating the surplus")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def main():
    """ Main function runs all the functions"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)


print("Welcome to the Sales Manager!\n")
main()