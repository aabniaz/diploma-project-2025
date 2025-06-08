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

df_raw = pd.read_excel('pokrov_v_razryv.xlsx')  
df = df_raw.pivot(index='Year', columns='Station', values='MeanSnowDepth')

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
    'Aral':  -0.351516,
    'Zhosaly': 0.261908,
    'Zliha': -0.199573,
    'Kazaly':  0.952681,
    'Karak': 0.010231,
    'Kulandy':  -0.965714,
    'Kyzylorda':0.383966,
    'Shiely': -0.057059
}

sems = {
    'Aral':   0.85163028122841,
    'Zhosaly':  0.26400533890717753,
    'Zliha': 0.763179952572251,
    'Kazaly':0.5758622457741055,
    'Karak':  0.23531661998713232,
    'Kulandy': 1.9315582636537327,
    'Kyzylorda':  0.9728786583401795,
    'Shiely':  0.28050315316451346
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
        ax.set_ylabel('mean_snow_depth  (mm)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=10)
# fig.suptitle('Monte Carlo forecast of winter temperatures by stations (2025-2034)', fontsize=16)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('snow_montecarlo')

plt.show()
