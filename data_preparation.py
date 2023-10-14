import pandas as pd

# Загрузка всех листов из Excel-файла
data_path = "C:/Users/WARNER/Desktop/Balance Stay.xlsx"
all_sheets = pd.read_excel(data_path, sheet_name=None)

data_list = []

# Преобразование месяцев в соответствующие номера
month_dict = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
    'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
}

# Обработка каждого листа
for sheet_name, sheet_data in all_sheets.items():
    month_data = {}

    # Преобразование названия листа в формат "месяц.год"
    month = sheet_name.split()[0]
    year = sheet_name.split()[-1]
    month_data['Date'] = month_dict[month] + '.' + year

    # Извлечение данных из ячеек
    month_data['Total income'] = round(sheet_data.iloc[18, 16])
    month_data['Total spends'] = round(sheet_data.iloc[19, 16])
    month_data['Cashier resort'] = sheet_data.iloc[20, 16]
    month_data['Balance'] = sheet_data.iloc[19, 16]
    month_data['Restaurant profit'] = sheet_data.iloc[34, 1]
    month_data['Sauna and Bar profit'] = sheet_data.iloc[34, 5]
    month_data['Hotel profit'] = sheet_data.iloc[34, 9]

    # Заполнение одного значения зарплаты для октября 2022 года вручную
    if sheet_name == "October 2022":
        month_data['Salary'] = 142300
    else:
        month_data['Salary'] = sheet_data.iloc[14 if month == "October" else 13, 13]

    month_data['Extra spends'] = sheet_data.iloc[53, 13]
    month_data['Monthly spends'] = sheet_data.iloc[28, 13]

    data_list.append(month_data)

# Объединение данных в один DataFrame
final_data = pd.DataFrame(data_list)

# Сохранение данных в новый Excel-файл
final_data.to_excel("C:/Users/WARNER/Desktop/Cleaned_Balance_Stay.xlsx", index=False)

print(final_data)
