from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Predefined spell intents and their descriptions
spells = {
    "lumos": "Lumos: A spell to light up your wand.",
    "accio": "Accio: A summoning charm to bring objects to you.",
    "expecto patronum": "Expecto Patronum: Conjures a protective Patronus.",
    "wingardium leviosa": "Wingardium Leviosa: Levitates objects.",
    "stupefy": "Stupefy: Stuns your opponent.",
    "expelliarmus": "Expelliarmus: Disarms your opponent."
}

# Default responses for unrecognized inputs
default_responses = [
    "Hmm, I don't recognize that spell. Can you try again?",
    "I'm not sure about that spell. Are you sure it's from Hogwarts?",
    "I don't have that spell in my book. Want to try another one?"
]

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chatbot endpoint to process user input and generate responses.
    """
    user_input = request.json.get("message", "").strip().lower()
    response = None

    # Check if input matches any spell
    for spell, description in spells.items():
        if spell in user_input:
            response = description
            break

    # Generate a random response if the input doesn't match any spell
    if response is None:
        response = random.choice(default_responses)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
