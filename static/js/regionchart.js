// Hàm tạo biểu đồ với dữ liệu được truyền vào
const createAreaChart = (canvasId, chartData) => {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Weekly COVID-19 Cases by Region',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                },
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false,
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Timeline',
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: 'Number of Cases',
                    },
                    beginAtZero: true,
                },
            },
        },
    });
};

// Lấy dữ liệu từ API
fetch('/get_case_continent')
    .then(response => response.json())
    .then(data => {
        // Chạy hàm tạo biểu đồ cho mỗi khu vực
        createAreaChart('africaChart', {
            labels: data.Africa.labels,
            datasets: [{
                label: 'Africa',
                data: data.Africa.data,
                borderColor: '#E95420',
                backgroundColor: 'rgba(233, 84, 32, 0.2)',
                fill: true,
            }]
        });

        createAreaChart('americasChart', {
            labels: data.Americas.labels,
            datasets: [{
                label: 'Americas',
                data: data.Americas.data,
                borderColor: '#FF5722',
                backgroundColor: 'rgba(255, 87, 34, 0.2)',
                fill: true,
            }]
        });

        createAreaChart('europeChart', {
            labels: data.Europe.labels,
            datasets: [{
                label: 'Europe',
                data: data.Europe.data,
                borderColor: '#0078D7',
                backgroundColor: 'rgba(0, 120, 215, 0.2)',
                fill: true,
            }]
        });

        createAreaChart('easternMediterraneanChart', {
            labels: data['Eastern Mediterranean'].labels,
            datasets: [{
                label: 'Eastern Mediterranean',
                data: data['Eastern Mediterranean'].data,
                borderColor: '#A569BD',
                backgroundColor: 'rgba(165, 105, 189, 0.2)',
                fill: true,
            }]
        });

        createAreaChart('southEastAsiaChart', {
            labels: data['South-East Asia'].labels,
            datasets: [{
                label: 'South-East Asia',
                data: data['South-East Asia'].data,
                borderColor: '#2ECC71',
                backgroundColor: 'rgba(46, 204, 113, 0.2)',
                fill: true,
            }]
        });

        createAreaChart('westernPacificChart', {
            labels: data['Western Pacific'].labels,
            datasets: [{
                label: 'Western Pacific',
                data: data['Western Pacific'].data,
                borderColor: '#F1C40F',
                backgroundColor: 'rgba(241, 196, 15, 0.2)',
                fill: true,
            }]
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
