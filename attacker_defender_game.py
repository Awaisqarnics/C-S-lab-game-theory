"""Core game-theory calculations for a 2x2 zero-sum attacker-defender game."""
import random

DEFAULT_MATRIX = [[-2, 5], [4, -1]]
ATTACKER_STRATEGIES = ["Attack server", "Attack database"]
DEFENDER_STRATEGIES = ["Protect server", "Protect database"]


def calculate_equilibrium(matrix):
    """
    For attacker-payoff matrix [[a,b],[c,d]], compute the mixed-strategy
    equilibrium for a non-degenerate 2x2 zero-sum game.
    p = probability attacker uses row 1; q = probability defender uses column 1.
    """
    a, b = map(float, matrix[0])
    c, d = map(float, matrix[1])
    denominator = a - b - c + d
    if abs(denominator) < 1e-12:
        raise ValueError("This matrix has no unique mixed-strategy equilibrium; try different payoffs.")
    p = (d - c) / denominator
    q = (d - b) / denominator
    value = (a * d - b * c) / denominator

    # A valid interior mixed equilibrium requires probabilities between 0 and 1.
    # If not, report the algebraic values and indicate a pure-strategy boundary case.
    p_valid = -1e-9 <= p <= 1 + 1e-9
    q_valid = -1e-9 <= q <= 1 + 1e-9
    return {
        "attacker_row1_probability": round(max(0.0, min(1.0, p)), 6),
        "attacker_row2_probability": round(1.0 - max(0.0, min(1.0, p)), 6),
        "defender_col1_probability": round(max(0.0, min(1.0, q)), 6),
        "defender_col2_probability": round(1.0 - max(0.0, min(1.0, q)), 6),
        "expected_attacker_payoff": round(value, 6),
        "is_interior_mixed_equilibrium": bool(p_valid and q_valid),
        "note": "Mixed-strategy probabilities are shown for this 2×2 zero-sum model. If probabilities fall outside 0–1 before clipping, the game may have a pure-strategy equilibrium."
    }


def simulate_game(matrix, equilibrium, rounds=10000, seed=42):
    """Run a reproducible simulation by sampling equilibrium strategies."""
    rng = random.Random(seed)
    p = equilibrium["attacker_row1_probability"]
    q = equilibrium["defender_col1_probability"]
    counts = [[0, 0], [0, 0]]
    payoff_total = 0.0
    payoff_series = []
    running = 0.0
    for i in range(rounds):
        row = 0 if rng.random() < p else 1
        col = 0 if rng.random() < q else 1
        counts[row][col] += 1
        payoff = float(matrix[row][col])
        payoff_total += payoff
        running += payoff
        # Keep graph payload small while retaining a useful trend.
        if (i + 1) % max(1, rounds // 100) == 0 or i == rounds - 1:
            payoff_series.append({"round": i + 1, "average": round(running / (i + 1), 4)})
    return {
        "rounds": rounds,
        "average_attacker_payoff": round(payoff_total / rounds, 6),
        "outcome_counts": counts,
        "outcome_percentages": [
            [round(counts[r][c] * 100 / rounds, 2) for c in range(2)]
            for r in range(2)
        ],
        "payoff_series": payoff_series
    }


def matrix_summary(matrix):
    values = [float(x) for row in matrix for x in row]
    return {
        "best_attacker_payoff": max(values),
        "worst_attacker_payoff": min(values),
        "average_cell_payoff": round(sum(values) / len(values), 4)
    }
