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
                        borderColor: '#F0B429',
                        backgroundColor: 'rgba(240, 180, 41, 0.05)',
                        borderWidth: 1.5,
                        tension: 0.1,
                        fill: true,
                        pointRadius: 0,
                        pointHoverRadius: 4,
                        pointHoverBackgroundColor: '#F0B429',
                        pointHoverBorderColor: '#0D1117',
                        pointHoverBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#8B949E',
                                font: {
                                    family: 'Inter',
                                    size: 12,
                                    weight: '500'
                                }
                            }
                        },
                        tooltip: {
                            backgroundColor: '#1C2128',
                            titleColor: '#E6EDF3',
                            bodyColor: '#F0B429',
                            borderColor: '#30363D',
                            borderWidth: 1,
                            titleFont: {
                                family: 'Inter',
                                size: 12,
                                weight: '500'
                            },
                            bodyFont: {
                                family: 'Inter',
                                size: 14,
                                weight: '700'
                            },
                            padding: 12,
                            cornerRadius: 8,
                            displayColors: false
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: '#484F58',
                                font: {
                                    family: 'Inter',
                                    size: 11
                                },
                                maxTicksLimit: 12
                            },
                            grid: {
                                color: '#21262D',
                                drawBorder: false
                            }
                        },
                        y: {
                            ticks: {
                                color: '#484F58',
                                font: {
                                    family: 'Inter',
                                    size: 11
                                },
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            },
                            grid: {
                                color: '#21262D',
                                drawBorder: false
                            }
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
