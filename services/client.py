from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
from pydoc import cli
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

# constants
BASE_URL = "https://api.novita.ai/v3/openai"
MODEL_NAME = "meta-llama/llama-3.2-1b-instruct"

client = OpenAI(
    base_url= BASE_URL,
    api_key=os.environ.get("NOVITA_API_KEY"),
)

def generate_commented_code(code:str, max_token:int):
    try:
        chat_responses = client.chat.completions.create(
        model= MODEL_NAME,
        temperature=0.7,
        stream= False,
        max_tokens= max_token,
        messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a senior software engineer skilled in writing precise comments only. Follow these instructions strictly:\n\n"
                        "Add **clear, concise, and professional comments** to the provided code. Include:\n"
                        "Docstrings for all functions and classes\n"
                        "Inline comments explaining non-obvious or critical logic\n\n"
                        "Strictly do not do anything else than writing comments. Stricltly do not add or provide alternative code"

                        "Example response:"
                        '''
                        def add(a, b):
                            """
                            Returns the sum of two numbers.

                            Args:
                                a (int): The first number.
                                b (int): The second number.

                            Returns:
                                int: The sum of a and b.

                            Raises:
                                TypeError: If either a or b is not an integer.
                                ValueError: If either a or b is negative.
                            """
                            # Check if both inputs are integers
                            if not isinstance(a, int) or not isinstance(b, int):
                                raise TypeError("Both inputs must be integers.")
                            # Check if both inputs are non-negative
                            if a < 0 or b < 0:
                                raise ValueError("Both inputs must be non-negative.")

                            # Use the built-in addition operator to perform the calculation
                            # This is more efficient and readable than using a loop or recursive function
                            return a + b
                        '''
                    )
                },
                {"role": "user", "content": code}
            ]
        )
        
        result = chat_responses.choices[0].message.content
        return result
    except Exception as ex:
        return f"Error generating comments {ex}"

def generate_documentation(code:str, max_token:int):
    try:
        chat_responses = client.chat.completions.create(
            model= MODEL_NAME,
            temperature=0.7,
            stream= False,
            max_tokens= max_token,
            messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior software engineer skilled in writing structured documentation only. Follow these instructions strictly:\n\n"
                            "Produce a **strictly formatted JSON** object with:\n"
                            "name: Function or class name\n"
                            "description: Brief summary of what it does\n"
                            "parameters: Dictionary with param name, type, and description\n"
                            "returns: Return name, type, and description\n"
                            "exceptions (optional): Raised exceptions with reasons\n"
                            "examples: Code usage examples with expected output\n\n"

                            "Example response: "
                            """
                            {
                                "name": "Add Function",
                                "description": "Adds two numbers together",
                                "parameters": {
                                    "a": {
                                        "name": "Number1",
                                        "type": "int",
                                        "description": "The first number to add"
                                    },
                                    "b": {
                                        "name": "Number2",
                                        "type": "int",
                                        "description": "The second number to add"
                                    }
                                },
                                "returns": {
                                    "name": "Result",
                                    "type": "int",
                                    "description": "The sum of the two numbers"
                                },
                                "exceptions": [],
                                "examples": [
                                    {
                                        "input": ["1", "2"],
                                        "expected_output": "3"
                                    },
                                    {
                                        "input": ["10", "5"],
                                        "expected_output": "15"
                                    }
                                ]
                            }
                            """
                        )
                    },
                    {"role": "user", "content": code}
                ]
        )
        
        result = chat_responses.choices[0].message.content
        return result
    except Exception as ex:
        return f"Error generating documentation {ex}"

def generate_improved_code(code:str, max_token:int):
    try:
        chat_responses = client.chat.completions.create(
            model= MODEL_NAME,
            temperature=0.7,
            stream= False,
            max_tokens= max_token,
            messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior software engineer skilled in writing improved code and finding complexity only. Follow these instructions strictly:\n\n"
                            "Analyze the code for **possible improvements**. If optimization is possible, provide a cleaner or more efficient version. Otherwise, write 'Already optimal"
                            "Report the **time complexity** of both the original and improved versions.\n\n"
                            "Output the following"
                            "1. \n<improved version or 'Already optimal'>\n"
                            "2. \nOriginal: O(...)\nImproved: O(...) or 'Same as original'\n"
                        )
                    },
                    {"role": "user", "content": code}
                ]
        )
        
        result = chat_responses.choices[0].message.content
        return result
    except Exception as ex:
        return f"Error generating improved code {ex}"

def generate_code_comments_and_docs(code:str, max_token:int=1024)->List:
    try:
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(generate_commented_code, code, max_token)
            future2 = executor.submit(generate_documentation, code, max_token)
            future3 = executor.submit(generate_improved_code, code, max_token)

            commented = future1.result()
            documentation = future2.result()
            improved = future3.result()

        return [commented, documentation, improved]
    except Exception as ex:
        return f"Error generating code, comments, and docs {ex}"
