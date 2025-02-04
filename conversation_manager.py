import json
import os

from llm_client import generate_text
from es_client import query_es, mapping_es
from config import NETFLOW_INDEX
from debugflags import debugflags
from prompt_templates import ADAPT_ES_QUERY, GENERATE_FINAL_ANSWER


def load_base_query_template(file: str) -> str:
    """
    Helper function that loads the contents of 'es_request_body.json' or 'dsl_query_example.json'
    and returns it as a string.
    """
    filepath = os.path.join(os.path.dirname(__file__), file)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def process_user_question(user_question: str) -> str:
    """
    Main conversation flow:
    1. Load the base JSON template from es_request_body.json and index mapping form Elasticsearch
    2. Build a prompt (ADAPT_ES_QUERY) instructing the LLM to adapt that template
       to the user's question.
    3. Parse the returned JSON. We expect a top-level object with a "query" key.
    4. Execute the query in Elasticsearch.
    5. Generate a final human-friendly answer (using GENERATE_FINAL_ANSWER).
    """

    # 1. Load the base JSON query template from file
    if debugflags.get_override_dsl_flag():
        print("--> Loading templates")
    base_query_template = load_base_query_template("es_request_body.json")
    es_mapping = mapping_es(NETFLOW_INDEX)

    # 2. Construct the prompt by injecting user_question and base_query_template
    if debugflags.get_override_dsl_flag():
        print("--> Rendering LLM query for DSL filter")
    prompt_for_query = ADAPT_ES_QUERY.format(
        user_query=user_question,
        base_query_template=base_query_template,
        index_mapping=es_mapping
    )

    # 3. Call the LLM
    if debugflags.get_override_dsl_flag():
        print("--> Running LLM model query asking to create DSL filter")
    llm_response = generate_text(prompt_for_query)

    if debugflags.get_debbugging_flag():
        print("### llm_response from generate_text(prompt_for_query) ###")
        print(llm_response)
        print("### type(llm_response) ###")
        print(type(llm_response))
        print("")

    # Attempt to parse the LLM's response as JSON
    if debugflags.get_override_dsl_flag():
        print("--> Processing LLM response")
    try:
        llm_response_json = json.loads(llm_response)
        es_query_body = llm_response_json.get("query", {})
    except json.JSONDecodeError:
        return (
            "Error: The model returned invalid JSON. "
            "Please refine the prompt or check the LLM output."
        )

    if not es_query_body:
        return (
            "Error: No 'query' field found in the LLM response. "
            "Make sure the model returned the JSON structure correctly."
        )

    if debugflags.get_override_dsl_flag():
        print("*** Overriding DSL filter ***")
        print("*** Using filter from dsl_query_example.json\n")
        es_query_body = load_base_query_template("dsl_query_example.json")

    # 4. Execute the query against Elasticsearch
    if debugflags.get_override_dsl_flag():
        print("--> Running Elasticsearch query")

    es_result = query_es(es_query_body, index=NETFLOW_INDEX)

    if debugflags.get_override_dsl_flag():
        print("### es_result from query_es(test, index=NETFLOW_INDEX) ###")
        print(es_result)
        print("### type(es_result) ###")
        print(type(es_result))
        print("")

    if not es_result:
        return "No valid response from Elasticsearch. Check logs or the query itself."

    # 5. Generate a final answer for the user
    if debugflags.get_override_dsl_flag():
        print("--> Rendering LLM query for explainng the Elasticsearch response")
    prompt_for_answer = GENERATE_FINAL_ANSWER.format(
        user_query=user_question,
        es_response=json.dumps(es_result, ensure_ascii=False, indent=2)
    )

    if debugflags.get_override_dsl_flag():
        print("--> Running LLM model query asking to explain Elasticsearch response")
    final_answer = generate_text(prompt_for_answer)

    if debugflags.get_override_dsl_flag():
        print("--> Returning LLM model answer")
    return final_answer
