from flask import Flask, request, jsonify
import pandas as pd
from owid import catalog

app = Flask(__name__)

def read_csv_to_dataframe(file_paths):
    """
    Reads multiple CSV files into a dictionary of DataFrames.
    :param file_paths: List of file paths to read.
    :return: Dictionary where keys are filenames (without extensions) and values are DataFrames.
    """
    data_df = {}
    for file_path in file_paths:
        try:
            # Read CSV into DataFrame
            df = pd.read_csv(file_path)
            
            # Normalize column names: lowercase and strip extra spaces
            df.columns = df.columns.str.lower().str.strip()
            
            # Use file name (without extension) as dictionary key
            file_name = file_path.split("/")[-1].replace(".csv", "").lower()
            data_df[file_name] = df
        except FileNotFoundError:
            print(f"Không tìm thấy tệp: {file_path}")
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đọc tệp {file_path}: {e}")
    return data_df

# File paths to CSVs
file_paths = [
    # Case data
    "D:/CPR/Case/new_cases.csv",
    "D:/CPR/Case/Case_age_sex.csv",
    # Deaths data
    "D:/CPR/Deaths/new_deaths.csv",
    "D:/CPR/Deaths/Deaths_age_sex.csv",
    # Vaccination data
    "D:/CPR/vacccin_full_location/vaccinations-by-age-group.csv",
    "D:/CPR/vacccin_full_location/vaccinations.csv"
]

# Read data into a dictionary
data = read_csv_to_dataframe(file_paths)

# Access DataFrames with normalized keys
# Case data
data_case = data.get('new_cases', pd.DataFrame())
data_case_age_sex = data.get('case_age_sex', pd.DataFrame())
# Deaths data
data_deaths = data.get('new_deaths', pd.DataFrame())
data_deaths_age_sex = data.get('deaths_age_sex', pd.DataFrame())
# Vaccination data
data_vaccinations = data.get('vaccinations', pd.DataFrame())
data_vaccinations_age_sex = data.get('vaccinations-by-age-group', pd.DataFrame())


continents = {
    "africa": ["Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", 
               "Central African Republic", "Chad", "Comoros", "Congo", "Djibouti", "Egypt", "Equatorial Guinea", 
               "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", 
               "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", 
               "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", 
               "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", 
               "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"],
    }

#  Hàm trả về dữ liệu trong ngày Case
@app.route("/get_case", methods=["GET"])
def get_case():
    location = request.args.get('location', "").lower()
    result = []
    local_continents = {k: [c.lower().strip() for c in v] for k, v in continents.items()}
    data_case['date'] = pd.to_datetime(data_case['date'], errors='coerce')
    if location == "world":
        for _, row in data_case.iterrows():
            if pd.notna(row['date']):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {country: row[country] if pd.notna(row[country]) else 0 for country in data_case.columns[1:]}
                }
                result.append(daily_data)
    elif location in local_continents:
        countries_in_continent = local_continents[location]
        available_countries = [c for c in countries_in_continent if c in data_case.columns]
        if not available_countries:
            return jsonify({"message": f"No data found for the continent '{location}'."}), 404
        for _, row in data_case.iterrows():
            if pd.notna(row["date"]):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {}
                }
                for country in available_countries:
                    daily_data["countries"][country] = row[country] if pd.notna(row[country]) else 0
                if daily_data["countries"]:
                    result.append(daily_data)
    elif location in data_case.columns:
        for _, row in data_case.iterrows():
            if pd.notna(row['date']):
                result.append({
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "new_cases": row[location]
                })
    else:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    if not result:
        return jsonify({"message": f"No data found for location '{location}'."}), 404
    return jsonify(result)
