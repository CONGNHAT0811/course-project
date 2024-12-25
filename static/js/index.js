document.addEventListener("DOMContentLoaded", () => {
    const data = {
        "World": [],
        "Continents": [
            "Asia", "Europe", "Africa", "North America", "South America", "Oceania"
        ],
        "Countries": [
            "Afghanistan", "Algeria", "Albania", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
            "Azerbaijan", "Bahamas", "Bahrain", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bolivia",
            "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Burkina Faso", "Burundi", "Cambodia", "Cameroon",
            "Cape Verde", "Central African Republic", "Chad", "Chile", "China", "Comoros", "Congo", "Costa Rica",
            "Croatia", "Cyprus", "Czechia", "Denmark", "Dominica", "Dominican Republic", "Djibouti", "Egypt",
            "El Salvador", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Finland", "France", "Gabon",
            "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
            "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel",
            "Italy", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
            "Lebanon", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Malawi", "Malaysia", "Maldives",
            "Malta", "Mauritania", "Mauritius", "Mexico", "Moldova", "Monaco", "Montenegro", "Morocco", "Mozambique",
            "Myanmar", "Namibia", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
            "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea",
            "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Saint Kitts and Nevis",
            "Saint Lucia", "Saint Vincent and the Grenadines", "San Marino", "Saudi Arabia", "Senegal", "Seychelles",
            "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Somalia", "South Africa", "South Korea", "South Sudan",
            "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania",
            "Thailand", "Timor-Leste", "Togo", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "United Arab Emirates",
            "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican", "Venezuela", "Vietnam",
            "Yemen", "Zambia", "Zimbabwe"
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
