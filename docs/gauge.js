const ctx = document.getElementById('gauge');
let gauge;   // Chart instance

async function draw() {
  const res = await fetch('/api/latest');
  const data = await res.json();

  const zones = [
    { from: 0,   to: 45,  color: 'rgba(239,68,68,0.7)'  }, // red
    { from: 45,  to: 55,  color: 'rgba(107,114,128,0.7)'}, // gray
    { from: 55,  to: 100, color: 'rgba(16,185,129,0.7)'}  // green
  ];

  const cfg = {
    type: 'gauge',
    data: { datasets: [{
      value: data.fng,
      data: zones.map(z => z.to),
      backgroundColor: zones.map(z => z.color),
    }]},
    options: {
      needle: { radiusPercentage: 2, widthPercentage: 3 },
      valueLabel: { formatter: v => `${v}/100` },
      plugins: { legend: { display: false } }
    }
  };

  if (gauge) { gauge.destroy(); }
  gauge = new Chart(ctx, cfg);

  // Emoji depending on the zone
  const emoji = data.fng < 45 ? '😱' : data.fng > 55 ? '🤑' : '😐';
  document.getElementById('outcome').textContent =
    `${emoji} BTC sentiment: ${data.fng.toFixed(2)}/100`;
}

document.getElementById('reload').addEventListener('click', draw);
draw();  // initial
