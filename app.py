from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Known item positions and descriptions
KNOWN_ITEMS = {
    "milk": "Dairy section near the top right",
    "eggs": "Dairy section near the top right",
    "bread": "Bakery aisle at the center back",
    "rice": "Grains section near the bottom right",
    "meat": "Butcher corner to the far right",
    "electronics": "Left wing near entrance",
    "toys": "Left middle zone",
    "fashion": "Clothing section center left",
    "pharmacy": "Front left corner"
}

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("query", "")
    item_list = ", ".join(KNOWN_ITEMS.keys())

    prompt = (
        f"Extract item names from this question: '{user_input}'.\n"
        f"Only choose from this list: {item_list}.\n"
        f"Return a JSON object like this:\n"
        f'{{"items": ["milk", "bread"], "directions": "Milk is in the Dairy section near the top right, Bread is at the Bakery section in the back"}}'
    )

    # Use OpenAI's latest Chat Completions API
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        parsed = eval(content) if "{" in content else {"items": [], "directions": content}
    except:
        parsed = {"items": [], "directions": "Sorry, I couldn't parse the item list."}

    return jsonify({
        "items": parsed.get("items", []),
        "reply": parsed.get("directions", "I couldn't find directions.")
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
