import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# Загрузка данных
data = pd.read_excel("C:/Users/WARNER/Desktop/Cleaned_Balance_Stay.xlsx")
data['Date'] = data['Date'].astype(str).apply(lambda x: '0' + x if len(x) == 6 else x)
data['Date'] = pd.to_datetime(data['Date'], format='%m.%Y')

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
        plt.show()

# Отображение баланса на отдельном графике
plot_and_forecast(data['Balance'], 'Balance', 'blue', 'lightblue')

# Отображение Total income и Total spends на одном графике
plt.figure(figsize=(14, 7))
plot_and_forecast(data['Total income'], 'Total Income', 'blue', 'lightblue', False)
plot_and_forecast(data['Total spends'], 'Total Spends', 'green', 'lightgreen', False)
plt.title('Actual vs Forecasted Income & Spends')
plt.xlabel('Date')
plt.ylabel('Amount')
plt.legend()
plt.grid(True)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 1e-3:.0f}k'))  # Форматирование оси Y
plt.tight_layout()
plt.show()

# Отображение трех прибылей на одной диаграмме
plt.figure(figsize=(14, 7))
plot_and_forecast(data['Restaurant profit'], 'Restaurant Profit', 'blue', 'lightblue', False)
plot_and_forecast(data['Sauna and Bar profit'], 'Sauna and Bar Profit', 'green', 'lightgreen', False)
plot_and_forecast(data['Hotel profit'], 'Hotel Profit', 'red', 'pink', False)
plt.title('Actual vs Forecasted Profits')
plt.xlabel('Date')
plt.ylabel('Profit Amount')
plt.legend()
plt.grid(True)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x * 1e-3:.0f}k'))  # Форматирование оси Y
plt.tight_layout()
plt.show()
