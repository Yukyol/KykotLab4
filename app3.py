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

def analyze_csv(csv_filename):
    try:
        df = pd.read_csv(csv_filename, encoding='utf-8')
    except FileNotFoundError:
        print("Повідомлення про відсутність або проблеми при відкритті файлу CSV")
        return

    print("Ok")

    gender_counts = df['Стать'].value_counts()
    print(gender_counts)
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Статевий розподіл')
    plt.show()

    df['Дата народження'] = pd.to_datetime(df['Дата народження'])
    df['Вік'] = df['Дата народження'].apply(lambda x: datetime.now().year - x.year - ((datetime.now().month, datetime.now().day) < (x.month, x.day)))
    df['Категорія'] = df['Вік'].apply(age_category)

    category_counts = df['Категорія'].value_counts()
    print(category_counts)
    category_counts.plot(kind='bar')
    plt.title('Кількість працівників за віковими категоріями')
    plt.show()

    for category in ['younger_18', '18-45', '45-70', 'older_70']:
        sub_df = df[df['Категорія'] == category]
        gender_category_counts = sub_df['Стать'].value_counts()
        print(f"Категорія {category}:")
        print(gender_category_counts)
        gender_category_counts.plot(kind='bar')
        plt.title(f'Статевий розподіл у категорії {category}')
        plt.show()

analyze_csv('employees.csv')