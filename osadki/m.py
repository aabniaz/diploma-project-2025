import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# mc for 1 station
def monte_carlo(last_value, sen_slope, sem, n_future=10, numb_simlts=1000):
    simlts = np.zeros((numb_simlts, n_future))
    for i in range(numb_simlts):
        future = [last_value]
        for _ in range(n_future):
            next_value = future[-1] + sen_slope + np.random.normal(0, sem)
            future.append(next_value)
        simlts[i, :] = future[1:]  
    return simlts

n_future = 10  
numb_simlts = 1000  
future_years = np.arange(2025, 2025 + n_future)

df_raw = pd.read_excel('osadki1_razryv.xlsx')  
df = df_raw.pivot(index='Year', columns='Station', values='MeanOsadki')

stations = df.columns.tolist()


sen_slopes = {
    'Aral':  np.nan,
    'Zhosaly': 0.010641,
    'Zliha': -0.007679,
    'Kazaly':  0.012296,
    'Karak': -0.017262,
    'Kulandy':  0.003249,
    'Kyzylorda':-0.066731,
    'Shiely': 0.012540
}

sems = {
    'Aral':   0.15729166665000005,
    'Zhosaly':  0.08999877451039402,
    'Zliha': 0.18577747480372292,
    'Kazaly':0.11421801074866585,
    'Karak':  0.15576926610827546,
    'Kulandy': 0.07569496276956963,
    'Kyzylorda':  0.13056210646779304,
    'Shiely':  0.14017395806482857
}

fig, axs = plt.subplots(2, 4, figsize=(16, 8))
axs = axs.flatten()

for i, station in enumerate(stations):
    last_value = df[station].iloc[-1]  
    sen_slope = sen_slopes[station]
    sem = sems[station]

    simlts = monte_carlo(last_value, sen_slope, sem, n_future, numb_simlts)

    # Mean and confidence intervals
    mean_fc = simlts.mean(axis=0)
    lower_b = np.percentile(simlts, 2.5, axis=0)
    upper_b = np.percentile(simlts, 97.5, axis=0)

    ax = axs[i]
    ax.plot(future_years, mean_fc, color='black', label='Average Forecast')
    ax.fill_between(future_years, lower_b, upper_b, color='lightblue', alpha=0.5, label='95% interval')
    ax.set_title(station, fontsize=10)
    ax.grid(True)

    if i % 4 == 0:
        ax.set_ylabel('mean_osadki (mm)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
# fig.suptitle('Monte Carlo forecast of winter temperatures by stations (2025-2034)', fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('snow_montecarlo')

plt.show()