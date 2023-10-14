import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from io import BytesIO
import os
from django.conf import settings



# Загрузка всех листов из Excel-файла
data_path = os.path.join(settings.BASE_DIR, 'media', 'Balance_Stay.xlsx')
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
final_data.to_excel(os.path.join(settings.BASE_DIR, "media", "Cleaned_Balance_Stay.xlsx"), index=False)


# Загрузка данных
data = pd.read_excel(os.path.join(settings.BASE_DIR, "media", "Cleaned_Balance_Stay.xlsx"))
data['Date'] = data['Date'].astype(str).apply(lambda x: '0' + x if len(x) == 6 else x)
data['Date'] = pd.to_datetime(data['Date'], format='%m.%Y')

# Функция для создания графиков и прогнозов
def plot_and_forecast(data_column, title, color, forecast_color, is_separate_chart=True):
    # Разделение данных на обучающую и тестовую выборки
    train = data_column[:-5]
    test = data_column[-5:]

    # Создание модели ARIMA
    model = ARIMA(train, order=(5,1,0))

    # Обучение модели
    model_fit = model.fit()

    # Прогнозирование
    forecast = model_fit.forecast(steps=len(test)+26)

    # Визуализация реальных и прогнозируемых значений
    plt.plot(data['Date'], data_column, label=f'Real {title}', marker='o', color=color)
    forecast_dates = pd.date_range(data['Date'].iloc[-1], periods=len(test)+26, freq='M')
    plt.plot(forecast_dates, forecast, label=f'Forecasted {title}', marker='o', color=forecast_color)

    if is_separate_chart:
        plt.title(f'Actual vs Forecasted {title}')
        plt.xlabel('Date')
        plt.ylabel(title)
        plt.legend()
        plt.grid(True)
        plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 1e-3:.0f}k'))  # Форматирование оси Y
        plt.tight_layout()
        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return forecast.tolist(), buf

    return forecast.tolist(), None

def get_forecast(plot_graphs=True):
    if not plot_graphs:
        return [None, None, None]

    # Баланс
    balance_forecast, balance_buf = plot_and_forecast(data['Balance'], 'Balance', 'blue', 'lightblue')

    # Доход и расходы
    plt.figure(figsize=(14, 7))
    income_forecast, income_buf = plot_and_forecast(data['Total income'], 'Total Income', 'blue', 'lightblue', False)
    spends_forecast, spends_buf = plot_and_forecast(data['Total spends'], 'Total Spends', 'green', 'lightgreen', False)
    plt.title('Actual vs Forecasted Income & Spends')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 1e-3:.0f}k'))  # Форматирование оси Y
    income_spends_buf = BytesIO()
    plt.tight_layout()
    plt.savefig(income_spends_buf, format="png")
    plt.close()

    # Прибыль
    plt.figure(figsize=(14, 7))
    restaurant_forecast, restaurant_buf = plot_and_forecast(data['Restaurant profit'], 'Restaurant Profit', 'blue', 'lightblue', False)
    sauna_forecast, sauna_buf = plot_and_forecast(data['Sauna and Bar profit'], 'Sauna and Bar Profit', 'green', 'lightgreen', False)
    hotel_forecast, hotel_buf = plot_and_forecast(data['Hotel profit'], 'Hotel Profit', 'red', 'pink', False)
    plt.title('Actual vs Forecasted Profits')
    plt.xlabel('Date')
    plt.ylabel('Profit Amount')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 1e-3:.0f}k'))  # Форматирование оси Y
    profits_buf = BytesIO()
    plt.tight_layout()
    plt.savefig(profits_buf, format="png")
    plt.close()

    return [balance_buf, income_spends_buf, profits_buf]
