from flask import Flask, request, jsonify
import pandas as pd
import os

from owid import catalog
from handler.DataHelper import DataHelper
from handler.functions.get_case import fn_get_case

app = Flask(__name__)

@app.route("/get_case", methods=["GET"])
def get_case():
    location = request.args.get('location', "").lower()

    try:
        data_helper = DataHelper(os.path.join(os.getcwd(), "handler", "data", "case", "new_cases.csv"))
        result = fn_get_case(location, data_helper)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
        




app.run(debug=True)