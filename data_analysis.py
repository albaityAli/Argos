import pandas as pd
import openpyxl


def check_name(cell):
    cell = cell.capitalize()
    return cell


def check_postcode(cell):
    cell = cell.replace(" ", "").upper()
    return cell


def check_numbers(cell):
    return cell.replace('"', "")


df = pd.read_excel("argos_accounts.xlsx", converters={
    'FName': check_name,
    'LName': check_name,
    'Postcode': check_postcode,
    'CardNumber': check_numbers,
    'ExpiryM': check_numbers,
    'ExpiryY': check_numbers,
    'DataComplete': check_name

})
shape = df.shape
rows = []
for i in range(1, shape[0]+1):
    rows.append(i)