@app.route("/get_sum_case", methods=["GET"])
def get_sum_case():
    location = request.args.get("location", "").lower() 
    result = []
    data_case["date"] = pd.to_datetime(data_case["date"], errors='coerce')
    local_continents = {k: [c.lower().strip() for c in v] for k, v in continents.items()}
    if location == "world":
        data_case["month_year"] = data_case["date"].dt.to_period("M")
        monthly_data = data_case.groupby("month_year").sum(numeric_only=True).reset_index()
        for _, row in monthly_data.iterrows():
            result.append({
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "total_new_cases": row.sum()  # Tổng tất cả các quốc gia trong tháng
            })

    elif location in local_continents:
        countries_in_continent = local_continents[location]
        available_countries = [c for c in countries_in_continent if c in data_case.columns]

        if not available_countries:
            return jsonify({"message": f"No data found for continent '{location}'."}), 404
        data_case["month_year"] = data_case["date"].dt.to_period("M")
        monthly_data = data_case.groupby("month_year")[available_countries].sum().reset_index()
        for _, row in monthly_data.iterrows():
            month_data = {
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "countries": []  # Mảng chứa thông tin các quốc gia trong tháng đó
            }
            for country in available_countries:
                month_data["countries"].append({
                    "country": country,  # Tên quốc gia
                    "total_new_cases": row[country]  # Tổng số ca của quốc gia trong tháng
                })
            result.append(month_data)
    elif location in data_case.columns:
        data_case["month_year"] = data_case["date"].dt.to_period("M")
        monthly_data = data_case.groupby("month_year")[location].sum().reset_index()
        for _, row in monthly_data.iterrows():
            result.append({
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "total_new_cases": row[location]  # Tổng số ca mới trong tháng
            })
    else:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    if not result:
        return jsonify({"message": f"No data found for location '{location}'."}), 404
    return jsonify(result)
@app.route("/get_yearly_case", methods=["GET"])
def get_yearly_case():
    location = request.args.get("location", "").lower()
    result = []

    # Đảm bảo cột 'date' là kiểu datetime
    data_case["date"] = pd.to_datetime(data_case["date"], errors='coerce')

    # Chuẩn hóa danh sách các quốc gia theo châu lục
    local_continents = {k: [c.lower().strip() for c in v] for k, v in continents.items()}

    if location == "world":
        # Tạo cột 'year' để nhóm theo năm
        data_case["year"] = data_case["date"].dt.year

        # Tổng hợp số ca mới trên toàn thế giới theo năm
        yearly_data = data_case.groupby("year").sum(numeric_only=True).reset_index()

        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in yearly_data.iterrows():
            result.append({
                "year": row["year"].item(),
                "total_new_cases": row.sum()  # Tổng tất cả các quốc gia
            })

    elif location in local_continents:
        countries_in_continent = local_continents[location]

        # Lọc các quốc gia thuộc châu lục có trong data_case
        available_countries = [c for c in countries_in_continent if c in data_case.columns]

        if not available_countries:
            return jsonify({"message": f"No data found for continent '{location}'."}), 404

        # Tạo cột 'year' để nhóm theo năm
        data_case["year"] = data_case["date"].dt.year

        # Tổng hợp số ca mới cho các quốc gia thuộc châu lục theo năm
        yearly_data = data_case.groupby("year")[available_countries].sum().reset_index()

        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in yearly_data.iterrows():
            result.append({
                "year": row["year"].item(),
                "total_new_cases": row[available_countries].sum()  # Tổng số ca của châu lục
            })

    elif location in data_case.columns:
        # Tạo cột 'year' để nhóm theo năm
        data_case["year"] = data_case["date"].dt.year

        # Tổng hợp số ca mới cho quốc gia riêng lẻ theo năm
        yearly_data = data_case.groupby("year")[location].sum().reset_index()

        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in yearly_data.iterrows():
            result.append({
                "year": row["year"].item(),
                "total_new_cases": row[location].item()
            })

    else:
        # Nếu không tìm thấy quốc gia/châu lục trong dữ liệu
        return jsonify({"message": f"Location '{location}' not found"}), 404

    if not result:
        return jsonify({"message": f"No data found for location '{location}'."}), 404

    return jsonify(result)
