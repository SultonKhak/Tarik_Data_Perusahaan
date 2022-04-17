import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
import pandas as pd
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Kemnaker")

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

github_adapter = HTTPAdapter(max_retries=3)

session = requests.Session()
session.mount('https://karirhub.kemnaker.go.id/', github_adapter)

workbook = Workbook()
sheet = workbook.active

def start_scrapping():

    # number = 2
    # 3824
    for i in range(1005):
        url = "https://karirhub-api.kemnaker.go.id/v1/available-companies?page=" + str(i) + "&limit=1&is_ssw=false"

        try:
            respone = session.get(url, headers=headers)
        except ConnectionError as ce:
            print(ce)

        while respone.status_code < 200:
            respone = requests.get(url)
            print(respone.status_code)

        if (respone.text == ''):
            data = []
        else:
            data = respone.json()

        if data:
            perusahaan = data["data"][0]["name"]
            sektor = data["data"][0]["industry"]["name"]
            alamat = data["data"][0]["region"]["name"]
            print(perusahaan)
            print(sektor)
            print(alamat)

            mycursor = mydb.cursor()
            sql = "INSERT INTO kemnaker.kemnaker() VALUES (%s,%s,%s)"
            print(sql)
            val = (perusahaan, sektor, alamat)
            print(val)
            mycursor.execute(sql, val)
            print("====================")

            mydb.commit()

start_scrapping()

