import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_new_vaccin(location: str, data_helper: DataHelper):
    # Chuẩn hóa cột `location`
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    # Chuyển đổi cột `date` về dạng datetime
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')

    # Xử lý cho 'world'
    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])
        result = filtered_data.apply(lambda row: {
            "location": row['location'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "new_people_vaccinated": row['new_people_vaccinated'],
            "new_people_fully_vaccinated": row['new_people_fully_vaccinated']
        }, axis=1).tolist()

    # Xử lý cho châu lục
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")
        
        filtered_data = data_helper.data[
            data_helper.data['location'].isin(available_countries)
        ]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])
        result = filtered_data.apply(lambda row: {
            "location": row['location'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "new_people_vaccinated": row['new_people_vaccinated'],
            "new_people_fully_vaccinated": row['new_people_fully_vaccinated']
        }, axis=1).tolist()

    # Xử lý cho quốc gia cụ thể
    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")
        
        filtered_data = filtered_data.sort_values(by=['location', 'date'])
        result = filtered_data.apply(lambda row: {
            "date": row['date'].strftime("%Y-%m-%d"),
            "new_people_vaccinated": row['new_people_vaccinated'],
            "new_people_fully_vaccinated": row['new_people_fully_vaccinated']
        }, axis=1).tolist()

    return result

def fn_get_total_new_vaccin(location: str, data_helper: DataHelper):
    result = []

    # Chuẩn hóa cột `location`
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    # Chuyển đổi cột `date` về dạng datetime và xử lý giá trị NaT
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]  # Lọc các ngày hợp lệ

    # Thay thế NaN trong các cột số bằng 0
    filtered_data['new_people_vaccinated'] = filtered_data['new_people_vaccinated'].fillna(0)
    filtered_data['new_people_fully_vaccinated'] = filtered_data['new_people_fully_vaccinated'].fillna(0)

    # Xử lý cho 'world'
    if location == "world":
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        # Tính tổng cho tất cả quốc gia
        total_vaccinated = int(filtered_data['new_people_vaccinated'].sum())  # Chuyển đổi sang int
        total_fully_vaccinated = int(filtered_data['new_people_fully_vaccinated'].sum())  # Chuyển đổi sang int

        # Lấy dữ liệu từng quốc gia và tính tổng
        for loc, loc_data in filtered_data.groupby('location'):
            total_loc_vaccinated = int(loc_data['new_people_vaccinated'].sum())
            total_loc_fully_vaccinated = int(loc_data['new_people_fully_vaccinated'].sum())
            result.append({
                "location": loc,
                "date": "total",
                "new_people_vaccinated": total_loc_vaccinated,
                "new_people_fully_vaccinated": total_loc_fully_vaccinated
            })

        # Thêm tổng vào kết quả cho toàn bộ thế giới
        result.append({
            "location": "world",
            "date": "Total",
            "new_people_vaccinated": total_vaccinated,
            "new_people_fully_vaccinated": total_fully_vaccinated
        })

    # Xử lý cho châu lục
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        # Lọc dữ liệu của các quốc gia trong châu lục
        filtered_data = filtered_data[filtered_data['location'].isin(available_countries)]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        # Tính tổng cho châu lục
        total_vaccinated = int(filtered_data['new_people_vaccinated'].sum())  # Chuyển đổi sang int
        total_fully_vaccinated = int(filtered_data['new_people_fully_vaccinated'].sum())  # Chuyển đổi sang int

        # Lấy dữ liệu từng quốc gia trong châu lục và tính tổng
        for loc, loc_data in filtered_data.groupby('location'):
            total_loc_vaccinated = int(loc_data['new_people_vaccinated'].sum())
            total_loc_fully_vaccinated = int(loc_data['new_people_fully_vaccinated'].sum())
            result.append({
                "location": loc,
                "date": "total",
                "new_people_vaccinated": total_loc_vaccinated,
                "new_people_fully_vaccinated": total_loc_fully_vaccinated
            })

        # Thêm tổng vào kết quả cho châu lục
        result.append({
            "location": location,
            "date": "Total",
            "new_people_vaccinated": total_vaccinated,
            "new_people_fully_vaccinated": total_fully_vaccinated
        })

    # Xử lý cho quốc gia cụ thể
    else:
        filtered_data = filtered_data[filtered_data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

        # Tính tổng cho quốc gia
        total_vaccinated = int(filtered_data['new_people_vaccinated'].sum())  # Chuyển đổi sang int
        total_fully_vaccinated = int(filtered_data['new_people_fully_vaccinated'].sum())  # Chuyển đổi sang int

        result = [{
            "location": location,
            "date": "total",
            "new_people_vaccinated": total_vaccinated,
            "new_people_fully_vaccinated": total_fully_vaccinated
        }]

    return result
