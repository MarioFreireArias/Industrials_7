import yfinance as yfinance
import pandas as pd
import datetime as dt
import os
import time
from AllCompanies.getCompaniesData import getCompanyTickers, getComanyCIK
from DataConversors import dfToAvro, dfToParquet, dfToCsv, dfToExcel, dfToJson, dfToParquet
#dfToOrc not working

# Get the current working directory
cwd = os.getcwd()

def prepare_environment():
    """
    Prepares the environment for the script to run.
    Creates neccessary folders and files if they don't exist.
    :return: None
    """
    #Create directory historical_data if it doesn't exist
    HISTORICAL_DATA_LOCATION = os.getenv("HISTORICAL_DATA_LOCATION")
    #If the user forgot to add the / at the beginning of the path, add it to avoid errors
    if (HISTORICAL_DATA_LOCATION[0] != '/'):
        HISTORICAL_DATA_LOCATION = '/' + HISTORICAL_DATA_LOCATION
    if not os.path.exists(cwd + HISTORICAL_DATA_LOCATION):
        os.makedirs(cwd + HISTORICAL_DATA_LOCATION)

    #Create subfolders for each filetype if the user wants to organize the data
    if (os.getenv("CREATE_SUBFOLDERS_FOR_EACH_FILETYE")=="1" or os.getenv("CREATE_SUBFOLDERS_FOR_EACH_FILETYE")=="True"):
        #Create subfolders for each filetype
        file_types = ['/avro', '/csv', '/excel', '/json', '/orc', '/parquet']
        for file_type in file_types:
            if not os.path.exists(cwd + HISTORICAL_DATA_LOCATION + file_type):
                os.makedirs(cwd + HISTORICAL_DATA_LOCATION + file_type)

def get_historical_data_single_ticker(ticker, start_date, end_date):
    """
    Gets historical data for a given ticker and date range
    :param ticker: Stock ticker
    :param start_date: Start date
    :param end_date: End date
    :return: Historical data for the given ticker and date range
    """
    # Get the historical data
    historical_data = yfinance.download(ticker, start=start_date, end=end_date)

    # Add the ticker as a column
    historical_data['ticker'] = ticker

    # Reset the index
    historical_data.reset_index(inplace=True)

    # Reorder the columns
    historical_data = historical_data[['ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]

    # Return the historical data
    return historical_data

def get_historical_data(start_date, end_date):
    compannies = getCompanyTickers()
    # Create an empty dataframe
    historical_data = pd.DataFrame()
    # For each ticker
    for ticker in compannies:
        cik = getComanyCIK(ticker)
        # Get the historical data for the ticker
        ticker_historical_data = get_historical_data_single_ticker(ticker, start_date, end_date)
        #New column with CIK
        ticker_historical_data.insert(0, 'CIK', cik)
        # Concatenate the dataframes
        historical_data = pd.concat([historical_data, ticker_historical_data])
    return historical_data

def save_historical_data(historical_data, file_type, output_location):
    """
    Saves the historical data to a file
    :param historical_data: Historical data
    :param file_type: File type
    :param output_location: Output location
    :return: None
    """
    # Get the current timestamp
    current_timestamp = time.strftime("%Y%m%d-%H%M%S")
    # Get the file name
    file_name = 'historical_data.' + file_type
    # Get the file path
    file_path = output_location + '/' + file_name
    # Save the historical data to a file
    if file_type == 'avro':
        dfToAvro(historical_data, file_path)
    elif file_type == 'csv':
        dfToCsv(historical_data, file_path)
    elif file_type == 'excel':
        dfToExcel(historical_data, file_path)
    elif file_type == 'json':
        dfToJson(historical_data, file_path)
    elif file_type == 'orc':
        #dfToOrc(historical_data, file_path)
        pass
    elif file_type == 'parquet':
        dfToParquet(historical_data, file_path)
    else:
        print('File type not supported')

