from debugflags import debugflags
from conversation_manager import process_user_question
import urllib3
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="NetFlow Chat - Ask your questions in English."
    )
    parser.add_argument(
        '--override-dsl',
        action='store_true',
        help='Override DSL template from LLM with one in dsl_query_example.json file.'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode so you can so what is actually happening.'
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Handle debug mode if enabled
    if args.debug:
        debugflags.set_debugging_flag()

    # Handle DSL override if enabled
    if args.override_dsl:
        debugflags.set_override_dsl_flag()

    urllib3.disable_warnings()

    print("Ask your question about NetFlow data in english (type 'exit' to finish):")
    while True:
        user_question = input("> ")
        if user_question.lower() in ["exit", "quit"]:
            print("The program has ended. Thank you")
            break

        response = process_user_question(user_question)
        print(f"[LLM Response]: {response}\n")


if __name__ == "__main__":
    main()
