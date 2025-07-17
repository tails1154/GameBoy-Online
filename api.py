from flask import Flask, request, jsonify
from collections import deque
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

buffers = {
    "player1": deque(),
    "player2": deque()
}

@app.route("/api/transfer", methods=["GET"])
def transfer():
    player = request.args.get("player")
    data = request.args.get("data")  # the byte this player is sending

    if player not in buffers:
        return jsonify({"error": "Invalid player"}), 400

    # Validate and parse sent byte
    try:
        sent_byte = int(data)
    except (TypeError, ValueError):
        sent_byte = None

    # Determine the other player (the receiver)
    other_player = "player1" if player == "player2" else "player2"

    # If we have a byte to send, enqueue it to the other player's buffer
    if sent_byte is not None:
        buffers[other_player].append(sent_byte & 0xFF)

    # Pop the next received byte for this player (or 0xFF if none)
    if buffers[player]:
        received_byte = buffers[player].popleft()
    else:
        received_byte = 0xFF

    return jsonify(received_byte)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
