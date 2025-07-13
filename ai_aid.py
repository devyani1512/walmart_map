# ai_assistant.py
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = ""

# Simulated store database
item_locations = {
    "milk": "Aisle 1, near dairy section",
    "bread": "Aisle 2, next to bakery",
    "rice": "Aisle 5, bottom shelf",
    "eggs": "Aisle 1, refrigerated section",
}

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get("query", "")
    

    found = []
    for item in item_locations:
        if item in user_input.lower():
            found.append(f"{item.capitalize()} is located at {item_locations[item]}.")

    if not found:
        return jsonify({"response": "Sorry, I couldn't find any matching items."})

    return jsonify({"response": " ".join(found)})

if __name__ == '__main__':
    app.run(debug=True)
