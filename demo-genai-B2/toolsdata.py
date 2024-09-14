
functionA = {
    "name": "get_time_date",
    "description": "Always use at the start of any other function. \
        Always use for getting current time. Always use before analysing anything. \
        Tool for knowing the current time and day and year, month now at the moment. \
        Use this to know only the time at the moment. \
        Do not provide any input schema (no parameter for this function).",
    "input_schema": {
        "type": "object",
    },
}


functionB = {
    "name": "link_to_knowledgebase",
    "description": "A datasource that store every things about Chí Phèo story by Nam Cao. Use this to search more about the story,\
        the characters name Bá Kiến, Thị Nở, Tự Lãng, Chí Phèo, or other small characters in the story. \
            Use this to know more and to analysis when asking about the story and the characters.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The texts or keywords that you want to search for the reference  or for more information about it. \
                    This should be a pargraphs, a lot of string that you want to find more context,or a text that can help \
                        you understand more about the story, the characters ",
            }
        },
        "required": ["query"],
    },
}


functionC = {
    "name": "get_article",
    "description": "A tool to retrieve an up to date Wikipedia article. \
                    Use side by side with get_information tool for comparing and evaluation informations",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title",
            },
        },
        "required": ["search_term"],
    },
}


functionD = {
    "name": "call_wolframalpha",
    "description": "- WolframAlpha understands natural language queries about entities in chemistry, physics, geography, history, art, astronomy, and more.\
                - WolframAlpha performs mathematical calculations, date and unit conversions, formula solving, etc.\
                - Convert inputs to simplified keyword queries whenever possible (e.g. convert 'how many people live in France' to 'France population').\
                - Send queries in English only; translate non-English queries before sending, then respond in the original language.\
                - Display image URLs with Markdown syntax: ![URL]\
                - ALWAYS use this exponent notation: `6*10^14`, NEVER `6e14`.\
                - ALWAYS use {'input': query} structure for queries to Wolfram endpoints; `query` must ONLY be a single-line string.\
                - ALWAYS use proper Markdown formatting for all math, scientific, and chemical formulas, symbols, etc.:  '$$\n[expression]\n$$' for standalone cases and '\( [expression] \)' when inline.\
                - Never mention your knowledge cutoff date; Wolfram may return more recent data.\
                - Use ONLY single-letter variable names, with or without integer subscript (e.g., n, n1, n_1).\
                - Use named physical constants (e.g., 'speed of light') without numerical substitution.\
                - Include a space between compound units (e.g., 'Ω m' for 'ohm*meter').\
                - To solve for a variable in an equation with units, consider solving a corresponding equation without units; exclude counting units (e.g., books), include genuine units (e.g., kg).\
                - If data for multiple properties is needed, make separate calls for each property.\
                - If a WolframAlpha result is not relevant to the query:\
                -- If Wolfram provides multiple 'Assumptions' for a query, choose the more relevant one(s) without explaining the initial result. If you are unsure, ask the user to choose.\
                -- Re-send the exact same 'input' with NO modifications, and add the 'assumption' parameter, formatted as a list, with the relevant values.\
                -- ONLY simplify or rephrase the initial query if a more relevant 'Assumption' or other input suggestions are not provided.\
                -- Do not explain each step unless user input is needed. Proceed directly to making a better API call based on the available assumptions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to search on wolframalpha. query Must strictly follow the description of the function.",
            },
        },
        "required": ["query"],
    },
}


functionE = {
    "name": "get_information",
    "description": "Use this tool to search for anything on the internet. \
                    Use side by side with wiki tool for comparing and evaluation informations. \
                    Can Use this tool when the users asks for general news, that is recently.\
                    Must use this tool to get information of everything on the internet.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search query to find the information about it",
            },
        },
        "required": ["search_term"],
    },
}


tool_get_vnexpress_news = {
    "name": "get_vnexpress_news",
    "description": "Use this tool only to get the latest news for stocks. \
                    This tool will fetch you the latest 10 news about stock market in Vietnam \
                    Do not use this tool for searching any news. This tool only for retrieve stock new.",
    "input_schema": {
        "type": "object",
    },
}


tool_get_stock_price = {
    "name": "get_stock_price",
    "description": "Use this tool to retrieve the historical stock price data for a specific company.\
                    This tool will get the open high low close value of the ticker.\
                    The tool has been set to take the price until today and 1 month behind as default.\
                    If the user do not specify the date, always get the price for the latest date.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
            "start": {
                "type": "string",
                "description": "The start date for retrieving stock data, in YYYY-MM-DD format.",
            },
            "end": {
                "type": "string",
                "description": "The end date for retrieving stock data, in YYYY-MM-DD format.",
            },
        },
        "required": ["ticker", "start", "end"],
    },
}


tool_get_stock_intraday = {
    "name": "get_stock_intraday",
    "description": "Use this tool to get intraday stock data for a specific company for the closest day until today.\
                    This tool will output the price in hours to minutes level of the stock. \
                    Use this tool only if the users ask questions related to intraday stock price or for technical analysis questions. \
                    If the users do not ask about technical indicators or prices, or about fundamental analysis, do not use this tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_company_info = {
    "name": "get_company_info",
    "description": "Use this tool to get the overview profile of a company in Vietnam.\
                    This tool will output two information: company profile and company future strategies.\
                    The company profile includes industry, company type, shareholders, number of shares. \
                    The strategy includes company promise, business risk, key developments and business strategies of the firm.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_company_events = {
    "name": "get_company_events",
    "description": "Use this tool to get significant events of a specific firm in Vietnam.\
                    This tool will output name of events and description about it for the searched company. \
                    The output will also contains some basic indicators of the company like Relative Strength Index, Relative Strength, Price of the stock, some ratio like price change.\
                    This tool will help users know what is happening and have a quick glance how the events impact to the stock price of the firm.\
                    By default, this tool will get the latest 5 events for the firm.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_company_shareholders = {
    "name": "get_company_shareholders",
    "description": "Use this tool to get the list of shareholders for a specific company in Vietnam. \
                    The tool retrieves shareholder information, including their names and the amount of shares they hold. \
                    Use this tool only when users ask very specific questions regarding the shareholders in a specific firm.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            }
        },
        "required": ["ticker"],
    },
}


