document.addEventListener("DOMContentLoaded", () => {
    const data = {
        "World": [],
        "Continents": [
            "Asia", "Europe", "Africa", "North America", "South America", "Oceania"
        ],
        "Countries": [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Australia", "Austria",
            "Bangladesh", "Belgium", "Canada", "China", "Denmark", "Egypt", "France", "Germany", "India",
            "Japan", "Mexico", "Nepal", "Norway", "Pakistan", "United States", "Vietnam"
        ]
    };

    const regionSelect = document.getElementById("region-select");

    const worldOption = document.createElement("option");
    worldOption.value = "world";
    worldOption.textContent = "World";
    worldOption.selected = true;
    regionSelect.appendChild(worldOption);

    const continentGroup = document.createElement("optgroup");
    continentGroup.label = "Continents";
    data.Continents.forEach(continent => {
        const option = document.createElement("option");
        option.value = continent.toLowerCase();
        option.textContent = continent;
        continentGroup.appendChild(option);
    });
    regionSelect.appendChild(continentGroup);

    const countryGroup = document.createElement("optgroup");
    countryGroup.label = "Countries";
    data.Countries.forEach(country => {
        const option = document.createElement("option");
        option.value = country.toLowerCase().replace(/\s+/g, "-");
        option.textContent = country;
        countryGroup.appendChild(option);
    });
    regionSelect.appendChild(countryGroup);
});
