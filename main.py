import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from pihmalawi_config import config
from datetime import datetime

def get_org_unit(facility):
    facility = str(facility)
    if facility.lower().startswith("chifunga"):
        return "pciHYsH4glX"
    if facility.lower().startswith("lisungwi"):
        return "jBJ1nrUXKIu"
    if facility.lower().startswith("matope"):
        return "GjNQ12Y2l0F"
    if facility.lower().startswith("midzemba"):
        return "zq5yo5iRvsL"
    if facility.lower().startswith("nkula"):
        return "cfzBcWqPOoy"
    if facility.lower().startswith("zalewa"):
        return "NW5K84KJ4xp"
    if facility.lower().startswith("dambe"):
        return "OhKdUBApLZa"
    if facility.lower().startswith("ligowe"):
        return "gA0WGnhCnYt"
    if facility.lower().startswith("luwani"):
        return "y3FF95NnZzl"
    if facility.lower().startswith("magaleta"):
        return "NFqFeBSH2Re"
    if facility.lower().startswith("matandani"):
        return "JKAFWLrwdji"
    if facility.lower().startswith("neno dh"):
        return "Rmh4wKR794k"
    if facility.lower().startswith("neno parish"):
        return "I4Vox6oteWl"
    if facility.lower().startswith("nsambe"):
        return "HxziIaDjatq"

def get_attribute_option_combo(attributeOptionCombo):
    attributeOptionCombo = str(attributeOptionCombo)
    if attributeOptionCombo.lower()=="yes":
        return "hw3lundkEdl"
    if attributeOptionCombo.lower()=="no":
        return "cKkVX9bH3vB"

if __name__ == '__main__':
    for each_endpoint in config["endpoints"]:
        report_config_df = pd.read_csv(each_endpoint["config_file"])
        report_df = pd.read_excel(each_endpoint["report_file"], header=0)
        report_df["orgUnit"] = report_df["Facility"].apply(get_org_unit)
        report_df["attributeOptionCombo"] = report_df["Event Supported by GAC"].apply(get_attribute_option_combo)
        print(report_df.head())

        for index, row in report_df.iterrows():
            facility_report = {
                "program": report_config_df["program"].iat[0],
                "attributeOptionCombo":row["attributeOptionCombo"],
                "completeDate": str(datetime.today().date()),
                "eventDate": row["Date"].strftime('%Y-%m-%dT%H:%M:%S'),
                "orgUnit": row["orgUnit"],
                "status": "COMPLETED",
                "dataValues": []
            }
            for idx, each_config in report_config_df.iterrows():
                column_name = each_config["excel_column"]
                if column_name in row:
                    data_element = {
                        "dataElement": each_config["program_element_id"],
                        "value": row[column_name]
                    }
                    facility_report["dataValues"].append(data_element)

            print(facility_report)
            url = each_endpoint["base"] + report_config_df["resource"].iat[0]
            username = each_endpoint["username"]
            password = each_endpoint["password"]
            post_result = requests.post(url, json=facility_report,
                                        auth=HTTPBasicAuth(username=username, password=password))
            print(post_result.status_code)
            if post_result.status_code == 200:
                print(post_result.text)
                print("Report for " + row["Facility"] + " has been added in NDP")
            else:
                print("Error loading " + row["Facility"] + ". " + post_result.text)