import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file for secure API key handling
load_dotenv()

# Configure the Gemini API with the API key from environment variables
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Define the generation configuration settings for the AI model
generation_config = {
    "temperature": 1,  # Controls the randomness of the response (higher = more creative)
    "top_p": 0.95,  # Top-p sampling, used for controlling the diversity of generated text
    "top_k": 40,  # Limits the number of tokens considered for each step in generation
    "max_output_tokens": 8192,  # Maximum number of tokens the model can generate (8192 is a common max)
    "response_mime_type": "text/plain",  # Specifies the format of the response as plain text
}

# Initialize the generative model from the Gemini API
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",  # Name of the model to be used
    generation_config=generation_config,  # Pass the generation config to the model
    system_instruction="Act as a blog expert. Generate a blog post for any topic the user will input. Make it professional and precise. Be insightful and flexible to fit the user’s needs.",
)

# Streamlit UI setup
st.header("Blog Post Generator AI")  # Display header for the Streamlit app
st.write("Enter a topic below and select the maximum length for the blog post.")  # Description text

# Streamlit slider for selecting the maximum length of the blog post
length_option = st.slider(
    "Select the maximum length of the blog post using the slider:",  # Label for the slider
    min_value=100,  # Minimum length of the blog post in words
    max_value=2000,  # Maximum length of the blog post in words
    value=500,  # Default value for the blog length (set to 500 words)
    step=100  # Slider steps in increments of 100 words
)

# Text input for the user to provide a topic for the blog post
topic = st.text_input("Enter the topic for your blog post:")

if topic:  # Check if the user has entered a topic
    # Display the selected topic and length on the page for confirmation
    st.write(f"Generating a blog post about **{topic}** with a maximum length of {length_option} words...")

    def process_gemini_response(prompt, length):
        """
        Process the user's input to generate a blog post using the Gemini API, ensuring the post
        respects the user-defined length in words.

        Args:
            prompt (str): The topic for which the blog post needs to be generated.
            length (int): The desired maximum length of the blog post, specified in words.

        Returns:
            str: The generated blog post text.
        """
        # Modify the prompt to include instructions on the desired blog length
        modified_prompt = f"Generate a blog post about '{prompt}' with a maximum of {length} words."
        
        # Start a new chat session with the Gemini model
        chat_session = model.start_chat()

        # Send the modified prompt to the model and get the response
        response = chat_session.send_message(modified_prompt)

        return response.text  # Return the generated text from the model

    # Call the function to generate the blog post based on the user’s topic and selected length
    blog_post = process_gemini_response(topic, length_option)

    # Display the generated blog post on the Streamlit app
    st.write(blog_post)
