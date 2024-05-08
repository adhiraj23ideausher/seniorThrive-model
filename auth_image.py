from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from keras.preprocessing import image
import numpy as np
import openai
import base64
import requests
from dotenv import load_dotenv
load_dotenv()
import os

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")


def encode_image(image_path):
    if image_path.startswith('http://') or image_path.startswith('https://'):
        response = requests.get(image_path)
        response.raise_for_status()  
        image_data = response.content
    else:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()    
    return base64.b64encode(image_data).decode('utf-8')

# Function to calculate cosine similarity
def calculate_cosine_similarity(text1, texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1] + texts)
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:])
    return np.max(cosine_similarities)

# Function to caption the image and authenticate based on selected room
def caption_and_authenticate_image(image_path, selected_room):
    if selected_room=='others':
        return True
    encoded_image = encode_image(image_path)
    room_options = ['living room', 'bedroom', 'kitchen', 'bathroom', 'others'] # see mobile ui

    if selected_room.lower() not in room_options:
        # return "Invalid room selection. Please choose from: 'living room', 'bedroom', 'kitchen', 'bathroom', 'others'"
        return False
    result = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Tell me if the given photo is of the {selected_room} in one word yes or no"},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}"},
                ]
            },
        ],
        max_tokens=1000,
    )

    personalized_result = result.choices[0].message.content
    known_error_messages = [
        "I'm sorry, I can't provide assistance with that request.",
        "I'm sorry, but I cannot assist with this request.",
        "I'm sorry, but I cannot provide an analysis of the image based on your request.",
        "I'm sorry, I can't assist with that request."
    ]

    max_similarity = calculate_cosine_similarity(personalized_result, known_error_messages)
    similarity_threshold = 0.25

    if max_similarity > similarity_threshold:
        # return "Please take the photo again."
        return False
    elif "yes" in personalized_result.lower():  # Check if the output contains "yes"
        # return image_path  
        return True
    else:
        # return "Please reselect the option."
        return False

# url='https://upload.wikimedia.org/wikipedia/commons/5/50/Black_colour.jpg'
# print(caption_and_authenticate_image(url,'toilet'))