from langchain_ollama import OllamaLLM  
from langchain.prompts import PromptTemplate 
import json                             
import pyperclip                       

# Initialize the Ollama language model with specified model version and base URL for local API access.
llm = OllamaLLM(model="llama3.1:8b", base_url="http://127.0.0.1:11434")

def count_words(string): 
    words = string.split()  # Split the input string into words using whitespace as delimiter.
    return len(words)       # Return the count of words in the list.


# Main function to use the LLM for translation and grammar checking
def grammar_checking(question):
    prompt = PromptTemplate(  # Define a prompt template for grammar checking and translation
        template=f"""
        As an English expert, it is your duty to:
        - Your duty is to scrutinize and correct any grammatical inaccuracies in the sentences. 
        - Please rewrite them to ensure that they meet the standards English communication (email etc) and sound genuinely human.
        - Do not interpret any abbreviations; just leave them as they are.
        The result should be provided in the following JSON data structure:

        "input": "{question}",
        "output": "corrected sentence",
        "explanation": "brief explanation of the correction"
      
        Please respond only with the output in the exact format specified, without any further conversation or explanation.
        """,
        input_variables=["question"],  
    )
    grammar_chain = prompt | llm   # Combine prompt and language model into a chain for processing
    user_output = grammar_chain.invoke({"question": question}) # Invoke the chain with the input question
    user_output = str(user_output.replace('```', '')) # Clean up the output by removing unwanted characters
    
    if user_output is None:   # Check if the output is empty
        print("The user did not respond")  
    else:
        outputs = json.loads(user_output)   # Load output into a JSON object
        output = outputs["output"]  # Extract the corrected sentence
        pyperclip.copy(output) # copy the output to clipboard so user can paste the results on their editor or email app.
        explanation = outputs["explanation"]   # Extract the explanation for the correction
        out_puts = f"Rephrased by AI: {output}\nExplanation: {explanation}\n\n\n"
        return out_puts 

# Continuously prompt the user for input until valid text is processed.
while True:
    user_input = input("User Input:")
    if count_words(user_input) < 5:
        print("Can't proceed, the requesy only has few words, you need atleast 5 words")
    else:
        user_output = grammar_checking(user_input)  # Perform grammar checking and correction on the input text.
        print(user_output)  # Output the processed information.
        break  # Exit the loop after one cycle.