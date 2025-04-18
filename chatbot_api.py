from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# Sample book data (same as the JSON you provided)
books = {
    "the great gatsby": "A novel set in the Jazz Age, telling the tragic story of Jay Gatsby's love for Daisy Buchanan and the moral decay of the American Dream.",
    "the odyssey": "An ancient Greek epic poem following Odysseus' ten-year journey home after the Trojan War, facing mythical creatures and divine interventions.",
    "we": "A dystopian novel set in a future totalitarian society where people live under constant surveillance, inspiring works like 1984.",
    "1984": "A novel portraying a totalitarian regime where Big Brother watches over citizens, controlling truth and suppressing individuality."
}

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_query = data.get("query", "").lower()

    response = "I don't know about that book. Try asking about 'The Great Gatsby', 'The Odyssey', 'We', or '1984'."

    for book in books:
        if book in user_query:
            response = books[book]
            break

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