tool_get_company_inside_trades = {
    "name": "get_company_inside_trades",
    "description": "Use this tool to get the dataframe contains the information of inside trades of companies.\
                    The tool will return you the announce date, deal method,deal action, deal quantity,\
                    deal price and deal ratio of the trade. \
                    Use this tool only when users ask very specific questions about a firm. Do not use this tool for general questions like fundmental and technical analysis.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            }
        },
        "required": ["ticker"],
    },
}


tool_get_subsidiaries = {
    "name": "get_subsidiaries",
    "description": "Use this tool to retrieve the list of subsidiary companies for a given company. \
                    The tool will return you the names of the subsidiary companies and the percentage of ownership that the parent company has in each subsidiary.\
                    This tool is only used when users ask very specific questions about subsidiaries of the company to understand details. \
                    Do not use in cases that users just ask general fundamental or technical analysis if not needed.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            }
        },
        "required": ["ticker"],
    },
}


tool_get_dividends = {
    "name": "get_dividends",
    "description": "Use this tool to retrieve dividend information for a specific company. \
                    The tool provides a dataframe containing detailed dividend data, including: \
                    - `exercise_date`: The date when the dividend was paid. \
                    - `cash_year`: The year in which the dividend was declared. \
                    - `cash_dividend_percentage`: The percentage of the dividend paid in cash. \
                    - `issue_method`: The method used for issuing the dividend, such as cash or shares.\
                    Use this tool only when users ask specific questions related to fundamental analysis. Some questions will require analysis of divide",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            }
        },
        "required": ["ticker"],
    },
}


tool_get_company_balance_sheet = {
    "name": "get_company_balance_sheet",
    "description": "Use this tool to get the balance sheet of the company.\
                    The period by default is year, but you can adjust it to get quarter period by set the period parameter to 'quarter'.\
                    The tool will return balance sheets with contains some important information like cash, fixed asset, asset, debt, equity, capital and other balance sheet items.\
                    The tool will return the latest 4 quarter performance or 4 years by default.\
                    However, you can modify the periods backward by changing the period_back parameters.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
            "period": {
                "type": "string",
                "description": "The period for the balance sheet data, either 'year' or 'quarter'. Default is 'year'.",
            },
            "period_back": {
                "type": "integer",
                "description": "The number of periods to retrieve. Default is 4.",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_company_income_statement = {
    "name": "get_company_income_statement",
    "description": "Use this tool to get the income statement of a company.\
                    The tool will return you 4 most recents quarters or years by default, depend on the parameter period.\
                    This tool can get data further time in the past by changing the period_back parameters.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
            "period": {
                "type": "string",
                "description": "The period for the income statement data, either 'year' or 'quarter'. Default is 'year'.",
            },
            "period_back": {
                "type": "integer",
                "description": "The number of periods to retrieve. Default is 4.",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_cash_flow = {
    "name": "get_cash_flow",
    "description": "Use this tool to get very detail cash flow information of a company.\
                    This tool by default will get the latest 4 years or quarters backward.\
                    However, it can get data for a longer time by changing the period_back.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
            "period": {
                "type": "string",
                "description": "The period for the cash flow data, either 'year' or 'quarter'. Default is 'year'.",
            },
            "period_back": {
                "type": "integer",
                "description": "The number of periods to retrieve. Default is 4.",
            },
        },
        "required": ["ticker"],
    },
}


tool_get_company_financial_ratio = {
    "name": "get_company_financial_ratio",
    "description": "Use this tool to get the very detail data about financial ratios of a company.\
                    It includes some significant information like P/E, P/B, P/Cash Flow, Market Cap, EV/EBITDA, Profit margin, ROIC, ROA, and other ratios.\
                    The tool by default will get the latest 4 years or quarters, depending on the parameter period and period_back of the tool.\
                    In the data, if the Quarter column is 5, means that this is the data for the full year, not specific quarter.",
    "input_schema": {
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "The stock ticker symbol of the company (e.g., A32 for CTCP 32, AAA for CTCP Nhựa An Phát Xanh).",
            },
            "period": {
                "type": "string",
                "description": "The period for the financial ratio data, either 'year' or 'quarter'. Default is 'year'.",
            },
            "period_back": {
                "type": "integer",
                "description": "The number of periods to retrieve. Default is 4.",
            },
        },
        "required": ["ticker"],
    },
}


def return_tool():
    return [
        functionA,
        functionB,
        functionC,
        functionD,
        functionE,
        tool_get_vnexpress_news,
        tool_get_stock_price,
        tool_get_stock_intraday,
        tool_get_company_info,
        tool_get_company_events,
        tool_get_company_shareholders,
        tool_get_company_inside_trades,
        tool_get_subsidiaries,
        tool_get_dividends,
        tool_get_company_balance_sheet,
        tool_get_company_income_statement,
        tool_get_cash_flow,
        tool_get_company_financial_ratio,
    ]
