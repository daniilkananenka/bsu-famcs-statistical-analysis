import pandas as pd
import numpy as np
import scipy.stats as st

file_path = 'data.csv' 

df = pd.read_csv(file_path, decimal=',')

col_name = 'Индекс'

data = df[col_name].values
n = len(data)

print(f"--- ОБЩИЕ ДАННЫЕ ---")
print(f"Объем выборки (N): {n}")

# Задание 1
mean = np.mean(data)
var = np.var(data, ddof=1)       
std = np.std(data, ddof=1)       
mode = st.mode(data, keepdims=True)[0][0] 
median = np.median(data)         
skewness = st.skew(data, bias=False)  
kurtosis = st.kurtosis(data, bias=False) 

print(f"\n--- 1. БАЗОВЫЕ ХАРАКТЕРИСТИКИ ---")
print(f"Среднее значение: {mean:.4f}")
print(f"Выборочная дисперсия: {var:.4f}")
print(f"СКО: {std:.4f}")
print(f"Мода: {mode:.4f}")
print(f"Медиана: {median:.4f}")
print(f"Коэф. асимметрии: {skewness:.4f}")
print(f"Коэф. эксцесса: {kurtosis:.4f}")

# Задание 2
trim_percent = 0.10 
trunc_mean = st.trim_mean(data, trim_percent)
cv = (std / np.abs(mean)) * 100
mad = np.mean(np.abs(data - mean)) 
rel_linear_dev = (mad / np.abs(mean)) * 100

print(f"\n--- 2. ПОКАЗАТЕЛИ ВАРИАЦИИ ---")
print(f"Усеченное среднее (10%): {trunc_mean:.4f}")
print(f"Коэффициент вариации (V): {cv:.2f}%")
print(f"Относит. линейное отклонение: {rel_linear_dev:.2f}%")

# Задание 3
alpha = 0.05 
z_crit = st.norm.ppf(1 - alpha/2)
margin = z_crit * (std / np.sqrt(n))

ci_lower = mean - margin
ci_upper = mean + margin
print(f"\n--- 3. ДОВЕРИТЕЛЬНЫЙ ИНТЕРВАЛ (95%, Z-критерий) ---")
print(f"Интервал:[{ci_lower:.4f} ; {ci_upper:.4f}]")

# Задание 4
k = int(np.ceil(1 + 3.322 * np.log10(n))) 
obs_freq, bin_edges = np.histogram(data, bins=k)

# Теоретические вероятности
cdf_values = st.norm.cdf(bin_edges, loc=mean, scale=std)
exp_probs = np.diff(cdf_values)

exp_probs[0] = st.norm.cdf(bin_edges[1], loc=mean, scale=std)
exp_probs[-1] = 1.0 - st.norm.cdf(bin_edges[-2], loc=mean, scale=std)

exp_freq = exp_probs * n

ddof = 2
chi_stat, p_value = st.chisquare(f_obs=obs_freq, f_exp=exp_freq, ddof=ddof)

print(f"\n--- 4. КРИТЕРИЙ ПИРСОНА (НА НОРМАЛЬНОСТЬ) ---")
print(f"Число интервалов (k): {k}")
print(f"Границы интервалов: {np.round(bin_edges, 2)}")
print(f"Наблюдаемые частоты (Эмпирические): {obs_freq}")
print(f"Ожидаемые частоты (Теоретические): {np.round(exp_freq, 2)}")
print(f"Статистика Хи-квадрат: {chi_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value > 0.05:
    print("Вывод: Данные подчиняются нормальному распределению.")
else:
    print("Вывод: Данные НЕ подчиняются нормальному распределению.")