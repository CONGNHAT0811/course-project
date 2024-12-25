import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_new_vaccin(location: str, data_helper: DataHelper, year: str = "total"):
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    if year != "total":
        data_helper.data = data_helper.data[data_helper.data['date'].dt.year.astype(str) == year]
    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        grouped_data = filtered_data.groupby('location')[['new_people_fully_vaccinated']].sum()
        grouped_data = grouped_data.applymap(abs)
        result = grouped_data.reset_index().to_dict(orient='records')
        
        if not isinstance(result, list):
            result = [result]
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]
        grouped_data = filtered_data.groupby('location')[['new_people_fully_vaccinated']].sum()
        grouped_data = grouped_data.applymap(abs)
        result = grouped_data.reset_index().to_dict(orient='records')
        
        if not isinstance(result, list):
            result = [result]
    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

        if year == "total":
            total_vaccinated = filtered_data[['new_people_fully_vaccinated']].sum()
            total_vaccinated = total_vaccinated.abs()
            result = [{
                "location": location,
                "new_people_fully_vaccinated": float(total_vaccinated['new_people_fully_vaccinated'])
            }]
        else:
            total_vaccinated = filtered_data[['new_people_fully_vaccinated']].sum()
            total_vaccinated = total_vaccinated.abs()
            result = [{
                "location": location,
                "year": year,
                "new_people_fully_vaccinated": float(total_vaccinated['new_people_fully_vaccinated'])
            }]

    return result


def fn_get_total_new_vaccin(location: str, data_helper: DataHelper, year: str = "total"):
    result = []
    
    # Chuẩn hóa dữ liệu đầu vào
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()
    
    # Chuyển đổi cột date và lọc dữ liệu hợp lệ
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
    filtered_data['new_people_fully_vaccinated'] = filtered_data['new_people_fully_vaccinated'].fillna(0)
    
    # Lọc theo năm nếu cần
    if year != "total":
        filtered_data = filtered_data[filtered_data['date'].dt.year == int(year)]

    # Xử lý dữ liệu theo location
    if location == "world":
        for date, date_data in filtered_data.groupby('date'):
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": "world",
                "date": date.strftime("%Y-%m-%d"),
                "new_people_fully_vaccinated": int(abs(total_fully_vaccinated))
            })
        return sorted(result, key=lambda x: x['date'])

    elif location in data_helper.local_continents:
        # Lọc dữ liệu theo các quốc gia trong châu lục
        continent_countries = [c.lower() for c in data_helper.local_continents[location]]
        continent_data = filtered_data[filtered_data['location'].isin(continent_countries)]
        
        # Tổng hợp dữ liệu theo ngày
        for date, date_data in continent_data.groupby('date'):
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": location,
                "date": date.strftime("%Y-%m-%d"),
                "new_people_fully_vaccinated": int(abs(total_fully_vaccinated))
            })
        return sorted(result, key=lambda x: x['date'])

    else:
        # Xử lý cho một quốc gia cụ thể
        country_data = filtered_data[filtered_data['location'] == location]
        for date, date_data in country_data.groupby('date'):
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": location,
                "date": date.strftime("%Y-%m-%d"),
                "new_people_fully_vaccinated": int(abs(total_fully_vaccinated))
            })
        return sorted(result, key=lambda x: x['date'])



 
#vẽ area

def fn_get_total_new_vaccin_continent(location: str, data_helper: DataHelper, year: str = "total"):
    # Chuẩn hóa dữ liệu đầu vào
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()
    
    # Chuyển đổi date và lọc dữ liệu
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
    filtered_data['new_people_fully_vaccinated'] = filtered_data['new_people_fully_vaccinated'].fillna(0)

    # Lọc theo năm nếu cần
    if year != "total":
        filtered_data = filtered_data[filtered_data['date'].dt.year == int(year)]

    # Chuẩn bị kết quả dạng array
    result = []

    if location == "world":
        # Tổng hợp dữ liệu theo ngày
        daily_data = filtered_data.groupby('date').agg({
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

        # Chuyển đổi thành array of objects
        for _, row in daily_data.iterrows():
            result.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'total_cases': float(abs(row['new_people_fully_vaccinated']))
            })

    elif location in data_helper.local_continents:
        # Lọc dữ liệu cho châu lục cụ thể
        continent_countries = [c.lower() for c in data_helper.local_continents[location]]
        continent_data = filtered_data[filtered_data['location'].isin(continent_countries)]
        
        # Tổng hợp dữ liệu theo ngày cho châu lục
        daily_data = continent_data.groupby('date').agg({
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

        # Chuyển đổi thành array of objects
        for _, row in daily_data.iterrows():
            result.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'total_cases': float(abs(row['new_people_fully_vaccinated']))
            })

    else:
        # Lọc dữ liệu cho quốc gia cụ thể
        country_data = filtered_data[filtered_data['location'] == location]
        daily_data = country_data.groupby('date').agg({
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

        # Chuyển đổi thành array of objects
        for _, row in daily_data.iterrows():
            result.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'total_cases': float(abs(row['new_people_fully_vaccinated']))
            })

    # Sắp xếp kết quả theo ngày
    result.sort(key=lambda x: x['date'])
    return result
