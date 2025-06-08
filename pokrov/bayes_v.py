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
    simltd = t.rvs(df=n-1, loc=x_bar, scale=sem, size=n_future)
    return simltd, x_bar, sem

df_raw = pd.read_excel('pokrov_v_razryv.xlsx')
df = df_raw.pivot(index='Year', columns='Station', values='MeanSnowDepth')

stations = df.columns.tolist()

break_years = {
    'Aral': 2013,
    'Zhosaly': 2020,
    'Zliha': 2015,
    'Kazaly': 2020,
    'Karak': 2007,
    'Kulandy': 2015,
    'Kyzylorda': 2020,
    'Shiely': 2007
}

fig, axs = plt.subplots(2, 4, figsize=(16, 8))
axs = axs.flatten()

n_future = 10  

for i, station in enumerate(stations):
    series = df[station].dropna()

    start_year = series.index.min()  # First real year in station data
    years = series.index.values      # Years of actual data
    future_years = np.arange(years[-1] + 1, years[-1] + 1 + n_future)

    predictions, x_bar, sem = bayes_fc_form(series, n_future=n_future)

    ax = axs[i]
    ax.plot(years, series.values, 'o-', label='Actual data')
    ax.plot(future_years, predictions, 'x--', label='Forecast')

    ax.fill_betweenx([min(predictions)-1, max(predictions)+1], years[-1], future_years[-1],
                     color='lightgray', alpha=0.3)

    if station in break_years:
        ax.axvline(x=break_years[station], color='red', linestyle='--', label='Razryv Year')

    ax.set_title(station, fontsize=10)
    ax.grid(True)

    if i % 4 == 0:
        ax.set_ylabel('mean_snow_depth (mm)')
    if i >= 4:
        ax.set_xlabel('Years')

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=4, fontsize=10)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('snow_bayes')
plt.show()
