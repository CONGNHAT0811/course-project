import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_deaths(location: str, data_helper: DataHelper):
    result = []

    if location == "world":
        for _, row in data_helper.data.iterrows():
            if pd.notna(row['date']):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {country: row[country] if pd.notna(row[country]) else 0 for country in data_helper.data.columns[1:]}
                }
                result.append(daily_data)
        return result

    if location in data_helper.local_continents:
        available_countries = [country for country in data_helper.local_continents[location] if country in data_helper.data.columns]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'.")

        for _, row in data_helper.data.iterrows():
            if pd.notna(row['date']):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {country: row[country] if pd.notna(row[country]) else 0 for country in available_countries}
                }
                if daily_data["countries"]:
                    result.append(daily_data)
        return result

    if location in data_helper.data.columns:
        for _, row in data_helper.data.iterrows():
            if pd.notna(row['date']):
                result.append({
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "new_deaths": row[location]
                })
        return result

    raise ValueError(f"No data found for location '{location}'.")

def fn_get_total_deaths(location: str, data_helper: DataHelper):
    total_result = {}

    if location == "world":
        for country in data_helper.data.columns[1:]:
            total_result[country] = int(data_helper.data[country].fillna(0).sum())
        return total_result

    if location in data_helper.local_continents:
        available_countries = [country for country in data_helper.local_continents[location] if country in data_helper.data.columns]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'.")

        for country in available_countries:
            total_result[country] = int(data_helper.data[country].fillna(0).sum())
        return total_result

    if location in data_helper.data.columns:
        total_result[location] = int(data_helper.data[location].fillna(0).sum())
        return total_result

    raise ValueError(f"No data found for location '{location}'.")

def fn_get_total_deaths_year(location: str, year: int, data_helper: DataHelper):
    
    total_result = {}

    if 'date' not in data_helper.data.columns:
        raise ValueError("The dataset does not contain a 'date' column.")
    
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    data_helper.data['Year'] = data_helper.data['date'].dt.year

    data_for_year = data_helper.data[data_helper.data["Year"] == year]
    if data_for_year.empty:
        raise ValueError(f"No data available for the year {year}.")

    if location == "world":
        for country in data_for_year.columns[1:]:
            total_result[country] = int(data_for_year[country].fillna(0).sum())
        return total_result

    if location in data_helper.local_continents:
        available_countries = [country for country in data_helper.local_continents[location] if country in data_for_year.columns]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}' in {year}.")

        for country in available_countries:
            total_result[country] = int(data_for_year[country].fillna(0).sum())
        return total_result

    if location in data_for_year.columns:
        total_result[location] = int(data_for_year[location].fillna(0).sum())
        return total_result

    raise ValueError(f"No data found for location '{location}' in {year}.")


def fn_get_deaths_continent(location: str, data_helper: DataHelper):
    result = {}  

    if location == "world":
        result["world"] = [
            {
                "date": row['date'].strftime("%Y-%m-%d"),
                "total_cases": sum(
                    row[country] if pd.notna(row[country]) else 0
                    for country in data_helper.data.columns[1:]  
                )
            }
            for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
        ]
        
        for continent, countries in data_helper.local_continents.items():
            available_countries = [country for country in countries if country in data_helper.data.columns]
            if available_countries:
                result[continent] = [
                    {
                        "date": row['date'].strftime("%Y-%m-%d"),
                        "total_cases": sum(row[country] if pd.notna(row[country]) else 0 for country in available_countries)
                    }
                    for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
                ]
    elif location in data_helper.local_continents:
        available_countries = [country for country in data_helper.local_continents[location] if country in data_helper.data.columns]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'.")
        
        result[location] = [
            {
                "date": row['date'].strftime("%Y-%m-%d"),
                "total_cases": sum(row[country] if pd.notna(row[country]) else 0 for country in available_countries)
            }
            for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
        ]
    else:
        raise ValueError(f"No data found for location '{location}'.")
    
    return result
