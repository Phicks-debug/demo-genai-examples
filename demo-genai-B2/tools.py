from modules.core import Tools

from datetime import datetime
import pytz, boto3, json
import wikipedia # type: ignore

import requests
from bs4 import BeautifulSoup
from langchain_community.tools import DuckDuckGoSearchRun
import pandas as pd
from vnstock3 import Vnstock
from datetime import date


@Tools.tool("retrieve","data")
def get_time_date() -> str:
    """
    Function to retrive current time day, month and year base on time zone
    """
    
    # Attempt to get the current time in the specified time zone
    tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(tz)

    # Format the time as a string
    return current_time.strftime('%Y-%m-%d %H:%M:%S %Z')


@Tools.tool("retrieve","documents")
def link_to_knowledgebase(query: str) -> json:
    """
    Function to call API to knowledge base and retrieve data source from it.
    
    @param query: The query we want to search for
    
    @return: Compressed json file with chunking base and link-sources
    """
        
    runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    
    # Compress into API POST request to send to knowledge base
    kwargs = {
        "knowledgeBaseId": "AYP6WXNCZ0",
        "retrievalConfiguration": {
            "vectorSearchConfiguration": {
                "numberOfResults": 100,
                "overrideSearchType": "HYBRID"   
            }
        },
        "retrievalQuery": {
            "text": query
        }
    }
    
    # Retrieve from knowledge base
    return runtime.retrieve(**kwargs)


@Tools.tool("retrieve", "data")
def get_article(search_term):
    """_
    Function to retrieve data from wiki page
    """
    
    results = wikipedia.search(search_term)
    first_result = results[0]
    page = wikipedia.page(first_result, auto_suggest=False)
    
    return page.content


@Tools.tool("retrieve", "data")
def get_stock_price(ticker: str, start:str):
    """
    Use this tool to retrieve the stock price data for a specific company. 
    This tool will get the price as a pandas dataframe, with open, high, low, close, volume and ticker columns.
    The tool has been set to take the price until today and 1 month behind as default. 
    If the user do not specify the date, always get the price for the latest date
    
    @param ticker:
    @param start:
    @param end:
    
    @return:
    """
    
    # Initiate the stock object
    stock = Vnstock().stock(symbol = ticker, source = "TCBS")
    today = date.today().strftime("%Y-%m-%d")
    
    # Query the latest stock until today
    price_df = stock.quote.history(start = start, end = today)
    
    return price_df.to_dict()
    
    
@Tools.tool("retrieve", "data")
def get_stock_intraday(ticker: str,):
    """
    Use this tool to get the intraday data for a stock ticker for the closest day until today
    
    @param ticker:
    
    @return: 
    """
    
    stock = Vnstock().stock(symbol = ticker, source = "TCBS")
    df = stock.quote.intraday(symbol = ticker, show_log = False)
    df["ticker"] = ticker
    
    return df.to_dict()
    

@Tools.tool("retrieve", "data")
def get_company_info(ticker: str):
    """
    Use this tool to get the overview profile of a company in Vietnam. 
    There will be two dataframe: overview dataframe let you know the profile, 
    and strategy will give you the company promise, business risk, key developments and business strategies of the company
    
    @param ticker:
    @param data:
    
    @return:
    """
    
    company = Vnstock().stock(symbol = ticker, source = "TCBS").company
    
    overview = company.overview()
    overview = overview[[
        "industry",
        "company_type", 
        "no_shareholders",
        "foreign_percent",
        "outstanding_share",
        "issue_share",
        "short_name",
        "website"
    ]]
    
    strategy = company.profile()
    strategy = strategy[[
        "company_promise",
        "business_risk",
        "key_developments",
        "business_strategies"
    ]]
    
    return overview.to_dict, strategy.to_dict
    

@Tools.tool("retrieve", "data")
def get_company_events(ticker: str):
    """
    Use this tool to get significant events of companies in Vietnam. 
    The output contains a dataframe includes rsi, rs, price, price_change_ratio, price_change_ratio_1m, event_name, event_desc.
    The rsi stands for Relative Strength Index, rs stands for Relative Strength, 
    price and price change ratio will allow you to know the impact of the events 
    and event description will let you know detail of the event.
    The tool will return only the 5 most recent events
    
    @param ticker:
    
    @return
    """
    
    company = Vnstock().stock(symbol = ticker, source = "TCBS").company
    
    events = company.events()
    events = events[[
        "rsi",
        "rs",
        "price",
        "price_change_ratio",
        "event_name",
        "event_desc"
    ]]
    
    return events.to_dict()
    

@Tools.tool("retrieve", "data")
def get_company_shareholders(ticker: str):
    """
    Use this tool to get the shareholders list of a company.
    
    @param ticker: ticker of the company
    
    @return:
    """
    
    # Initiate stock object
    company = Vnstock().stock(symbol = ticker, source = "TCBS").company
    
    # Get the shareholder list
    shareholders = company.shareholders()
    
    return shareholders.to_dict()


@Tools.tool("retrieve", "data")
def get_company_inside_trades(ticker: str):
    """
    Use this tool to get the dataframe contains the information of inside trades of companies.
    The tool will return you the announce date, deal action, deal quantity, 
    deal price and deal ratio of the trade.
    
    @param ticker:
    
    @return:
    """
    
    # Initiate object
    company = Vnstock().stock(symbol = ticker, source = "TCBS").company
    
    # Get dataframe of inside trades
    inside_trades = company.insider_deals()
    
    return inside_trades.to_dict()


