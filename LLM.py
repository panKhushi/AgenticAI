import sys
print(sys.executable)
from openai import OpenAI
from config import API_KEY , BASE_URL , MODEL_NAME

client = OpenAI(
    api_key= API_KEY,
    base_url= BASE_URL
)

def chat(messages: list)-> str :
    response = client.chat.completions.create(
        model = MODEL_NAME,
        messages= messages,
        temperature= 0
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__" :
    messages = [
        { 
            "role": "user",
            "content" : "tell me the correct date and time"
        }
    ]
    response = chat(messages)

    print(response)