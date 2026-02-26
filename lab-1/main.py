import pandas as pd
import matplotlib.pyplot as plt

file_path = 'data.csv' 

try:
    df = pd.read_csv(file_path, decimal=',')
    
except FileNotFoundError:
    print(f"File '{file_path}' not found")
    raise

# Дискретный вариационный ряд
series = df['Индекс'].value_counts().reset_index()
series.columns = ['x_i', 'm_i']
series = series.sort_values(by='x_i').reset_index(drop=True)

# Характеристики
N = len(df['Индекс'])
series['w_i'] = series['m_i'] / N
series['m_i_cum'] = series['m_i'].cumsum()
series['w_i_cum'] = series['w_i'].cumsum()

series.insert(0, 'group_no', range(1, len(series) + 1))

print("Дискретный вариационный ряд:")
formatted_series = series.copy()
formatted_series['w_i'] = formatted_series['w_i'].round(4)
formatted_series['w_i_cum'] = formatted_series['w_i_cum'].round(4)
print(formatted_series.to_string(index=False))

# Графики
fig, axes = plt.subplots(1, 3, figsize=(14, 6))

# Полигон распределения (по абсолютным частотам m_i)
axes[0].plot(series['x_i'], series['m_i'], marker='o', linestyle='-', color='blue')
axes[0].set_title('Полигон распределения частот')
axes[0].set_xlabel('Значение признака (Индекс)')
axes[0].set_ylabel('Частота ($m_i$)')
axes[0].set_yticks(range(0, int(series['m_i'].max()) + 2)) 
axes[0].grid(True, linestyle='--', alpha=0.7)

# Кумулята (по накопленным абсолютным частотам m_i_cum)
axes[1].plot(series['x_i'], series['m_i_cum'], marker='s', linestyle='-', color='red')
axes[1].set_title('Кумулята абсолютных частот')
axes[1].set_xlabel('Значение признака (Индекс)')
axes[1].set_ylabel('Накопленная частота ($m_i^C$)')
axes[1].set_yticks(range(0, N + 2, 2))
axes[1].grid(True, linestyle='--', alpha=0.7)

# Кумулята (по накопленным относительным частотам w_i_cum)
axes[2].plot(series['x_i'], series['w_i_cum'], marker='s', linestyle='-', color='red')
axes[2].set_title('Кумулята относительных частот')
axes[2].set_xlabel('Значение признака (Индекс)')
axes[2].set_ylabel('Накопленная частота ($w_i^C$)')
axes[2].grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()