@app.route("/get_cases_by_age_sex", methods=["GET"])
def get_cases_by_age_sex():
    location = request.args.get("location", "").lower()
    # Lọc dữ liệu theo địa điểmfiltered_data = data_case_age_sex[
    filtered_data = data_case_age_sex[data_case_age_sex['location'].str.strip().str.lower() == location.strip().lower()]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}, 404)
    
    result = []
    for index, row in filtered_data.iterrows():
        date = row['date']
        # Tạo một dictionary cho từng ngày với dữ liệu nhóm tuổi
        age_data = {
            "date": date,
            "age_groups": {
                "1-10": {
                    "male": row['male_1-10'],
                    "female": row['female_1-10']
                },
                "11-20": {
                    "male": row['male_11-20'],
                    "female": row['female_11-20']
                },
                "21-30": {
                    "male": row['male_21-30'],
                    "female": row['female_21-30']
                },
                "31-40": {
                    "male": row['male_31-40'],
                    "female": row['female_31-40']
                },
                "41-50": {
                    "male": row['male_41-50'],
                    "female": row['female_41-50']
                },
                "51-60": {
                    "male": row['male_51-60'],
                    "female": row['female_51-60']
                },
                "61-70": {
                    "male": row['male_61-70'],
                    "female": row['female_61-70']
                },
                "71-80": {
                    "male": row['male_71-80'],
                    "female": row['female_71-80']
                },
                "80+": {
                    "male": row['male_80+'],
                    "female": row['female_80+']
                }
            }
        }
        result.append(age_data)
    
    return jsonify(result)
@app.route("/get_case_sum_by_age_sex", methods=["GET"])
def get_case_sum_by_age_sex():
    location = request.args.get("location", "").lower()
    filtered_data = data_case_age_sex[
        data_case_age_sex['location'].str.strip().str.lower() == location
    ]
    
    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}), 404
    
    # Đảm bảo rằng cột 'date' ở định dạng datetime
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    # Thêm các cột năm và tháng
    filtered_data['year'] = filtered_data['date'].dt.year
    filtered_data['month'] = filtered_data['date'].dt.month
    
    # Chọn các cột nhóm tuổi
    age_columns = [
        'male_1-10', 'female_1-10', 'male_11-20', 'female_11-20',
        'male_21-30', 'female_21-30', 'male_31-40', 'female_31-40',
        'male_41-50', 'female_41-50', 'male_51-60', 'female_51-60',
        'male_61-70', 'female_61-70', 'male_71-80', 'female_71-80',
        'male_80+', 'female_80+'
    ]
    
    # Nhóm theo năm và tháng và tính tổng cho mỗi nhóm tuổi
    aggregated_data = filtered_data.groupby(['year', 'month'])[age_columns].sum().reset_index()
    
    # Chuyển đổi dữ liệu đã tổng hợp sang định dạng JSON
    result = []
    for _, row in aggregated_data.iterrows():
        age_totals = {
            "year": int(row['year']),
            "month": int(row['month']),
            "age_totals": {
                "1-10": {
                    "male": int(row['male_1-10']),  # Chuyển đổi sang int
                    "female": int(row['female_1-10'])  # Chuyển đổi sang int
                },
                "11-20": {
                    "male": int(row['male_11-20']),
                    "female": int(row['female_11-20'])
                },
                "21-30": {
                    "male": int(row['male_21-30']),
                    "female": int(row['female_21-30'])
                },
                "31-40": {
                    "male": int(row['male_31-40']),
                    "female": int(row['female_31-40'])
                },
                "41-50": {
                    "male": int(row['male_41-50']),
                    "female": int(row['female_41-50'])
                },
                "51-60": {
                    "male": int(row['male_51-60']),
                    "female": int(row['female_51-60'])
                },
                "61-70": {
                    "male": int(row['male_61-70']),
                    "female": int(row['female_61-70'])
                },
                "71-80": {
                    "male": int(row['male_71-80']),
                    "female": int(row['female_71-80'])
                },
                "80+": {
                    "male": int(row['male_80+']),
                    "female": int(row['female_80+'])
                }
            }
        }
        result.append(age_totals)
    
    return jsonify(result)   
