import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
data = pd.read_excel('C:/Users/WARNER/Desktop/Cleaned_Balance_Stay.xlsx')

# Преобразование значений столбца 'Date' в строковый тип, затем в формат datetime
data['Date'] = data['Date'].astype(str).apply(lambda x: '0' + x if len(x) == 6 else x)  # Добавление ведущего нуля для месяцев 1-9
data['Date'] = pd.to_datetime(data['Date'], format='%m.%Y')

# Сортировка данных по дате
data = data.sort_values(by='Date')

# Установка стиля
sns.set_style("whitegrid")

# 1) Изменение "Total income" и "Total spends" по месяцам
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Date', y='Total income', marker='o', label='Total Income')
sns.lineplot(data=data, x='Date', y='Total spends', marker='o', label='Total Spends')
plt.title('Изменение Total Income и Total Spends по месяцам')
plt.ylabel('Amount')
plt.xlabel('Date')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('total_income_spends.png')
plt.show()

# 2) Изменение "Balance" по месяцам
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Date', y='Balance', marker='o', color='blue')
plt.title('Изменение Balance по месяцам')
plt.ylabel('Amount')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('balance.png')
plt.show()

# 3) Сравнение "Restaurant profit", "Sauna and Bar profit" и "Hotel profit" по месяцам
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Date', y='Restaurant profit', marker='o', label='Restaurant Profit')
sns.lineplot(data=data, x='Date', y='Sauna and Bar profit', marker='o', label='Sauna and Bar Profit')
sns.lineplot(data=data, x='Date', y='Hotel profit', marker='o', label='Hotel Profit')
plt.title('Сравнение Restaurant Profit, Sauna and Bar Profit и Hotel Profit по месяцам')
plt.ylabel('Profit')
plt.xlabel('Date')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('profit_comparison.png')
plt.show()

# 4) Изменение "Extra spends", "Monthly spends", "Cashier resort" и "Salary" по месяцам
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='Date', y='Extra spends', marker='o', label='Extra Spends')
sns.lineplot(data=data, x='Date', y='Monthly spends', marker='o', label='Monthly Spends')
sns.lineplot(data=data, x='Date', y='Cashier resort', marker='o', label='Cashier Resort')
sns.lineplot(data=data, x='Date', y='Salary', marker='o', label='Salary')  # Добавлено изменение Salary
plt.title('Изменение Extra Spends, Monthly Spends, Cashier Resort и Salary по месяцам')
plt.ylabel('Amount')
plt.xlabel('Date')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('spends_salary_comparison.png')
plt.show()
