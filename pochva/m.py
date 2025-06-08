import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# mc for 1 station
def monte_carlo_simulation(last_value, sen_slope, sem, n_future=10, numb_simlts=1000):
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

df_raw = pd.read_excel('pochva_temp_razryv.xlsx')  # <-- твой файл
df = df_raw.pivot(index='Year', columns='Station', values='Temperature')

stations = df.columns.tolist()

# sen_slopes = {
#     'Aral': 0.108341,
#     'Zhosaly': 0.046038,
#     'Zliha': 0.203046,
#     'Kazaly': 0.053623,
#     'Karak': 0.104285,
#     'Kulandy': 0.127007,
#     'Kyzylorda': 0.134510,
#     'Shiely': 0.220423
# }

sen_slopes = {
    'Aral':   -0.077778,
    'Zhosaly': 0.171256,
    'Zliha': -0.260572,
    'Kazaly': 0.072685,
    'Karak': -0.127411,
    'Kulandy':  -0.050926,
    'Kyzylorda': -0.162932,
    'Shiely': -0.306827
}

sems = {
    'Aral':   0.9019673069276666,
    'Zhosaly':  0.920910365922455,
    'Zliha': 0.9134875713607992,
    'Kazaly':0.8417624720640777,
    'Karak':  0.861229096249707,
    'Kulandy': 0.8764472406135344,
    'Kyzylorda':  0.8007937268852837,
    'Shiely':  0.638290874391163
}

fig, axs = plt.subplots(2, 4, figsize=(16, 8))
axs = axs.flatten()

for i, station in enumerate(stations):
    last_value = df[station].iloc[-1]   # temp 2024 
    sen_slope = sen_slopes[station]
    sem = sems[station]

    simlts = monte_carlo_simulation(last_value, sen_slope, sem, n_future, numb_simlts)

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
        ax.set_ylabel('Temp (°C)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
# fig.suptitle('Monte Carlo forecast of winter temperatures by stations (2025-2034)', fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('soil_montecarlo')

plt.show()
