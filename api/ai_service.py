import openai
import json
import os

from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from dotenv import load_dotenv

openai.api_key = '';

class ProductBundleGenerator:

    def __init__(self):
        load_dotenv()

        openai.api_key = os.getenv('OPENAI_API_KEY')
        llm = OpenAI(model="gpt-4-1106-preview")
        self.service_context = ServiceContext().from_defaults(llm=llm);


def generate_bundles(self, products_data):
    # Create a .txt file that contains the products_data
    with open('products_data.txt', 'w') as file:
        for product in products_data:
            file.write(f"{product}\n")

    # Load documents from the .txt file
    documents = SimpleDirectoryReader('products_data.txt').load_data()

    # Create the vector store index from the loaded documents
    index = VectorStoreIndex.from_documents(documents, service_context=self.service_context)
    query_engine = index.as_query_engine()

    # Create a prompt for generating a suggestion of product bundles (max of 3)
    my_prompt = (
        "Given the following products, suggest up to 3 product bundles that would "
        "provide a good mix and maximize value for the customer:\n\n"
        f"{products_data}"
    )

    # Query the index to generate bundle suggestions
    products = query_engine.query(my_prompt)

    # Return or process the generated bundle suggestions
    return assessment


def format_bundles(text):
    """
    Convert the text response from OpenAI into a list of bundles.

    Args:
        text (str): The response text from OpenAI.

    Returns:
        list of dict: Bundles with product details.
    """
    # Implement text parsing based on the format of OpenAI's response
    # This is a placeholder; adjust based on actual response format
    import json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Handle any errors in parsing
        return []