@app.route("/get_case_sum_year_by_age_sex", methods=["GET"])
def get_case_sum_year_by_age_sex():
    location = request.args.get("location", "").lower()
    
    # Filter data for the specified location
    filtered_data = data_case_age_sex[
        data_case_age_sex['location'].str.strip().str.lower() == location
    ]
    
    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}), 404
    
    # Ensure the 'date' column is in datetime format
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    # Add the year column
    filtered_data['year'] = filtered_data['date'].dt.year
    
    # Select age group columns
    age_columns = [
        'male_1-10', 'female_1-10', 'male_11-20', 'female_11-20',
        'male_21-30', 'female_21-30', 'male_31-40', 'female_31-40',
        'male_41-50', 'female_41-50', 'male_51-60', 'female_51-60',
        'male_61-70', 'female_61-70', 'male_71-80', 'female_71-80',
        'male_80+', 'female_80+'
    ]
    
    # Group by year and calculate the total for each age group
    aggregated_data = filtered_data.groupby(['year'])[age_columns].sum().reset_index()
    
    # Convert the aggregated data to JSON format
    result = []
    for _, row in aggregated_data.iterrows():
        age_totals = {
            "year": int(row['year']),
            "age_totals": {
                "1-10": {
                    "male": int(row['male_1-10']),
                    "female": int(row['female_1-10'])
                },
                "11-20": {
                    "male": int(row['male_11-20']),
                    "female": int(row['female_11-20'])
                },
                "21-30": {
                    "male": int(row['male_21-30']),
                    "female": int(row['female_21-30'])
                },
                "31-40": {
                    "male": int(row['male_31-40']),
                    "female": int(row['female_31-40'])
                },
                "41-50": {
                    "male": int(row['male_41-50']),
                    "female": int(row['female_41-50'])
                },
                "51-60": {
                    "male": int(row['male_51-60']),
                    "female": int(row['female_51-60'])
                },
                "61-70": {
                    "male": int(row['male_61-70']),
                    "female": int(row['female_61-70'])
                },
                "71-80": {
                    "male": int(row['male_71-80']),
                    "female": int(row['female_71-80'])
                },
                "80+": {
                    "male": int(row['male_80+']),
                    "female": int(row['female_80+'])
                }
            }
        }
        result.append(age_totals)
    
    return jsonify(result)
@app.route("/get_deaths", methods=["GET"])
def get_deaths():
    location = request.args.get('location', "").lower()
    result = []

    # Chuẩn hóa danh sách các quốc gia của châu lục
    local_continents = {k: [c.lower().strip() for c in v] for k, v in continents.items()}

    # Kiểm tra nếu 'date' không phải datetime, chuyển đổi
    data_deaths['date'] = pd.to_datetime(data_deaths['date'], errors='coerce')

    if location == "world":
        for _, row in data_deaths.iterrows():
            if pd.notna(row['date']):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {country: row[country] if pd.notna(row[country]) else 0 for country in data_deaths.columns[1:]}
                }
                result.append(daily_data)
    elif location in local_continents:
        countries_in_continent = local_continents[location]

        # Kiểm tra quốc gia trong DataFrame
        available_countries = [c for c in countries_in_continent if c in data_case.columns]
        missing_countries = [c for c in countries_in_continent if c not in data_case.columns]

        print("Available countries:", available_countries)  # Debug
        print("Missing countries:", missing_countries)  # Debug

        if not available_countries:
            return jsonify({"message": f"No data found for the continent '{location}'."}), 404

        for _, row in data_deaths.iterrows():
            if pd.notna(row["date"]):
                daily_data = {
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "countries": {}
                }

                for country in available_countries:
                    daily_data["countries"][country] = row[country] if pd.notna(row[country]) else 0

                if daily_data["countries"]:
                    result.append(daily_data)
    elif location in data_deaths.columns:
        for _, row in data_deaths.iterrows():
            if pd.notna(row['date']):
                result.append({
                    "date": row['date'].strftime("%Y-%m-%d"),
                    "new_cases": row[location]
                })
    else:
        return jsonify({"message": f"Location '{location}' not found"}), 404

    if not result:
        return jsonify({"message": f"No data found for location '{location}'."}), 404

    return jsonify(result)
