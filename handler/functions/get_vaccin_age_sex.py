import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_vaccin_age_sex(location: str, data_helper: DataHelper, year: str):
    result = []

    # Chuẩn hóa cột `location`
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    # Chuyển đổi cột `date` về dạng datetime
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')

    # Xử lý cho 'world'
    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        # Tổng hợp giá trị cho 'world'
        aggregated_data = filtered_data.groupby('date').sum(numeric_only=True).reset_index()
        aggregated_data['location'] = 'world'
        filtered_data = aggregated_data

    # Xử lý cho châu lục
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")
        
        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        # Tổng hợp giá trị cho châu lục
        aggregated_data = filtered_data.groupby('date').sum(numeric_only=True).reset_index()
        aggregated_data['location'] = location
        filtered_data = aggregated_data

    # Xử lý cho quốc gia cụ thể
    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")
        
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

    # Nếu năm yêu cầu là 'total', cộng tất cả các năm lại
    if year == "total":
        aggregated_data = filtered_data.sum(numeric_only=True)
        aggregated_data['location'] = location
        aggregated_data['date'] = 'total'
        result.append({
            "location": aggregated_data['location'],
            "date": aggregated_data['date'],
            "age_groups": {
                "1-10": {"male": aggregated_data['male_1-10'], "female": aggregated_data['female_1-10']},
                "11-20": {"male": aggregated_data['male_11-20'], "female": aggregated_data['female_11-20']},
                "21-30": {"male": aggregated_data['male_21-30'], "female": aggregated_data['female_21-30']},
                "31-40": {"male": aggregated_data['male_31-40'], "female": aggregated_data['female_31-40']},
                "41-50": {"male": aggregated_data['male_41-50'], "female": aggregated_data['female_41-50']},
                "51-60": {"male": aggregated_data['male_51-60'], "female": aggregated_data['female_51-60']},
                "61-70": {"male": aggregated_data['male_61-70'], "female": aggregated_data['female_61-70']},
                "71-80": {"male": aggregated_data['male_71-80'], "female": aggregated_data['female_71-80']},
                "80+": {"male": aggregated_data['male_80+'], "female": aggregated_data['female_80+']}
            }
        })
    else:
        # Nếu year là năm cụ thể, lọc và cộng dồn các giá trị trong năm đó
        filtered_data = filtered_data[filtered_data['date'].dt.year == int(year)]
        aggregated_data = filtered_data.groupby('date').sum(numeric_only=True).reset_index()
        
        # Tổng hợp tất cả các giá trị trong năm cụ thể
        total_data = aggregated_data.sum(numeric_only=True)
        total_data['location'] = location
        total_data['date'] = year

        result.append({
            "location": total_data['location'],
            "date": total_data['date'],
            "age_groups": {
                "1-10": {"male": total_data['male_1-10'], "female": total_data['female_1-10']},
                "11-20": {"male": total_data['male_11-20'], "female": total_data['female_11-20']},
                "21-30": {"male": total_data['male_21-30'], "female": total_data['female_21-30']},
                "31-40": {"male": total_data['male_31-40'], "female": total_data['female_31-40']},
                "41-50": {"male": total_data['male_41-50'], "female": total_data['female_41-50']},
                "51-60": {"male": total_data['male_51-60'], "female": total_data['female_51-60']},
                "61-70": {"male": total_data['male_61-70'], "female": total_data['female_61-70']},
                "71-80": {"male": total_data['male_71-80'], "female": total_data['female_71-80']},
                "80+": {"male": total_data['male_80+'], "female": total_data['female_80+']}
            }
        })

    return result