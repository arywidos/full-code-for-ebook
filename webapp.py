from langchain_ollama import OllamaLLM   # Import the Ollama language model from langchain community library
from langchain.prompts import PromptTemplate   # Import PromptTemplate to create formatted prompts for the language model
import json                                   # Import JSON library for data handling
import streamlit as st                        # Import Streamlit for building web applications

# Set the configuration for the Streamlit app
st.set_page_config(page_title="🦜🔗 English Evpert V1.0", page_icon=":robot:")
st.title("🤖 English AI - V1.0")              # Title for the web app
st.caption("🚀English expert powered by AI (Llama3.1)")  # Caption to describe the app

# Initialize the Ollama language model with specified model version and base URL for local API access.
llm = OllamaLLM(model="llama3.1:8b", base_url="http://127.0.0.1:11434")
    
## Function to count words in a string
def count_words(string): 
    words = string.split()  # Split string into words
    return len(words)       # Return the number of words

# Main function to use the LLM for translation and grammar checking
def translate_grammar_checking(question):
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
        input_variables=["question"],  # Specify the input variable for the prompt template
    )
    grammar_chain = prompt | llm  # Combine the prompt with a language model to create a processing chain
    user_output = grammar_chain.invoke({"question": question})  # Invoke the processing chain with the input question to generate the output
    user_output = str(user_output.replace('```', ''))  # Clean up the output by removing any unwanted code formatting characters (like backticks)
    # Check if the output is empty (None)
    if user_output is None:
        print("The user did not respond")  # Notify if there was no response from the user
    else:
        
        outputs = json.loads(user_output)  # Load the cleaned-up output into a JSON object for easier access
        output  = outputs["output"]          # Extract the corrected sentence from the JSON object       
        explanation = outputs["explanation"]         # Extract the explanation for the correction from the JSON object
        out_puts = f"**Rephrashed:**\n\n:blue[{output}.]\n\n*:red[Hints: {explanation}]*"
        # Return the formatted output string
        return out_puts

# Create a form in the Streamlit app for user input
with st.form('my_form'):
    text = st.text_area('Please enter the text here, you would like me to review for grammatical accuracy:')
    submitted = st.form_submit_button('Submit')  # Submit button
    if submitted:
        with st.status("Checking, please wait...", expanded=True):  # Show status while processing
            if text == '':
                st.error("The text area appears to be blank. Could you please ensure that you have entered the required information?.")  # Error if text area is empty
            else:
                st.write(translate_grammar_checking(text))  # Display the result of translation/grammar checking
                st.success("Done!")  # Indicate process completion
