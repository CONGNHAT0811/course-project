import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_case(location: str, data_helper: DataHelper):
    result = []

    # Nếu location là "world", lấy tất cả quốc gia
    if location == "world":
        for _, row in data_helper.data.iterrows():
            if pd.notna(row['date']):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {country: row[country] if pd.notna(row[country]) else 0 for country in data_helper.data.columns[1:]}
                }
                result.append(daily_data)
        return result

    # Nếu location là một châu lục, lấy dữ liệu cho các quốc gia trong châu lục
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

    # Nếu location là một quốc gia, lấy dữ liệu cho quốc gia đó
    if location in data_helper.data.columns:
        for _, row in data_helper.data.iterrows():
            if pd.notna(row['date']):
                result.append({
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "new_cases": row[location]
                })
        return result

    # Nếu không tìm thấy location
    raise ValueError(f"No data found for location '{location}'.")
