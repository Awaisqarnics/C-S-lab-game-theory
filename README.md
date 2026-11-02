# Game Theory for Cybersecurity: Attacker vs. Defender — Web Project

A beginner-friendly Flask web application that demonstrates a 2×2 zero-sum attacker–defender game. It includes an editable payoff matrix, mixed-strategy calculations, a reproducible simulation, and interactive charts.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Internet connection for the Chart.js library used by the dashboard charts

## Run on Windows
1. Extract this ZIP file.
2. Open the extracted folder in VS Code or File Explorer.
3. In the folder, open Terminal / PowerShell.
4. Create a virtual environment:
   ```powershell
   python -m venv venv
   ```
5. Activate it:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, run this once in that terminal:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```
6. Install dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
7. Start the website:
   ```powershell
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.
9. Press **Run simulation** to calculate results.

## Project files
- `app.py` — Flask web server and API
- `attacker_defender_game.py` — game calculations and simulation logic
- `templates/index.html` — website structure
- `static/css/style.css` — responsive styling
- `static/js/script.js` — form handling and charts

## Model
The default attacker-payoff matrix is:

| | Defender: Protect server | Defender: Protect database |
|---|---:|---:|
| Attacker: Attack server | -2 | 5 |
| Attacker: Attack database | 4 | -1 |

Positive values favor the attacker; negative values represent attacker losses. The defender's objective in this zero-sum model is to minimize the attacker's expected payoff.

For this matrix, the mixed-strategy probabilities are calculated from the matrix. The app also runs a seeded simulation so results can be reproduced.

## Notes
- This is an educational model, not a real intrusion tool.
- The app currently supports a 2×2 payoff matrix.
- Do not use `debug=True` deployment mode on a public production server.
