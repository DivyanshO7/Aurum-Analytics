document.addEventListener('DOMContentLoaded', function () {
    // Only initialize chart if on chart page
    const ctx = document.getElementById('goldChart');
    if (ctx) {
        initChart(ctx);
    }
});

let myChart;

function initChart(ctx) {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {

            const labels = data.dates;
            const prices = data.prices;

            // Forecast Data Append (Visual hack to show prediction)
            const lastDate = labels[labels.length - 1];
            const futureDates = data.prediction.future_dates;
            const futurePrices = data.prediction.future_prices;

            // Combine for visualization
            // For a simple line charts, we can just show historical for now 
            // and maybe a dashed line for future if we had complex dataset merging logic here vs pure JS.
            // keeping it simple: Show Historical Data

            const config = {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Gold Price (USD)',
                        data: prices,
                        borderColor: '#facc15',
                        backgroundColor: 'rgba(250, 204, 21, 0.1)',
                        borderWidth: 2,
                        tension: 0.1,
                        fill: true,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: { color: '#94a3b8' }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#94a3b8' },
                            grid: { color: '#334155' }
                        },
                        y: {
                            ticks: { color: '#94a3b8' },
                            grid: { color: '#334155' }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index',
                    },
                }
            };

            myChart = new Chart(ctx, config);
        })
        .catch(error => console.error('Error fetching chart data:', error));
}

function updateChart(period) {
    // In a real app, this would fetch filtered data from API
    // For this prototype, we'll just simulate a zoom/filter or reload
    // Since we fetch 1y by default, we can slice the data array in JS.

    // Simulating "active" class toggle
    document.querySelectorAll('.chart-controls button').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    alert("Time period filter: " + period + " (Logic would slice data array here)");
}
