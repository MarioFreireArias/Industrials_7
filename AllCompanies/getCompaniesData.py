import pandas as pd 

def getCompaniesData():
    df = pd.read_csv('AllCompanies/AllSP500Companies.csv')
    #We only need the Industrials sector
    df = df[df['GICS Sector'] == 'Industrials']
    return df

def getCompanyTickers():
    df = getCompaniesData()
    companies = df['Symbol'].tolist()
    return companies

def getComanyCIK(ticker):
    df = getCompaniesData()
    cik = df[df['Symbol'] == ticker]['CIK'].values[0]
    return cik

