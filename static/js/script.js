let outcomeChart = null;
let payoffChart = null;

const $ = (id) => document.getElementById(id);
const percent = (v) => `${(Number(v) * 100).toFixed(2)}%`;
const fmt = (v) => Number(v).toFixed(3);

function setBar(id, probability) {
  $(id).style.width = `${Math.max(0, Math.min(100, Number(probability) * 100))}%`;
}

function renderCharts(data) {
  if (typeof Chart === "undefined") {
    $("message").textContent = "Results calculated. Charts need an internet connection to load Chart.js.";
    return;
  }
  const counts = data.simulation.outcome_counts;
  const labels = [
    "Attack server × Protect server",
    "Attack server × Protect database",
    "Attack database × Protect server",
    "Attack database × Protect database"
  ];
  const flattened = [counts[0][0], counts[0][1], counts[1][0], counts[1][1]];
  if (outcomeChart) outcomeChart.destroy();
  outcomeChart = new Chart($("outcomeChart"), {
    type: "bar",
    data: { labels, datasets: [{ label: "Observed rounds", data: flattened, backgroundColor: ["#7359e8", "#4788f5", "#24b58a", "#f3a14b"], borderRadius: 6, maxBarThickness: 42 }] },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { ticks: { maxRotation: 25, minRotation: 0, font: { size: 9 } }, grid: { display: false } }, y: { beginAtZero: true, ticks: { precision: 0 } } } }
  });
  const series = data.simulation.payoff_series;
  if (payoffChart) payoffChart.destroy();
  payoffChart = new Chart($("payoffChart"), {
    type: "line",
    data: { labels: series.map(p => p.round), datasets: [{ label: "Running average payoff", data: series.map(p => p.average), borderColor: "#7257e8", backgroundColor: "#7257e81a", fill: true, pointRadius: 0, borderWidth: 2, tension: .18 }] },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: "Round" }, grid: { display: false }, ticks: { maxTicksLimit: 6 } }, y: { title: { display: true, text: "Average payoff" } } } }
  });
}

async function runSimulation() {
  const btn = $("run-btn");
  const message = $("message");
  btn.disabled = true;
  message.classList.remove("error");
  message.textContent = "Calculating equilibrium and running simulation…";
  try {
    const matrix = [
      [Number($("a").value), Number($("b").value)],
      [Number($("c").value), Number($("d").value)]
    ];
    if (matrix.flat().some(v => !Number.isFinite(v))) throw new Error("Please enter a valid number in every payoff cell.");
    const response = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ matrix, rounds: Number($("rounds").value), seed: Number($("seed").value || 42) })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The simulation could not be completed.");
    const e = data.equilibrium;
    $("rounds-stat").textContent = Number(data.rounds).toLocaleString();
    $("expected-stat").textContent = fmt(e.expected_attacker_payoff);
    $("attacker-stat").textContent = percent(e.attacker_row1_probability);
    $("defender-stat").textContent = percent(e.defender_col1_probability);
    $("attacker-prob").textContent = percent(e.attacker_row1_probability);
    $("attacker2-prob").textContent = percent(e.attacker_row2_probability);
    $("defender-prob").textContent = percent(e.defender_col1_probability);
    $("defender2-prob").textContent = percent(e.defender_col2_probability);
    setBar("attacker-bar", e.attacker_row1_probability);
    setBar("attacker2-bar", e.attacker_row2_probability);
    setBar("defender-bar", e.defender_col1_probability);
    setBar("defender2-bar", e.defender_col2_probability);
    $("game-value").textContent = fmt(e.expected_attacker_payoff);
    $("equilibrium-note").textContent = e.note;
    renderCharts(data);
    message.textContent = `Done. Simulated ${Number(data.rounds).toLocaleString()} rounds. Average simulated payoff: ${fmt(data.simulation.average_attacker_payoff)}.`;
  } catch (err) {
    message.textContent = err.message;
    message.classList.add("error");
  } finally {
    btn.disabled = false;
  }
}

$("run-btn").addEventListener("click", runSimulation);
$("reset-btn").addEventListener("click", () => {
  $("a").value = -2; $("b").value = 5; $("c").value = 4; $("d").value = -1;
  $("rounds").value = 10000; $("seed").value = 42;
  runSimulation();
});
runSimulation();
