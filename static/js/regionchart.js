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
const exampleData = {
    "Africa": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [1000, 1200, 1300, 100, 1600, 100, 1800, 2000]
    },
    "Americas": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [2000, 2200, 2400, 2600, 2700, 2800, 200, 3000]
    },
    "Europe": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [1500, 1700, 1800, 1900, 200, 210, 2200, 2300]
    },
    "Eastern Mediterranean": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [800, 900, 950, 1000, 1050, 1100, 150, 200]
    },
    "South-East Asia": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [600, 700, 800, 850, 900, 950, 1000, 1050]
    },
    "Western Pacific": {
        "labels": ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8'],
            "data": [400, 500, 600, 650, 700, 750, 800, 850]
    }

};
createAreaChart('africaChart', {
    labels: exampleData.Africa.labels,
    datasets: [{
        label: 'Africa',
        data: exampleData.Africa.data,
        borderColor: '#E95420',
        backgroundColor: 'rgba(233, 84, 32, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
createAreaChart('americasChart', {
    labels: exampleData.Americas.labels,
    datasets: [{
        label: 'Americas',
        data: exampleData.Americas.data,
        borderColor: '#FF5722',
        backgroundColor: 'rgba(255, 87, 34, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
createAreaChart('europeChart', {
    labels: exampleData.Europe.labels,
    datasets: [{
        label: 'Europe',
        data: exampleData.Europe.data,
        borderColor: '#0078D7',
        backgroundColor: 'rgba(0, 120, 215, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
createAreaChart('easternMediterraneanChart', {
    labels: exampleData['Eastern Mediterranean'].labels,
    datasets: [{
        label: 'Eastern Mediterranean',
        data: exampleData['Eastern Mediterranean'].data,
        borderColor: '#A569BD',
        backgroundColor: 'rgba(165, 105, 189, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
createAreaChart('southEastAsiaChart', {
    labels: exampleData['South-East Asia'].labels,
    datasets: [{
        label: 'South-East Asia',
        data: exampleData['South-East Asia'].data,
        borderColor: '#2ECC71',
        backgroundColor: 'rgba(46, 204, 113, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
createAreaChart('westernPacificChart', {
    labels: exampleData['Western Pacific'].labels,
    datasets: [{
        label: 'Western Pacific',
        data: exampleData['Western Pacific'].data,
        borderColor: '#F1C40F',
        backgroundColor: 'rgba(241, 196, 15, 0.2)',
        fill: true,
        pointRadius: 0 
    }]
});
