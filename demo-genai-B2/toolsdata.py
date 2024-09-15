
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


def return_tool():
    return [
        functionA,
        functionB,
        functionC,
        functionD,
        functionE
    ]
