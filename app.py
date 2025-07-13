from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import re
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

KNOWN_ITEMS = {
    "milk": "in the Dairy section near the top right",
    "bread": "in the Bakery section in the bottom right",
    "rice": "in the Grocery section near the middle right",
    "eggs": "in the Dairy section near the top right",
    "meat": "in the Meat section beside Bakery",
    "electronics": "in the top middle near Toys",
    "toys": "at the top left corner",
    "fashion": "in the center of the store",
    "pharmacy": "near the bottom left corner by Health & Beauty"
}

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("query")

    prompt = f"""
    Given this customer question: "{user_input}"
    Extract all item names that are present in this list: {', '.join(KNOWN_ITEMS.keys())}.
    Only return the names of matching items as a comma-separated list.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_items = response.choices[0].message.content
    items = [item.strip().lower() for item in re.split(r'[;,\n]', raw_items) if item.strip().lower() in KNOWN_ITEMS]

    if not items:
        return jsonify({"items": [], "reply": "Sorry, I couldn't find those items on the map."})

    directions = [f"{item.capitalize()} is {KNOWN_ITEMS[item]}." for item in items]
    reply = " ".join(directions)

    return jsonify({"items": items, "reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)

