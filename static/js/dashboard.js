document.addEventListener("DOMContentLoaded", () => {
  const data = window.FinTrackData;
  const cash = document.getElementById("cashFlowChart");
  if (cash && data) {
    new Chart(cash, {
      type: "line",
      data: { labels: data.labels, datasets: [
        { label: "Income", data: data.income, borderColor: "#16a675", backgroundColor: "rgba(22,166,117,.10)", fill: true, tension: .35 },
        { label: "Expenses", data: data.expense, borderColor: "#f08a4b", backgroundColor: "rgba(240,138,75,.08)", fill: true, tension: .35 }
      ]},
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } }, scales: { y: { beginAtZero: true, grid: { color: "#edf0f5" } }, x: { grid: { display: false } } } }
    });
  }
  const cat = document.getElementById("categoryChart");
  if (cat && data) {
    new Chart(cat, { type: "doughnut", data: { labels: data.categoryLabels, datasets: [{ data: data.categoryValues, backgroundColor: ["#7567e8","#20a779","#f2a45e","#5b9bd5","#df6b83","#9b87c9","#75b8b0"], borderWidth: 0 }] }, options: { responsive: true, maintainAspectRatio: false, cutout: "68%", plugins: { legend: { position: "bottom" } } } });
  }
  const year = document.getElementById("yearChart");
  if (year && window.reportData) {
    const d = window.reportData;
    new Chart(year, { type: "bar", data: { labels: d.labels, datasets: [{ label: "Income", data: d.income, backgroundColor: "#20a779", borderRadius: 6 }, { label: "Expenses", data: d.expense, backgroundColor: "#f2a45e", borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: "bottom" } }, scales: { y: { beginAtZero: true }, x: { grid: { display: false } } } } });
  }
});
