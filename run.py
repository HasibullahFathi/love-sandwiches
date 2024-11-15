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
    while True:
        print("Please enter your sales data from the last market.")
        print("Entered sales data should be six digits separated by commas.")
        print("Example: 23, 24, 25, 14, 31, 10\n")

        data_str = input("Please enter the data:\n")
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
    

# def update_sales_worksheet(data):
#     """
#     update sales data in a new row in the google sheet
#     """
#     print("Update Sales worksheet.\n")
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print("Data entered in sales successfully!\n")

# def update_surplus_worksheet(data):
#     """
#     update surplus data in a new row in the google sheet
#     """
#     print("Update Surplus worksheet.\n")
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print("Data entered in the surplus successfully!\n")

# refactorin update surplus and update sales sheet methods
def update_worksheet(data, worksheet):
    """
    Recieve a list of int to be inserted in a worksheet 
    update the relevant worksheet withh the given data.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"Data entered in {worksheet} successfully!\n")

def calculate_surplus_data(sales_row):
    """
    compare stock data with sales and calculates the surplus for each item.
    if the number of items is positive then the we have waste
    if the number of items is negative it means that made extra items when the stock was sold out.
    """
    print("calculating the surplus...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    Collecting the last 5 entries for each sandwich and returns
    the data as list of lists
    """
    sales = SHEET.worksheet('sales')
    
    columns = []
    for i in range(1, 7):
        column = sales.col_values(i)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_date(data):
    """
    Calculates the average stock for each item type , adding 10%.
    """
    print("Calculating the average stock")
    
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """ Main function runs all the functions"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_date(sales_columns)
    update_worksheet(stock_data, 'stock')

    return stock_data
    


print("Welcome to the Sales Manager!\n")
stock_data = main()

def get_stock_values(data):
    """
    Returns a dictionary of stock data headings
    add each value to it's corresponding stock data headings
    """
    headings = SHEET.worksheet('stock').get_all_values()[0]

    return {heading: value for heading, value in zip(headings, data)}
    

stock_values = get_stock_values(stock_data)
print(stock_values)