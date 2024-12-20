const ctx = document.getElementById('covidChart').getContext('2d');

// Dữ liệu biểu đồ
const data = {
    labels: ['Jul 2023', 'Aug 2023', 'Sep 2023', 'Oct 2023', 'Nov 2023', 'Dec 2023',
        'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024', 'Jul 2024'],
    datasets: [{
        label: 'Weekly COVID-19 Cases',
        data: [100000, 600000, 300000, 400000, 150000, 200000, 350000, 250000, 100000, 50000, 80000, 90000, 62000],
        backgroundColor: 'rgba(54, 162, 235, 0.5)', // Màu nền biểu đồ
        borderColor: 'rgba(54, 162, 235, 1)', // Màu đường viền
        borderWidth: 2,
        fill: true,
        tension: 0.4
    }]
};

// Cấu hình biểu đồ
const config = {
    type: 'line',
    data: data,
    options: {
        plugins: {
            tooltip: {
                enabled: true,
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function (context) {
                        return `Week ${context.label}: ${context.formattedValue} cases`;
                    }
                }
            },
            title: {
                display: true,
                text: 'Weekly COVID-19 Cases (WHO Data)',
                font: {
                    size: 16
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Number of Cases'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Time Period'
                }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false
        },
        responsive: true
    },
    plugins: [{
        id: 'hoverColumn',
        beforeDraw: (chart) => {
            const ctx = chart.ctx;
            const activePoints = chart.tooltip?.dataPoints;

            if (activePoints && activePoints.length) {
                const x = activePoints[0].element.x; // Tọa độ x của điểm hover
                const topY = chart.scales.y.top;      // Đỉnh của cột
                const bottomY = chart.scales.y.bottom; // Đáy của cột
                const barWidth = 20; // Chiều rộng của cột

                // Vẽ cột màu
                ctx.save();
                ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'; // Màu của cột khi hover
                ctx.fillRect(x - barWidth / 2, topY, barWidth, bottomY - topY);
                ctx.restore();
            }
        }
    }]
};

// Tạo biểu đồ
new Chart(ctx, config);