@Tools.tool("retrieve", "data")
def get_subsidiaries(ticker: str):
    """
    Use this tool to get subsidiaries companies of a given company.
    
    @param ticker: ticker of the company
    """
    
    # Initiate object
    company = Vnstock().stock(symbol = ticker, source = "TCBS").company
    
    # Get the subsidiaries list
    subsidiares = company.subsidiaries()
    
    return subsidiares.to_dict()


@Tools.tool("retrieve", "data")
def get_dividends(ticker: str):
    """
    Use this tool to get the dataframe that contains data of dividends of a company.
    
    @param ticker: ticker of the company
    
    @return:
    """
    
    # Initiate object
    company = Vnstock().stock(symbol = ticker, source = "TCBS")
    
    # Get the dividends
    dividends = company.dividends()
    
    return dividends.to_dict()


## Get company financial information
@Tools.tool("retrieve", "data")
def get_company_balance_sheet(ticker: str, period: str = "year", period_back: int = 4):
    """
    Use this tool to get the balance sheet of the company. 
    The period by default is year, but you can adjust it to get quarter period by set the period parameter to 'quarter'.
    The tool will return balance sheets with contains some important information like cash, fixed asset, asset, debt, equity, capital and other balance sheet items.
    The tool will return the latest 4 quarter performance or 4 years by default. 
    However, you can modify the periods backward by changing the period_back parameters
    
    @param ticker:
    @param period:
    @param period_back:
    
    @return:
    """
    
    stock = Vnstock().stock(symbol = ticker, source = "VCI")
    balance_sheet = stock.finance.balance_sheet(period = period)
    # Get only latest 4 quarter
    balance_sheet = balance_sheet.iloc[:period_back]
    
    return balance_sheet.to_dict()


@Tools.tool("retrieve", "data")
def get_company_income_statement(ticker: str, period: str = "year", period_back: int = 4,):
    """
    Use this tool to get the income statement of the company. 
    The tool will return you 4 most recents quarters or years by default, depend on the parameter period.
    This tool can get data further time in the past by changing the period_back parameters.
    
    @param ticker:
    @param period:
    @param period_back:
    
    @return:
    """
    
    # Initiate Stock object
    stock = Vnstock().stock(symbol = ticker, source = "VCI")
    
    # Obtain income statement dataframe
    income_statement = stock.finance.income_statement(period = period)
    
    # Obtain latest 4 years or quarters
    income_statement = income_statement.iloc[:period_back]
    
    return income_statement.to_dict()


@Tools.tool("retrieve", "data")
def get_cash_flow(ticker: str, period: str = "year", period_back: int = 4):
    """
    Use this tool to get very detail cash flow information of a company. 
    This tool by default will get the latest 4 years or quarters backward. 
    However, it can get data for a longer time by changing the period_back
    
    
    @param ticker:
    @param period:
    @param period_back:
    
    @return:
    """
    
    # Initiate object
    stock = Vnstock().stock(symbol = ticker, source = "VCI").finance
    
    # Get the cash flow
    cash_flow = stock.cash_flow(period = period)
    
    # obtain the time
    cash_flow = cash_flow.iloc[:period_back]
    
    return cash_flow.to_dict()


@Tools.tool("retrieve", "data")
def get_company_financial_ratio(ticker:str, period: str = "year", period_back: int = 4):
    """
    Use this tool to get the very detail data about financial ratios of a company. 
    It includes some significant information like P/E, P/B, P/Cash Flow, Market Cap, EV/EBITDA, Profit margin, ROIC, ROA, and other ratios.
    The tool by default will get the latest 4 years or quarters, depending on the parameter period and period_back of the tool.
    In the data, if the Quarter column is 5, means that this is the data for the full year, not specific quarter
    
    @param ticker:
    @param period:
    @param period_back:
    
    @return:
    """
    # Initiate object
    stock = Vnstock().stock(symbol = ticker, source = "VCI").finance
    
    # Get the data
    financial_ratio = stock.ratio(period = period)
    
    # Change column name
    financial_ratio = financial_ratio.rename(columns = {"lengthReport" : "Quarter"})
    
    # Get the latest data
    financial_ratio = financial_ratio.iloc[:period_back]
    
    return financial_ratio.to_dict()
    

@Tools.tool("retrieve", "data")
def get_vnexpress_news(url, limit=10):
    """
    Use this tool only to search the news for stocks. This tool will fetch you the latest 10 news about stock market in Vietnam
    
    @params url: 
    """
    url = "https://vnexpress.net/kinh-doanh/chung-khoan"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = []

    # Select all article elements
    articles = soup.find_all('article', class_='item-news')

    for article in articles[:limit]:  # Limit to the first `limit` articles
        # Get the title and URL
        title_tag = article.find('h2', class_='title-news').find('a')
        title = title_tag.get_text(strip=True)
        article_url = title_tag['href']
        
        # Get the description
        description_tag = article.find('p', class_='description').find('a')
        description = description_tag.get_text(strip=True)
        
        # Store the extracted information
        news_items.append({
            'title': title,
            'url': article_url,
            'description': description
        })

    return news_items


@Tools.tool("retrieve", "data")
def get_relevant_news(search_term: str) -> str:
    """
    Use this tool to search for other news. Use this tool when the users asks for general news.
    
    @param search_term: Query search tool
    """
    search = DuckDuckGoSearchRun(max_results = 5)
    result = search.run(search_term)
    return result