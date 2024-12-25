import pandas as pd

class DataHelper:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.read_csv_to_dataframe()
        self.continents = self.initContinents()
        self.local_continents = {k: [c.lower().strip() for c in v] for k, v in self.continents.items()}
            
    def read_csv_to_dataframe(self):
        file_path = self.data_path
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.lower().str.strip()
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce') 
            return df
        
        except FileNotFoundError:
            print(f"Không tìm thấy tệp: {file_path}")
            return None
        
        except Exception as e:
            print(f"Đã xảy ra lỗi khi đọc tệp {file_path}: {e}")
            return None


    def initContinents(self):
        continents = {
            "africa": [
                "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Cape Verde", 
               "Central African Republic", "Chad", "Comoros", "Congo", "Djibouti", "Egypt", "Equatorial Guinea", 
               "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Kenya", 
               "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", 
               "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", 
               "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", 
               "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
            ],
            "asia": [
                "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", 
                "China", "Cyprus", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", 
                "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", 
                "Nepal", "North Korea", "Oman", "Pakistan", "Palestine", "Philippines", "Qatar", "Saudi Arabia", 
                "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Timor-Leste", "Turkey", 
                "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"
            ],
            "europe": [
                "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", 
               "Croatia", "Cyprus", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", 
               "Hungary", "Iceland", "Ireland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", 
               "Luxembourg", "Malta", "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", 
               "Norway", "Poland", "Portugal", "Romania", "Russia", "San Marino", "Serbia", "Slovakia", 
               "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom", "Vatican"
            ],
            "northamerica": [
                "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", 
                "Dominica", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", 
                "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Kitts and Nevis", "Saint Lucia", 
                "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"
            ],
            "southamerica": [
                "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", 
                "Peru", "Suriname", "Uruguay", "Venezuela"
            ],
            "oceania": [
                "Australia", "Fiji", "Kiribati", "Marshall Islands", "Micronesia (country)", "Nauru", "New Zealand", 
                "Palau", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Tuvalu", "Vanuatu"
            ]
        }
        return continents

    def get_countries_in_continent(self, continent):
        continent = continent.lower().strip()
        return self.local_continents.get(continent, [])

 

