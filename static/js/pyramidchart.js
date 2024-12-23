(function () {
    const ageGroups = ['80+', '75-79', '70-74', '65-69', '60-64', '55-59', '50-54', '45-49', '40-44', '35-39', '30-34', '25-29', '20-24', '15-19', '10-14', '5-9', '0-4'];
    const malePopulation = [-1000, -1500, -2000, -2400, -2700, -3000, -3200, -3400, -3600, -3700, -3800, -3900, -4000, -4200, -4500, -4800, -5000];
    const femalePopulation = [900, 1400, 1900, 2300, 2600, 2900, 3100, 3300, 3500, 3600, 3700, 3800, 3900, 4100, 4400, 4700, 4900];

    const ctx = document.getElementById('populationPyramid').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ageGroups,
            datasets: [
                {
                    label: 'Nam',
                    data: malePopulation,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Nữ',
                    data: femalePopulation,
                    backgroundColor: 'rgba(255, 206, 86, 0.7)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            scales: {
                x: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        callback: function (value) {
                            return Math.abs(value);
                        }
                    }
                },
                y: {
                    stacked: true,
                    reverse: false
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let value = Math.abs(context.raw);
                            return `${context.dataset.label}: ${value}`;
                        }
                    }
                }
            }
        }
    });
})();