@app.route("/get_sum_deaths", methods=["GET"])
def get_sum_deaths():
    location = request.args.get("location", "").lower() 
    result = []

    # Đảm bảo cột 'date' là kiểu datetime
    data_deaths["date"] = pd.to_datetime(data_deaths["date"], errors='coerce')

    # Chuẩn hóa danh sách các quốc gia theo châu lục
    local_continents = {k: [c.lower().strip() for c in v] for k, v in continents.items()}

    if location == "world":
        # Tạo cột tháng-năm để nhóm theo tháng và năm
        data_deaths["month_year"] = data_deaths["date"].dt.to_period("M")

        # Tổng hợp số ca mới trên toàn thế giới theo tháng-năm
        monthly_data = data_deaths.groupby("month_year").sum(numeric_only=True).reset_index()

        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in monthly_data.iterrows():
            result.append({
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "total_new_cases": row.sum()  # Tổng tất cả các quốc gia trong tháng
            })

    elif location in local_continents:
        countries_in_continent = local_continents[location]

        # Lọc các quốc gia thuộc châu lục có trong data_case
        available_countries = [c for c in countries_in_continent if c in data_deaths.columns]

        if not available_countries:
            return jsonify({"message": f"No data found for continent '{location}'."}), 404

        # Tạo cột tháng-năm để nhóm theo tháng và năm
        data_deaths["month_year"] = data_deaths["date"].dt.to_period("M")

        # Tổng hợp số ca mới cho các quốc gia thuộc châu lục theo tháng-năm
        monthly_data = data_deaths.groupby("month_year")[available_countries].sum().reset_index()

        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in monthly_data.iterrows():
            result.append({
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "total_new_cases": row[available_countries].sum()  # Tổng số ca của châu lục
            })

    elif location in data_deaths.columns:
        # Tạo cột tháng-năm để nhóm theo tháng và năm
        data_deaths["month_year"] = data_deaths["date"].dt.to_period("M")
        # Tổng hợp số ca mới cho quốc gia riêng lẻ theo tháng-năm
        monthly_data = data_deaths.groupby("month_year")[location].sum().reset_index()
        # Lặp qua từng dòng trong kết quả nhóm
        for _, row in monthly_data.iterrows():
            result.append({
                "month_year": str(row["month_year"]),  # Định dạng tháng-năm
                "total_new_cases": row[location]  # Tổng số ca mới trong tháng
            })

    else:
        # Nếu không tìm thấy quốc gia/châu lục trong dữ liệu
        return jsonify({"message": f"Location '{location}' not found"}), 404

    if not result:
        return jsonify({"message": f"No data found for location '{location}'."}), 404

    return jsonify(result)
@app.route("/get_yearly_deaths", methods=["GET"])
def get_yearly_deaths():
    location = request.args.get("location", "").lower() 
    result = []

    # Đảm bảo cột 'date' là kiểu datetime
    data_deaths["date"] = pd.to_datetime(data_deaths["date"], errors='coerce')

    # Kiểm tra xem quốc gia có trong cột DataFrame không
    if location in data_deaths.columns:
        # Tạo cột 'year' để nhóm theo năm
        data_deaths["year"] = data_deaths["date"].dt.year

        # Nhóm dữ liệu theo năm và tính tổng số ca mới cho mỗi năm
        yearly_data = data_deaths.groupby("year")[location].sum().reset_index()

        # Lặp qua từng dòng trong kết quả nhóm và chuyển đổi kiểu dữ liệu từ int64 sang int
        for index, row in yearly_data.iterrows():
            result.append({
                "year": row["year"].item(),  # Chuyển từ int64 sang int bằng .item()
                "total_new_deaths": row[location].item()  # Chuyển từ int64 sang int bằng .item()
            })
    else:
        # Nếu không tìm thấy quốc gia trong cột, trả về thông báo lỗi
        return jsonify({"message": f"Location '{location}' not found"}), 404
    
    return jsonify(result)
@app.route("/get_deaths_by_age_sex", methods=["GET"])
def get_deaths_by_age_sex():
    location = request.args.get("location", "").lower()
    # Lọc dữ liệu theo địa điểmfiltered_data = data_case_age_sex[
    filtered_data = data_deaths_age_sex[data_deaths_age_sex['location'].str.strip().str.lower() == location.strip().lower()]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}, 404)
    
    result = []
    for index, row in filtered_data.iterrows():
        date = row['date']
        # Tạo một dictionary cho từng ngày với dữ liệu nhóm tuổi
        age_data = {
            "date": date,
            "age_groups": {
                "1-10": {
                    "male": row['male_1-10'],
                    "female": row['female_1-10']
                },
                "11-20": {
                    "male": row['male_11-20'],
                    "female": row['female_11-20']
                },
                "21-30": {
                    "male": row['male_21-30'],
                    "female": row['female_21-30']
                },
                "31-40": {
                    "male": row['male_31-40'],
                    "female": row['female_31-40']
                },
                "41-50": {
                    "male": row['male_41-50'],
                    "female": row['female_41-50']
                },
                "51-60": {
                    "male": row['male_51-60'],
                    "female": row['female_51-60']
                },
                "61-70": {
                    "male": row['male_61-70'],
                    "female": row['female_61-70']
                },
                "71-80": {
                    "male": row['male_71-80'],
                    "female": row['female_71-80']
                },
                "80+": {
                    "male": row['male_80+'],
                    "female": row['female_80+']
                }
            }
        }
        result.append(age_data)
    
    return jsonify(result)
    
