from flask import Flask, render_template, request, jsonify
from attacker_defender_game import (
    DEFAULT_MATRIX, calculate_equilibrium, simulate_game, matrix_summary
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    try:
        data = request.get_json(force=True) or {}
        raw_matrix = data.get("matrix", DEFAULT_MATRIX)
        if not isinstance(raw_matrix, list) or len(raw_matrix) != 2 or any(not isinstance(row, list) or len(row) != 2 for row in raw_matrix):
            return jsonify({"error": "Enter a 2 × 2 payoff matrix."}), 400
        matrix = [[float(v) for v in row] for row in raw_matrix]
        rounds = int(data.get("rounds", 10000))
        rounds = max(100, min(rounds, 100000))
        seed = int(data.get("seed", 42))
        result = calculate_equilibrium(matrix)
        simulation = simulate_game(matrix, result, rounds=rounds, seed=seed)
        summary = matrix_summary(matrix)
        return jsonify({
            "matrix": matrix,
            "equilibrium": result,
            "simulation": simulation,
            "summary": summary,
            "rounds": rounds
        })
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        return jsonify({"error": f"Could not calculate this game: {exc}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
