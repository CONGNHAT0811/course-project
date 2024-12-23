fetch('https://unpkg.com/world-atlas/countries-50m.json')
    .then((r) => r.json())
    .then((data) => {
        // Extract the countries' features from the topojson data
        const countries = ChartGeo.topojson.feature(data, data.objects.countries).features;

        const exampleData = {
            "United States": 850,
            "Canada": 230,
            "Brazil": 680,
            "China": 920,
            "India": 500,
            "Australia": 450,
            "Russia": 600,
            "Mexico": 400,
            "Germany": 750,
            "France": 700,
            "United Kingdom": 670,
            "Japan": 800,
            "South Korea": 730,
            "Italy": 690,
            "Spain": 680,
            "Argentina": 550,
            "Egypt": 450,
            "South Africa": 470,
            "Nigeria": 600,
            "Saudi Arabia": 640,
            "Indonesia": 520,
            "Pakistan": 490,
            "Bangladesh": 480,
            "Turkey": 560,
            "Vietnam": 510,
            "Thailand": 530,
            "Malaysia": 550,
            "Singapore": 600,
            "Philippines": 570,
            "Chile": 620,
            "Peru": 580,
            "Colombia": 590,
            "Ukraine": 550,
            "Poland": 650,
            "Czech Republic": 620,
            "Romania": 600,
            "Greece": 610,
            "Finland": 580,
            "Portugal": 590,
            "Sweden": 660,
            "Norway": 680,
            "Denmark": 690,
            "Ireland": 700,
            "Switzerland": 750,
            "Netherlands": 740,
            "Belgium": 730,
            "Austria": 720,
            "Luxembourg": 800
        };
        // Create a chart using the 'choropleth' type
        const chart = new Chart(document.getElementById("canvas").getContext("2d"), {
            type: 'choropleth', // Type for choropleth map
            data: {
                labels: countries.map((d) => d.properties.name), // Labels as country names
                datasets: [{
                    label: 'Countries',
                    data: countries.map((d) => ({
                        feature: d,
                        value: exampleData[d.properties.name] || 0 // Use example data for each country
                    })),
                }]
            },
            options: {
                responsive: true, // Ensure the chart is responsive
                showOutline: true, // Show the outlines of the countries
                showGraticule: true, // Show graticule (latitudes and longitudes)
                plugins: {
                    legend: {
                        display: false // Hide the legend, since it's not needed for a choropleth map
                    },
                },
                scales: {
                    projection: {
                        type: 'geo', // Ensures the projection is applied
                        projection: 'equalEarth' // Use the Equal Earth projection for the map
                    }
                }
            }
        });
    });
