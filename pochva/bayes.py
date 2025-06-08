import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

def bayes_fc_form(series, n_future=10):
    n = len(series)
    x_bar = np.mean(series)
    s = np.std(series, ddof=1)
    sem = s / np.sqrt(n)
    print(station, sem)
    simultd = t.rvs(df=n-1, loc=x_bar, scale=sem, size=n_future)
    return simultd, x_bar, sem

df_raw = pd.read_excel('pochva_temp_razryv.xlsx') 
df = df_raw.pivot(index='Year', columns='Station', values='Temperature')

stations = df.columns.tolist()

fig, axs = plt.subplots(2, 4, figsize=(16, 8))  
axs = axs.flatten()  

years = np.arange(2015, 2025)
n_future = 10
future_years = np.arange(2025, 2025 + n_future)

for i, station in enumerate(stations):
    series = df[station]

    # Байесовский прогноз
    predictions, x_bar, sem = bayes_fc_form(series, n_future=n_future)

    ax = axs[i]
    ax.plot(years, series.values, 'o-', label='Actual data')
    ax.plot(future_years, predictions, 'x--', label='Forecast')
    ax.fill_betweenx([min(predictions)-1, max(predictions)+1], years[-1], future_years[-1],
                     color='lightgray', alpha=0.3)
    ax.axvline(x=2015, color='red', linestyle='--', label='Break point (2015)')
    ax.set_title(station, fontsize=10)
    ax.grid(True)

    if i % 4 == 0:
        ax.set_ylabel('Temp (°C)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=4, fontsize=10)
# fig.suptitle('Bayesian forecast of winter temperatures by stations (2015-2024)', fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.95]) 
plt.savefig('soil_bayes')

plt.show()
