import pandas as pd
from handler.DataHelper import DataHelper

def fn_get_vaccin(location: str, data_helper: DataHelper, year: str = None):
    try:
        result = []
        
        # Thêm log để debug
        print(f"Processing request for location: {location}, year: {year}")
        
        if location == "world":
            for _, row in data_helper.data.iterrows():
                if pd.notna(row['date']):
                    if year and year != "total" and str(row['date'].year) != str(year):
                        continue
                    
                    total_for_day = 0
                    for country in data_helper.data.columns[1:]:
                        if pd.notna(row[country]):
                            total_for_day += float(row[country])
                    
                    # Thêm data point ngay cả khi total = 0
                    daily_data = {
                        "date": row['date'].strftime("%Y-%m-%d"),
                        "total_cases": float(total_for_day)
                    }
                    result.append(daily_data)
        
        elif location in ["africa", "asia", "europe", "northamerica", "southamerica", "oceania"]:
            
            countries_in_location = data_helper.get_countries_in_continent(location)
            if not countries_in_location:
                print(f"Warning: No countries found for {location}")
                return [{
                    "date": f"{year}-01-01",
                    "total_cases": 0
                }]
            
            print(f"Found {len(countries_in_location)} countries in {location}: {countries_in_location}")
            
            # Kiểm tra xem các quốc gia có tồn tại trong dữ liệu không
            available_countries = [
                country for country in countries_in_location 
                if country in data_helper.data.columns
            ]
            print(f"Available countries in data: {available_countries}")
            
            for _, row in data_helper.data.iterrows():
                if pd.notna(row['date']):
                    if year and year != "total" and str(row['date'].year) != str(year):
                        continue
                    
                    total_for_day = 0
                    valid_count = 0  # Đếm số quốc gia có dữ liệu
                    
                    for country in available_countries:  # Sử dụng available_countries thay vì countries_in_location
                        if pd.notna(row[country]):
                            try:
                                value = float(row[country])
                                total_for_day += value
                                valid_count += 1
                            except (ValueError, TypeError) as e:
                                print(f"Error converting value for {country}: {row[country]}")
                                continue
                    
                    # Chỉ thêm vào kết quả nếu có ít nhất một quốc gia có dữ liệu
                    if valid_count > 0:
                        daily_data = {
                            "date": row['date'].strftime("%Y-%m-%d"),
                            "total_cases": float(total_for_day)
                        }
                        result.append(daily_data)
            
            # Kiểm tra kết quả
            print(f"Generated {len(result)} data points for {location}")
            if not result:
                print(f"Warning: No data points generated for {location}")
                return [{
                    "date": f"{year}-01-01",
                    "total_cases": 0
                }]
        
        else:
            if location not in data_helper.data.columns:
                print(f"Available columns: {data_helper.data.columns}")  # Debug log
                raise ValueError(f"Country not found: {location}")
                
            for _, row in data_helper.data.iterrows():
                if pd.notna(row['date']):
                    if year and year != "total" and str(row['date'].year) != str(year):
                        continue
                    
                    if pd.notna(row[location]):
                        daily_data = {
                            "date": row['date'].strftime("%Y-%m-%d"),
                            "total_cases": float(row[location])
                        }
                        result.append(daily_data)

        # Kiểm tra kết quả
        print(f"Found {len(result)} data points")  # Debug log
        
        if not result:
            # Trả về dữ liệu mẫu thay vì mảng rỗng
            return [{
                "date": f"{year}-01-01",
                "total_cases": 0
            }]

        return sorted(result, key=lambda x: x["date"])
        
    except Exception as e:
        print(f"Error in fn_get_case: {str(e)}")
        # Trả về dữ liệu mẫu trong trường hợp lỗi
        return [{
            "date": f"{year}-01-01",
            "total_cases": 0
        }]

def fn_get_total_vaccin(location: str, data_helper: DataHelper):
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

def fn_get_total_vaccin_year(location: str, year: int, data_helper: DataHelper):
    
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



def fn_get_vaccin_continent(location: str, data_helper: DataHelper, year):
    # Kiểm tra data trước khi xử lý
    if data_helper is None or data_helper.data is None:
        return None
        
    result = {}

    # Lọc dữ liệu theo năm nếu year không phải là "total"
    if year and year != "total":
        data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
        data_helper.data = data_helper.data[
            data_helper.data['date'].dt.year == year
        ]

    # Tính tổng toàn thế giới
    if location == "world":
        # Tổng thế giới từng ngày
        result["world"] = [
            {
                "date": row['date'].strftime("%Y-%m-%d"),
                "total_cases": sum(
                    row[country] if pd.notna(row[country]) else 0
                    for country in data_helper.data.columns[1:]  # Loại bỏ cột 'date'
                )
            }
            for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
        ]

        # Tổng thế giới toàn bộ
        result["world_total"] = sum(
            row[country] if pd.notna(row[country]) else 0
            for _, row in data_helper.data.iterrows()
            for country in data_helper.data.columns[1:]
        )

        # Tính tổng từng châu lục
        for continent, countries in data_helper.local_continents.items():
            available_countries = [country for country in countries if country in data_helper.data.columns]
            if available_countries:
                # Tổng từng ngày
                result[continent] = [
                    {
                        "date": row['date'].strftime("%Y-%m-%d"),
                        "total_cases": sum(
                            row[country] if pd.notna(row[country]) else 0
                            for country in available_countries
                        )
                    }
                    for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
                ]
                # Tổng toàn bộ
                result[f"{continent}_total"] = sum(
                    row[country] if pd.notna(row[country]) else 0
                    for _, row in data_helper.data.iterrows()
                    for country in available_countries
                )

    # Tính tổng cho từng châu lục khi location là một châu lục
    elif location in data_helper.local_continents:
        available_countries = [country for country in data_helper.local_continents[location] if country in data_helper.data.columns]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'.")
        
        # Tổng từng ngày
        result[location] = [
            {
                "date": row['date'].strftime("%Y-%m-%d"),
                "total_cases": sum(
                    row[country] if pd.notna(row[country]) else 0
                    for country in available_countries
                )
            }
            for _, row in data_helper.data.iterrows() if pd.notna(row['date'])
        ]
        # Tổng toàn bộ
        result[f"{location}_total"] = sum(
            row[country] if pd.notna(row[country]) else 0
            for _, row in data_helper.data.iterrows()
            for country in available_countries
        )
    else:
        raise ValueError(f"No data found for location '{location}'.")

    return result