#Hàm trả về số người  Deaths theo Age và Sex    
@app.route("/get_deaths_sum_by_age_sex", methods=["GET"])
def get_deaths_sum_by_age_sex():
    location = request.args.get("location", "").lower()
    filtered_data = data_deaths_age_sex[
        data_deaths_age_sex['location'].str.strip().str.lower() == location
    ]
    
    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}), 404
    
    # Đảm bảo rằng cột 'date' ở định dạng datetime
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    # Thêm các cột năm và tháng
    filtered_data['year'] = filtered_data['date'].dt.year
    filtered_data['month'] = filtered_data['date'].dt.month
    
    # Chọn các cột nhóm tuổi
    age_columns = [
        'male_1-10', 'female_1-10', 'male_11-20', 'female_11-20',
        'male_21-30', 'female_21-30', 'male_31-40', 'female_31-40',
        'male_41-50', 'female_41-50', 'male_51-60', 'female_51-60',
        'male_61-70', 'female_61-70', 'male_71-80', 'female_71-80',
        'male_80+', 'female_80+'
    ]
    
    # Nhóm theo năm và tháng và tính tổng cho mỗi nhóm tuổi
    aggregated_data = filtered_data.groupby(['year', 'month'])[age_columns].sum().reset_index()
    
    # Chuyển đổi dữ liệu đã tổng hợp sang định dạng JSON
    result = []
    for _, row in aggregated_data.iterrows():
        age_totals = {
            "year": int(row['year']),
            "month": int(row['month']),
            "age_totals": {
                "1-10": {
                    "male": int(row['male_1-10']),  # Chuyển đổi sang int
                    "female": int(row['female_1-10'])  # Chuyển đổi sang int
                },
                "11-20": {
                    "male": int(row['male_11-20']),
                    "female": int(row['female_11-20'])
                },
                "21-30": {
                    "male": int(row['male_21-30']),
                    "female": int(row['female_21-30'])
                },
                "31-40": {
                    "male": int(row['male_31-40']),
                    "female": int(row['female_31-40'])
                },
                "41-50": {
                    "male": int(row['male_41-50']),
                    "female": int(row['female_41-50'])
                },
                "51-60": {
                    "male": int(row['male_51-60']),
                    "female": int(row['female_51-60'])
                },
                "61-70": {
                    "male": int(row['male_61-70']),
                    "female": int(row['female_61-70'])
                },
                "71-80": {
                    "male": int(row['male_71-80']),
                    "female": int(row['female_71-80'])
                },
                "80+": {
                    "male": int(row['male_80+']),
                    "female": int(row['female_80+'])
                }
            }
        }
        result.append(age_totals)
    
    return jsonify(result)

#Hàm trả về só người Deaths theo Age và Sex của năm 
@app.route("/get_deaths_sum_year_by_age_sex", methods=["GET"])
def get_deaths_sum_year_by_age_sex():
    location = request.args.get("location", "").lower()
    
    # Filter data for the specified location
    filtered_data = data_deaths_age_sex[
        data_deaths_age_sex['location'].str.strip().str.lower() == location
    ]
    
    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}), 404
    
    # Ensure the 'date' column is in datetime format
    filtered_data['date'] = pd.to_datetime(filtered_data['date'])
    
    # Add the year column
    filtered_data['year'] = filtered_data['date'].dt.year
    
    # Select age group columns
    age_columns = [
        'male_1-10', 'female_1-10', 'male_11-20', 'female_11-20',
        'male_21-30', 'female_21-30', 'male_31-40', 'female_31-40',
        'male_41-50', 'female_41-50', 'male_51-60', 'female_51-60',
        'male_61-70', 'female_61-70', 'male_71-80', 'female_71-80',
        'male_80+', 'female_80+'
    ]
    
    # Group by year and calculate the total for each age group
    aggregated_data = filtered_data.groupby(['year'])[age_columns].sum().reset_index()
    
    # Convert the aggregated data to JSON format
    result = []
    for _, row in aggregated_data.iterrows():
        age_totals = {
            "year": int(row['year']),
            "age_totals": {
                "1-10": {
                    "male": int(row['male_1-10']),
                    "female": int(row['female_1-10'])
                },
                "11-20": {
                    "male": int(row['male_11-20']),
                    "female": int(row['female_11-20'])
                },
                "21-30": {
                    "male": int(row['male_21-30']),
                    "female": int(row['female_21-30'])
                },
                "31-40": {
                    "male": int(row['male_31-40']),
                    "female": int(row['female_31-40'])
                },
                "41-50": {
                    "male": int(row['male_41-50']),
                    "female": int(row['female_41-50'])
                },
                "51-60": {
                    "male": int(row['male_51-60']),
                    "female": int(row['female_51-60'])
                },
                "61-70": {
                    "male": int(row['male_61-70']),
                    "female": int(row['female_61-70'])
                },
                "71-80": {
                    "male": int(row['male_71-80']),
                    "female": int(row['female_71-80'])
                },
                "80+": {
                    "male": int(row['male_80+']),
                    "female": int(row['female_80+'])
                }
            }
        }
        result.append(age_totals)
    
    return jsonify(result)

