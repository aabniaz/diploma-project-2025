import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# mc for 1 station
def monte_carlo(last_v, sen_slope, sem, n_future=10, numb_simlts=1000):
    forcts = np.zeros((numb_simlts, n_future))
    for i in range(numb_simlts):
        future = [last_v]
        for _ in range(n_future):
            next_value = future[-1] + sen_slope + np.random.normal(0, sem)
            future.append(next_value)
        forcts[i, :] = future[1:]  
    return forcts

n_future = 10  
numb_simlts = 1000  
future_years = np.arange(2025, 2025 + n_future)

df_raw = pd.read_excel('air_temp_razryv.xlsx')  
df = df_raw.pivot(index='Year', columns='Station', values='Temperature')

stations = df.columns.tolist()


sen_slopes = {
    'Aral':  0.034259,
    'Zhosaly': 0.081645,
    'Zliha': -0.216379,
    'Kazaly': -0.028472,
    'Karak': -0.141111,
    'Kulandy':  -0.165136,
    'Kyzylorda': 0.027748,
    'Shiely': -0.233604
}

sems = {
    'Aral':  0.8988842288583698,
    'Zhosaly': 0.9399644527220183,
    'Zliha': 0.9186464204736037,
    'Kazaly': 0.8723047470404758,
    'Karak': 0.8633232074488641,
    'Kulandy': 0.8206929895320523,
    'Kyzylorda':  0.8599187136074214,
    'Shiely':  0.6467627789664374
}

fig, axs = plt.subplots(2, 4, figsize=(16, 8))
axs = axs.flatten()

for i, station in enumerate(stations):
    last_v = df[station].iloc[-1]  # temp 2024 
    sen_slope = sen_slopes[station]
    sem = sems[station]

    forcts = monte_carlo(last_v, sen_slope, sem, n_future, numb_simlts)

    # mean and confidence intervals
    mean_fc = forcts.mean(axis=0)
    lower_b = np.percentile(forcts, 2.5, axis=0)
    upper_b = np.percentile(forcts, 97.5, axis=0)

    ax = axs[i]
    ax.plot(future_years, mean_fc, color='black', label='Average Forecast')
    ax.fill_between(future_years, lower_b, upper_b, color='lightblue', alpha=0.5, label='95% interval')
    ax.set_title(station, fontsize=10)
    ax.grid(True)

    if i % 4 == 0:
        ax.set_ylabel('Temp (°C)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
# fig.suptitle('Monte Carlo forecast of winter temperatures by stations (2025-2034)', fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('air_montecarlo')
plt.show()
