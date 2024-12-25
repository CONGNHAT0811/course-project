from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from handler.DataHelper import DataHelper

from handler.functions.get_case import fn_get_case
from handler.functions.get_case import fn_get_total_case
from handler.functions.get_case import fn_get_total_case_year
from handler.functions.get_case import fn_get_case_continent
from handler.functions.get_case_age_sex import fn_get_case_age_sex

from handler.functions.get_deaths_age_sex import fn_get_deaths_age_sex
from handler.functions.get_deaths import fn_get_deaths
from handler.functions.get_deaths import fn_get_total_deaths_year, fn_get_deaths_continent, fn_get_total_deaths

from handler.functions.get_new_vaccin import fn_get_new_vaccin, fn_get_total_new_vaccin
from handler.functions.get_new_vaccin import fn_get_total_new_vaccin
from handler.functions.get_vaccin_age_sex import fn_get_vaccin_age_sex
from handler.functions.get_vaccin_age_sex import fn_get_total_vaccin_age_sex


app = Flask(__name__)
@app.route("/")
def index():
    
    return render_template("index.html") 


from flask import request, jsonify
import os

#Dùng để vẽ area chart
@app.route("/get_case", methods=["GET"])
def get_case():
    location = request.args.get('location', "").lower()
    year = request.args.get('year', type=int)
    valid_years = [2020, 2021, 2022, 2023, 2024,]
    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "case", "new_cases.csv"))
        result = fn_get_case(location, data_helper, year)
        return jsonify(result)  
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

#Dùng để vẽ Region chart   
@app.route("/get_case_continent", methods=["GET"])
def get_case_continent():
    location = request.args.get('location', "world").lower()
    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "case", "new_cases.csv"))
        result = fn_get_case_continent(location, data_helper)
        
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    
#Dùng để vẽ MapChart và table 
@app.route("/get_total_case", methods=["GET"])
def get_total_case():
    location = request.args.get('location', "").lower()
    year = request.args.get('year', type=int)
    valid_years = [2020, 2021, 2022, 2023, 2024]

    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "case", "new_cases.csv"))
        
        if year and year in valid_years:
            result = fn_get_total_case_year(location, year, data_helper)
        else:
            result = fn_get_total_case(location, data_helper)
            
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
 
        
#dùng để vẽ tháp giới  tính  của case                
@app.route("/get_case_age_sex", methods=["GET"])
def get_case_age_sex():
    location = request.args.get('location', "").lower()
    year = request.args.get('year', type=int)
    valid_years = [2020, 2021, 2022, 2023, 2024]

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "case", "case_age_sex.csv")
        )
        result = fn_get_case_age_sex(location, data_helper, year)
        return jsonify(result), 200  
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

#Dùng để vẽ area chart của deaths
@app.route("/get_deaths", methods=["GET"])
def get_deaths():
    location = request.args.get('location', "").lower()
    year = request.args.get('year', type=int)
    valid_years = [2020, 2021, 2022, 2023, 2024,]

    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "deaths", "new_deaths.csv"))
        result = fn_get_deaths(location, data_helper,year)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


#dùng để vẽ Region chart của deaths
@app.route("/get_deaths_continent", methods=["GET"])
def get_deaths_continent():
    location = request.args.get('location', "world").lower()
    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "deaths", "new_deaths.csv"))
        result = fn_get_deaths_continent(location, data_helper)
        
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

 
#dùng để vẽ mapchart và table của deaths
@app.route("/get_total_deaths", methods=["GET"])
def get_total_deaths():
    location = request.args.get('location', "").lower()
    year = request.args.get('year', type=int)
    valid_years = [2020, 2021, 2022, 2023, 2024]

    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "deaths", "new_deaths.csv"))
        
        if year and year in valid_years:
            result = fn_get_total_deaths_year(location, year, data_helper)
        else:
            result = fn_get_total_deaths(location, data_helper)
            
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

#dùng để vẽ tháp giới tính của deaths
@app.route("/get_deaths_age_sex", methods=["GET"])
def get_deaths_age_sex():
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "deaths", "deaths_age_sex.csv")
        )
        result = fn_get_deaths_age_sex(location, data_helper)
        return jsonify(result), 200 
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404  

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


    
#Hàm lấy ra giá trị New_vaccin        
@app.route("/get_new_vaccin", methods=["GET"])
def get_new_vaccin():
    
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "vacccin_full_location", "vaccinations.csv")
        )
        result = fn_get_new_vaccin(location, data_helper)
        return jsonify(result), 200  
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404  

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500   
    
    
#Ham lấy ra giá trị Vaccin theo tuoi và giới tính    
@app.route("/get_vaccin_age_sex", methods=["GET"])
def get_vaccin_age_sex():
    
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "vacccin_full_location", "vaccinations-by-age-group.csv")
        )
        result = fn_get_vaccin_age_sex(location, data_helper)
        return jsonify(result), 200  
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404  

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500      

    
    
@app.route("/get_total_new_vaccin", methods=["GET"])
def get_total_new_vaccin():
    
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "vacccin_full_location", "vaccinations.csv")
        )
        result = fn_get_total_new_vaccin(location, data_helper)
        return jsonify(result), 200 
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404  

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500      
          
@app.route("/get_total_vaccin_age_sex", methods=["GET"])
def get_total_vaccin_age_sex():
    
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(
            os.path.join(os.getcwd(), "handler", "data", "vacccin_full_location", "vaccinations-by-age-group.csv")
        )
        result = fn_get_total_vaccin_age_sex(location, data_helper)
        return jsonify(result), 200  
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404  

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500      
                    
app.run(debug=True)