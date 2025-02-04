GENERATE_FINAL_ANSWER = """
The user asks: "{user_query}"

Below are the results of the Elasticsearch query in JSON format:
{es_response}

Please provide a concise answer in English explaining the insights gained from the data.
Do not paste raw JSON structures. Use a user-friendly style.
"""

ADAPT_ES_QUERY = """
You have a base Elasticsearch query template in JSON:

{base_query_template}

And here is the ElasticSearch index mapping for index search will be performed on:

{index_mapping}

The user asks: "{user_query}"

Your task:
1. Take the base JSON query template and adapt it to reflect the user's request (time range, fields, filters, etc.).
2. Keep the JSON structure valid. Only modify or add the necessary parts.
3. Return a single JSON object with the top-level key "query".
   For example:
   {{
       "query": {{ 
          "size": 0,
          ... 
       }}
   }}
4. Output must be strictly valid JSON. Do not include extra commentary, code blocks, or markdown.
5. The returned object must be as simple as possible
"""
