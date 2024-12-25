import pandas as pd  
from handler.DataHelper import DataHelper

# Function to get the case data for a specific location and year
def fn_get_case_age_sex(location: str, data_helper: DataHelper):
    result = []
    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')

    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")

        filtered_data = filtered_data.sort_values(by=['location', 'date'])

    # Process the data and return the result
    result = filtered_data.apply(lambda row: {
        "location": row['location'],
        "date": row['date'].strftime("%Y-%m-%d"),
        "age_groups": {
            "1-10": {"male": row['male_1-10'], "female": row['female_1-10']},
            "11-20": {"male": row['male_11-20'], "female": row['female_11-20']},
            "21-30": {"male": row['male_21-30'], "female": row['female_21-30']},
            "31-40": {"male": row['male_31-40'], "female": row['female_31-40']},
            "41-50": {"male": row['male_41-50'], "female": row['female_41-50']},
            "51-60": {"male": row['male_51-60'], "female": row['female_51-60']},
            "61-70": {"male": row['male_61-70'], "female": row['female_61-70']},
            "71-80": {"male": row['male_71-80'], "female": row['female_71-80']},
            "80+": {"male": row['male_80+'], "female": row['female_80+']}
        }
    }, axis=1).tolist()

    return result

# Function to get the total case data across all years for a specific location or continent
def fn_get_total_case_age_sex(location: str, data_helper: DataHelper):
    result = []

    data_helper.data['location'] = data_helper.data['location'].str.strip().str.lower()
    location = location.strip().lower()
    data_helper.data['date'] = pd.to_datetime(data_helper.data['date'], errors='coerce')
    filtered_data = None

    total_male = total_female = {age_group: 0 for age_group in ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "80+"]}

    # Case for "world" location
    if location == "world":
        filtered_data = data_helper.data[pd.notna(data_helper.data['date'])]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        for loc, loc_data in filtered_data.groupby('location'):
            for age_group in total_male.keys():
                total_male[age_group] += loc_data[f'male_{age_group}'].sum()
                total_female[age_group] += loc_data[f'female_{age_group}'].sum()
            result.append({
                "location": loc,
                "date": "total",
                "age_groups": {age_group: {"male": int(loc_data[f'male_{age_group}'].sum()), "female": int(loc_data[f'female_{age_group}'].sum())} for age_group in total_male}
            })

        # Adding a world-wide total
        result.append({
            "location": "world",
            "date": "Total",
            "age_groups": {
                age_group: {"male": int(total_male[age_group]), "female": int(total_female[age_group])} 
                for age_group in total_male
            }
        })

    # Case for continent
    elif location in data_helper.local_continents:
        available_countries = [
            country.lower() for country in data_helper.local_continents[location]
            if country.lower() in data_helper.data['location'].values
        ]
        if not available_countries:
            raise ValueError(f"No data found for the continent '{location}'")

        filtered_data = data_helper.data[data_helper.data['location'].isin(available_countries)]
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        for loc, loc_data in filtered_data.groupby('location'):
            for age_group in total_male.keys():
                total_male[age_group] += loc_data[f'male_{age_group}'].sum()
                total_female[age_group] += loc_data[f'female_{age_group}'].sum()
            result.append({
                "location": loc,
                "date": "total",
                "age_groups": {age_group: {"male": int(loc_data[f'male_{age_group}'].sum()), "female": int(loc_data[f'female_{age_group}'].sum())} for age_group in total_male}
            })

        # Adding a continent-wide total
        result.append({
            "location": location,
            "date": "Total",
            "age_groups": {
                age_group: {"male": int(total_male[age_group]), "female": int(total_female[age_group])} 
                for age_group in total_male
            }
        })

    # Case for a specific location
    else:
        filtered_data = data_helper.data[data_helper.data['location'] == location]
        if filtered_data.empty:
            raise ValueError(f"No data found for the specified location '{location}'")
        filtered_data = filtered_data.sort_values(by=['location', 'date'])

        for age_group in total_male.keys():
            total_male[age_group] = int(filtered_data[f'male_{age_group}'].sum())
            total_female[age_group] = int(filtered_data[f'female_{age_group}'].sum())

        result.append({
            "location": location,
            "date": "total",
            "age_groups": {
                age_group: {"male": total_male[age_group], "female": total_female[age_group]}
                for age_group in total_male
            }
        })

    return result
