import pandas as pd  
from handler.DataHelper import DataHelper

def fn_get_vaccin_age_sex(location: str, data_helper: DataHelper, year: str):
    result = []
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')

    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]

    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]

    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

    # Thay đổi cách lọc theo năm
    if year != "total":
        try:
            year = int(year)
            # Chỉ lấy dữ liệu của năm được chỉ định
            filtered_data = filtered_data[filtered_data['date'].dt.year == year]
        except ValueError:
            raise ValueError(f"Invalid year: {year}")

    if filtered_data.empty:
        raise ValueError(f"No data found for the specified location and year")

    # Xử lý giá trị thiếu (NaN) bằng cách thay thế bằng 0
    filtered_data = filtered_data.fillna(0)

    # Tính tổng các nhóm tuổi
    age_groups = {
        "1-10": {"male": int(filtered_data['male_1-10'].sum()), "female": int(filtered_data['female_1-10'].sum())},
        "11-20": {"male": int(filtered_data['male_11-20'].sum()), "female": int(filtered_data['female_11-20'].sum())},
        "21-30": {"male": int(filtered_data['male_21-30'].sum()), "female": int(filtered_data['female_21-30'].sum())},
        "31-40": {"male": int(filtered_data['male_31-40'].sum()), "female": int(filtered_data['female_31-40'].sum())},
        "41-50": {"male": int(filtered_data['male_41-50'].sum()), "female": int(filtered_data['female_41-50'].sum())},
        "51-60": {"male": int(filtered_data['male_51-60'].sum()), "female": int(filtered_data['female_51-60'].sum())},
        "61-70": {"male": int(filtered_data['male_61-70'].sum()), "female": int(filtered_data['female_61-70'].sum())},
        "71-80": {"male": int(filtered_data['male_71-80'].sum()), "female": int(filtered_data['female_71-80'].sum())},
        "80+": {"male": int(filtered_data['male_80+'].sum()), "female": int(filtered_data['female_80+'].sum())}
    }

    result = {
        "location": location,
        "year": year,
        "age_groups": age_groups
    }

    return result
