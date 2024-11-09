from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Đọc dữ liệu từ CSV
df = pd.read_csv("owid-covid-data.csv")
data = df.to_dict()


@app.route("/getdata", methods=["GET"])
def get_data():
    location = request.args.get("location", "")
    result = []
    for index, row in df.iterrows():
        # Check if the location is a string before applying .lower()
        if isinstance(row["location"], str) and row["location"].lower() == location.lower():
            result.append(row.to_dict())
    
    if not result:
        return jsonify({"message": f"Location '{location}' not found"}), 404  
    
    return jsonify(result)
 

#Hàm trả về Case của quốc gia 
@app.route("/get_case", methods=["GET"])
def get_case():
    location = request.args.get("location", "").lower()  
    result = []
    for index, row in df.iterrows():
        if row["location"].lower() == location:
            result.append({
                "location": row["location"],
                "date": row["date"],
                "new_cases": row["new_cases"],
                "total_cases": row["total_cases"]
            })
    if not result:
        return jsonify({"message": f"Location '{location}' not found"}), 404  
    return jsonify(result)  


# Hàm trả về Sum_Case của các tháng 
@app.route("/get_sum_case", methods=["GET"])
def get_sum_case():
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")   
    location = request.args.get("location", "").lower()  
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400
    result = df[df["location"].str.lower() == location]
    if result.empty:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    result["month_year"] = result["date"].dt.to_period("M").astype(str)  
    monthly_new_cases = result.groupby(["location", "month_year"])["new_cases"].sum().reset_index()
    result_list = monthly_new_cases.to_dict(orient="records")
    return jsonify(result_list) 


#Hàm trả về Sum_Case_Year
@app.route("/get_yearly_cases", methods=["GET"])
def get_yearly_cases():
    df["year"] = df["date"].dt.year
    location = request.args.get("location", "").lower() 
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400
    result = df[df["location"].str.lower() == location]
    if result.empty:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    
    yearly_new_cases = result.groupby(["location", "year"])["new_cases"].sum().reset_index()
    result_list = yearly_new_cases.to_dict(orient="records")
    return jsonify(result_list)  

#Hàm trả về Deaths
@app.route("/get_deaths", methods=["GET"])
def get_deaths():
    location = request.args.get("location", "").lower()  
    result = []
    for index, row in df.iterrows():
        if row["location"].lower() == location:
            result.append({
                "location": row["location"],
                "date": row["date"],
                "new_deaths": row["new_deaths"],
                "total_deaths": row["total_deaths"]
            })
    if not result:
        return jsonify({"message": f"Location '{location}' not found"}), 404  
    return jsonify(result)  


# Hàm trả về  Sum_Deaths của các tháng
@app.route("/get_sum_deaths", methods=["GET"])
def get_sum_deaths():
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    location = request.args.get("location", "").lower()  
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400
    result = df[df["location"].str.lower() == location]
    
    if result.empty:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    result["month_year"] = result["date"].dt.to_period("M").astype(str)  
    
    monthly_new_cases = result.groupby(["location", "month_year"])["new_deaths"].sum().reset_index()
    result_list = monthly_new_cases.to_dict(orient="records")

    return jsonify(result_list)  


#hàm trả về Sum_Deaths_Year
@app.route("/get_yearly_deaths", methods=["GET"])
def get_yearly_deaths():
    df["year"] = df["date"].dt.year
    location = request.args.get("location", "").lower()  
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400
    result = df[df["location"].str.lower() == location]
    if result.empty:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    
    yearly_new_cases = result.groupby(["location", "year"])["new_deaths"].sum().reset_index()
    result_list = yearly_new_cases.to_dict(orient="records")

    return jsonify(result_list) 
#Hàm trả về phần trăm  của quốc gia đó trong tháng 
@app.route("/get_percentage", methods=["GET"])
def get_percentage():
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")
    location = request.args.get("location", "").lower()  
    if not location:
        return jsonify({"message": "Location parameter is required"}), 400
    result = df[df["location"].str.lower() == location]
    
    if result.empty:
        return jsonify({"message": f"Location '{location}' not found"}), 404
    result["month_year"] = result["date"].dt.to_period("M").astype(str)  
    
    monthly_new_cases = result.groupby(["location", "month_year"])["people_vaccinated"].sum().reset_index()
    result_list = monthly_new_cases.to_dict(orient="records")

    return jsonify(result_list) 



#hàm trả về số người tiêm đầy đủ số mũi  mỗi ngày 
@app.route("/get_full_vaccin", methods=["GET"])
def get_full_vaccin():
    location = request.args.get("location", "").lower()
    result = []
    for index, row in df.iterrows():
        if isinstance(row["location"], str) and row["location"].lower() == location:
            result.append({
                "location": row["location"],
                "date": row["date"],
                "new_vaccinations": row["new_vaccinations"],
            })
    if not result:
        return jsonify({"message": f"Location '{location}' not found"}), 404  
    
    return jsonify(result)
    
if __name__ == "__main__":
    app.run(debug=True)
