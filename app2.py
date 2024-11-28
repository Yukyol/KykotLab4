import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def age_category(age):
    if age < 18:
        return 'younger_18'
    elif 18 <= age <= 45:
        return '18-45'
    elif 45 < age <= 70:
        return '45-70'
    else:
        return 'older_70'

def categorize_employees(csv_filename, xlsx_filename):
    try:
        df = pd.read_csv(csv_filename, encoding='utf-8')
    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV")
        return

    df['Дата народження'] = pd.to_datetime(df['Дата народження'])
    df['Вік'] = df['Дата народження'].apply(
        lambda x: datetime.now().year - x.year - ((datetime.now().month, datetime.now().day) < (x.month, x.day)))
    df['Категорія'] = df['Вік'].apply(age_category)

    try:
        with pd.ExcelWriter(xlsx_filename, engine='openpyxl') as writer:
            df.index += 1
            df.index.name = '№'

            df.to_excel(writer, sheet_name='all', index=True)
            df[df['Категорія'] == 'younger_18'].to_excel(writer, sheet_name='younger_18', index=True)
            df[df['Категорія'] == '18-45'].to_excel(writer, sheet_name='18-45', index=True)
            df[df['Категорія'] == '45-70'].to_excel(writer, sheet_name='45-70', index=True)
            df[df['Категорія'] == 'older_70'].to_excel(writer, sheet_name='older_70', index=True)

        print("Ok")
    except Exception as e:
        print("Повідомлення про неможливість створення XLSX файлу:", str(e))

categorize_employees('employees.csv', 'employees.xlsx')
