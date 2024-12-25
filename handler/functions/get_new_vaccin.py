import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_new_vaccin(location: str, data_helper: DataHelper, year: str):
    # Chuẩn hóa cột `location`
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    # Chuyển đổi cột `date` về dạng datetime
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')

    # Nếu 'year' không phải 'total', lọc dữ liệu theo năm
    if year != "total":
        # Lọc theo năm cụ thể
        data_helper.data = data_helper.data[data_helper.data['date'].dt.year.astype(str) == year]

    # Xử lý cho 'world'
    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        if year == "total":
            # Tính tổng các trường trong tất cả các năm (tổng tất cả các ngày)
            grouped_data = filtered_data.groupby('location')[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            grouped_data = grouped_data.applymap(abs)  # Áp dụng giá trị tuyệt đối
            result = grouped_data.reset_index().to_dict(orient='records')
        else:
            # Tính tổng các trường trong tất cả các ngày trong năm cụ thể
            grouped_data = filtered_data.groupby('location')[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            grouped_data = grouped_data.applymap(abs)  # Áp dụng giá trị tuyệt đối
            result = grouped_data.reset_index().to_dict(orient='records')

    # Xử lý cho châu lục
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]
        if year == "total":
            # Tính tổng các trường cho từng quốc gia trong khu vực
            grouped_data = filtered_data.groupby('location')[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            grouped_data = grouped_data.applymap(abs)  # Áp dụng giá trị tuyệt đối
            result = grouped_data.reset_index().to_dict(orient='records')
        else:
            # Tính tổng các trường trong tất cả các ngày trong năm cho từng quốc gia trong khu vực
            grouped_data = filtered_data.groupby('location')[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            grouped_data = grouped_data.applymap(abs)  # Áp dụng giá trị tuyệt đối
            result = grouped_data.reset_index().to_dict(orient='records')

    # Xử lý cho quốc gia cụ thể
    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

        if year == "total":
            # Tính tổng các trường cho tất cả các ngày trong tất cả các năm của quốc gia
            total_vaccinated = filtered_data[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            total_vaccinated = total_vaccinated.abs()  # Áp dụng giá trị tuyệt đối
            result = [{
                "location": location,
                "new_people_vaccinated": total_vaccinated['new_people_vaccinated'],
                "new_people_fully_vaccinated": total_vaccinated['new_people_fully_vaccinated']
            }]
        else:
            # Tính tổng các trường trong tất cả các ngày trong năm cụ thể của quốc gia
            total_vaccinated = filtered_data[['new_people_vaccinated', 'new_people_fully_vaccinated']].sum()
            total_vaccinated = total_vaccinated.abs()  # Áp dụng giá trị tuyệt đối
            result = [{
                "location": location,
                "year": year,
                "new_people_vaccinated": total_vaccinated['new_people_vaccinated'],
                "new_people_fully_vaccinated": total_vaccinated['new_people_fully_vaccinated']
            }]

    return result


def fn_get_total_new_vaccin(location: str, data_helper: DataHelper, year: str):
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

    # Xử lý khi year = total, tính tổng trong tất cả các năm
    if year == "total":
        filtered_data = filtered_data.groupby(['location', 'date']).agg({
            'new_people_vaccinated': 'sum',
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

    else:
        # Xử lý khi year là năm cụ thể
        filtered_data = filtered_data[filtered_data['date'].dt.year == int(year)]
        filtered_data = filtered_data.groupby(['location', 'date']).agg({
            'new_people_vaccinated': 'sum',
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

    # Xử lý cho 'world'
    if location == "world":
        # Tính tổng cho tất cả quốc gia trong mỗi ngày
        for date, date_data in filtered_data.groupby('date'):
            total_vaccinated = date_data['new_people_vaccinated'].sum()
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": "world",
                "date": date.strftime("%Y-%m-%d"),
                "new_people_vaccinated": abs(int(total_vaccinated)),
                "new_people_fully_vaccinated": abs(int(total_fully_vaccinated))
            })

        # Lấy dữ liệu của từng quốc gia trong mỗi ngày và tính tổng
        for loc, loc_data in filtered_data.groupby('location'):
            for date, date_data in loc_data.groupby('date'):
                total_loc_vaccinated = date_data['new_people_vaccinated'].sum()
                total_loc_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
                result.append({
                    "location": loc,
                    "date": date.strftime("%Y-%m-%d"),
                    "new_people_vaccinated": abs(int(total_loc_vaccinated)),
                    "new_people_fully_vaccinated": abs(int(total_loc_fully_vaccinated))
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
        
        for date, date_data in filtered_data.groupby('date'):
            total_vaccinated = date_data['new_people_vaccinated'].sum()
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": location,
                "date": date.strftime("%Y-%m-%d"),
                "new_people_vaccinated": abs(int(total_vaccinated)),
                "new_people_fully_vaccinated": abs(int(total_fully_vaccinated))
            })

        # Lấy dữ liệu của từng quốc gia trong châu lục
        for loc, loc_data in filtered_data.groupby('location'):
            for date, date_data in loc_data.groupby('date'):
                total_loc_vaccinated = date_data['new_people_vaccinated'].sum()
                total_loc_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
                result.append({
                    "location": loc,
                    "date": date.strftime("%Y-%m-%d"),
                    "new_people_vaccinated": abs(int(total_loc_vaccinated)),
                    "new_people_fully_vaccinated": abs(int(total_loc_fully_vaccinated))
                })

    # Xử lý cho quốc gia cụ thể
    else:
        filtered_data = filtered_data[filtered_data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

        for date, date_data in filtered_data.groupby('date'):
            total_vaccinated = date_data['new_people_vaccinated'].sum()
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            result.append({
                "location": location,
                "date": date.strftime("%Y-%m-%d"),
                "new_people_vaccinated": abs(int(total_vaccinated)),
                "new_people_fully_vaccinated": abs(int(total_fully_vaccinated))
            })

    return result




 


def fn_get_total_new_vaccin_continent(location: str, data_helper: DataHelper, year: str):
    result = {}

    # Chuẩn hóa cột `location`
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()

    # Chuyển đổi cột `date` về dạng datetime và xử lý giá trị NaT
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]  # Lọc các ngày hợp lệ

    # Thay thế NaN trong các cột số bằng 0
    filtered_data['new_people_vaccinated'] = filtered_data['new_people_vaccinated'].fillna(0)
    filtered_data['new_people_fully_vaccinated'] = filtered_data['new_people_fully_vaccinated'].fillna(0)

    # Xử lý khi year = total, tính tổng trong tất cả các năm
    if year == "total":
        filtered_data = filtered_data.groupby(['location', 'date']).agg({
            'new_people_vaccinated': 'sum',
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()
    else:
        # Xử lý khi year là năm cụ thể
        filtered_data = filtered_data[filtered_data['date'].dt.year == int(year)]
        filtered_data = filtered_data.groupby(['location', 'date']).agg({
            'new_people_vaccinated': 'sum',
            'new_people_fully_vaccinated': 'sum'
        }).reset_index()

    # Xử lý cho 'world'
    if location == "world":
        world_data = {}

        # Lấy dữ liệu tổng hợp theo ngày cho toàn bộ thế giới
        for date, date_data in filtered_data.groupby('date'):
            total_vaccinated = date_data['new_people_vaccinated'].sum()
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            date_str = date.strftime("%Y-%m-%d")
            world_data[date_str] = {
                "new_people_vaccinated": int(total_vaccinated),
                "new_people_fully_vaccinated": int(total_fully_vaccinated)
            }

        result["world"] = world_data

        # Thêm dữ liệu của từng châu lục
        for continent, countries in data_helper.local_continents.items():
            continent_data = filtered_data[filtered_data['location'].isin(countries)]
            continent_data_dict = {}

            for date, date_data in continent_data.groupby('date'):
                total_vaccinated = date_data['new_people_vaccinated'].sum()
                total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
                date_str = date.strftime("%Y-%m-%d")
                continent_data_dict[date_str] = {
                    "new_people_vaccinated": int(total_vaccinated),
                    "new_people_fully_vaccinated": int(total_fully_vaccinated)
                }

            result[continent] = continent_data_dict

    # Return the result for a specific continent if location is not "world"
    elif location in data_helper.local_continents.keys():
        continent_data = filtered_data[filtered_data['location'].isin(data_helper.local_continents[location])]
        continent_data_dict = {}

        for date, date_data in continent_data.groupby('date'):
            total_vaccinated = date_data['new_people_vaccinated'].sum()
            total_fully_vaccinated = date_data['new_people_fully_vaccinated'].sum()
            date_str = date.strftime("%Y-%m-%d")
            continent_data_dict[date_str] = {
                "new_people_vaccinated": int(total_vaccinated),
                "new_people_fully_vaccinated": int(total_fully_vaccinated)
            }

        result[location] = continent_data_dict

    return result