#hàm trả về Vaccin theo Age vaf Sex 
@app.route("/get_vaccin_by_age_sex", methods=["GET"])
def get_vaccin_by_age_sex():
    location = request.args.get("location", "").lower()
    # Lọc dữ liệu theo địa điểmfiltered_data = data_case_age_sex[
    filtered_data = data_vaccinations_age_sex[data_vaccinations_age_sex['location'].str.strip().str.lower() == location.strip().lower()]

    if filtered_data.empty:
        return jsonify({"error": "No data found for the specified location"}, 404)
    
    result = []
    for index, row in filtered_data.iterrows():
        date = row['date']
        # Tạo một dictionary cho từng ngày với dữ liệu nhóm tuổi
        age_data = {
            "date": date,
            "age_groups": {
                "1-10": {
                    "male": row['male_1-10'],
                    "female": row['female_1-10']
                },
                "11-20": {
                    "male": row['male_11-20'],
                    "female": row['female_11-20']
                },
                "21-30": {
                    "male": row['male_21-30'],
                    "female": row['female_21-30']
                },
                "31-40": {
                    "male": row['male_31-40'],
                    "female": row['female_31-40']
                },
                "41-50": {
                    "male": row['male_41-50'],
                    "female": row['female_41-50']
                },
                "51-60": {
                    "male": row['male_51-60'],
                    "female": row['female_51-60']
                },
                "61-70": {
                    "male": row['male_61-70'],
                    "female": row['female_61-70']
                },
                "71-80": {
                    "male": row['male_71-80'],
                    "female": row['female_71-80']
                },
                "80+": {
                    "male": row['male_80+'],
                    "female": row['female_80+']
                }
            }
        }
        result.append(age_data)
    
    return jsonify(result)

#hàm trả về  người  đã tiênm ít nhất 1  mũi  vavccin và đã tiêm đầy đủ  mũi vaccin 
@app.route('/get_vaccinations', methods=['GET'])
def get_vaccinations():   
    location = request.args.get("location", "").lower() 
    result = []

    # Đảm bảo cột 'date' là kiểu datetime
    data_vaccinations["date"] = pd.to_datetime(data_vaccinations["date"], errors='coerce')

    # Kiểm tra xem quốc gia có trong cột DataFrame không
    if location in data_vaccinations['location'].str.lower().values:
        # Lọc dữ liệu cho quốc gia đã chỉ định
        filtered_data = data_vaccinations[data_vaccinations['location'].str.lower() == location]

        # Lặp qua các dòng của DataFrame đã lọc để lấy dữ liệu theo từng ngày
        for index, row in filtered_data.iterrows():
            if pd.notna(row["date"]):   
                result.append({
                    "date": row["date"].strftime("%Y-%m-%d"),   
                    "new_people_vaccinated": row["new_people_vaccinated"],
                    "new_people_fully_vaccinated": row["new_people_fully_vaccinated"],
                })
    else:
        # Nếu không tìm thấy quốc gia trong cột, trả về thông báo lỗi
        return jsonify({"message": f"Location '{location}' not found"}), 404
    
    return jsonify(result)
        
        
if __name__ == "__main__":
    app.run(debug=True)
