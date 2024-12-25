let tableChart; // Global variable to track the table

function updateTable(caseData) {
    // Convert caseData object to array format
    const countriesData = Object.entries(caseData)
        .filter(([country]) => {
            // Filter out non-country entries
            const nonCountries = ['Year', 'world', 'asia', 'europe', 'africa', 'north america', 
                'south america', 'oceania', 'european union (27)', 'high-income countries', 
                'low-income countries', 'lower-middle-income countries', 'upper-middle-income countries'];
            return !nonCountries.includes(country.toLowerCase());
        })
        .map(([country, cases]) => ({
            country: country.charAt(0).toUpperCase() + country.slice(1), // Capitalize country name
            number: cases
        }))
        .sort((a, b) => b.number - a.number); // Sort by number of cases descending

    const maxNumber = Math.max(...countriesData.map(d => d.number));
    const tableBody = document.getElementById("countryTableBody");
    
    // Clear existing table content
    tableBody.innerHTML = '';

    countriesData.forEach((data) => {
        // Create table row
        const row = document.createElement("tr");

        // Create Country cell (sticky column)
        const countryCell = document.createElement("td");
        countryCell.textContent = data.country;
        countryCell.classList.add("sticky-column");
        row.appendChild(countryCell);

        // Create Number cell with a bar
        const numberCell = document.createElement("td");
        const barContainer = document.createElement("div");
        barContainer.classList.add("bar-container");

        // Create the number value element
        const numberValue = document.createElement("span");
        numberValue.classList.add("number-value");
        numberValue.textContent = data.number.toLocaleString(); // Format number with commas

        // Create the bar element
        const bar = document.createElement("div");
        bar.classList.add("bar");

        // Set bar width based on the number
        bar.style.width = `${(data.number / maxNumber) * 100}%`;

        // Add color class based on value ranges
        if (data.number < 100000) {
            bar.classList.add("low");
        } else if (data.number < 1000000) {
            bar.classList.add("medium");
        } else {
            bar.classList.add("high");
        }

        // Add number value and bar to the number cell
        barContainer.appendChild(numberValue);
        barContainer.appendChild(bar);
        numberCell.appendChild(barContainer);
        row.appendChild(numberCell);

        // Add row to table
        tableBody.appendChild(row);
    });
}

// Modify the existing updateMapChart function to update the table as well
function updateMapChart() {
    const regionSelect = document.getElementById('region-select');
    const yearRadio = document.querySelector('input[name="mapchart_button"]:checked');
    
    const selectedRegion = regionSelect ? regionSelect.value : 'world';
    const selectedYear = yearRadio ? yearRadio.value : '2021';

    fetch(`/get_total_case_year?location=${selectedRegion}&year=${selectedYear}`)
        .then(response => response.json())
        .then(caseData => {
            // Update the map
            // ... (existing map update code) ...

            // Update the table with the same data
            updateTable(caseData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Initial load will be handled by updateMapChart
document.addEventListener('DOMContentLoaded', function() {
    // The existing DOMContentLoaded handler will call updateMapChart
    // which will now update both the map and table
});