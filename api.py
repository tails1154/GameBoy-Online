from flask import Flask, request, jsonify
from collections import deque

app = Flask(__name__)

# Buffers for each connected emulator ("player1", "player2")
buffers = {
    "player1": deque(),
    "player2": deque()
}

@app.route("/api/transfer", methods=["POST"])
def transfer_byte():
    """
    POST { "from": "player1", "to": "player2", "byte": <int> }
    Enqueue a byte to be received by the target.
    """
    data = request.json
    sender = data.get("from")
    receiver = data.get("to")
    byte = data.get("byte")
    if sender not in buffers or receiver not in buffers:
        return jsonify({"error": "Invalid sender or receiver"}), 400
    # Emulate serial transfer: push to receiver's buffer
    buffers[receiver].append(byte & 0xFF)
    return "ok"
@app.route("/api/receive", methods=["GET"])
def receive_byte():
    """
    GET /api/receive?player=player2
    Returns the next byte for the player, or 255 if none available.
    """
    player = request.args.get("player")
    if player not in buffers:
        return jsonify({"error": "Invalid player"}), 400
    if buffers[player]:
        byte = buffers[player].popleft()
    else:
        byte = 0xFF  # 0xFF means no cable or nothing sent
    return str(byte)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
