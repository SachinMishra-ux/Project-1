from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

groq= Groq()

def classify_with_llm(log_message):

    prompt= """
    You are a log classification system. Your task is to classify the given log message into one of the following categories:
    1. Workflow Error
    2. Deprecation Warning
    If you are not able to classify the log message, return "Unclassified"
    Return only the category name, nothing else.
    Below is the log messages:
    {log_message}
    """

    response= groq.chat.completions.create(
        messages= [
            {"role": "user", "content": prompt.format(log_message=log_message)}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5)

    content= response.choices[0].message.content
    return content.strip()

if __name__ == "__main__":
    #log_message= "API endpoint 'getCustomerDetails' is deprecated and will be removed in version 3.2. Use 'fetchCustomerInfo' instead."
    log_message= "Lead conversion failed for prospect ID 7842 due to missing contact information."
    print(classify_with_llm(log_message))
    
    

    

    