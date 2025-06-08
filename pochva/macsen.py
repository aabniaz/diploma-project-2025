import pandas as pd
import pymannkendall as mk
from scipy.stats import linregress

df = pd.read_excel('pochva_temp.xlsx')

break_years = {
    'Aral': 2015,
    'Zhosaly': 2015,
    'Zliha': 2015,
    'Kazaly': 2015,
    'Karak': 2015,
    'Kulandy': 2015,
    'Kyzylorda': 2015,
    'Shiely': 2015
}

results = []

stations = df['Station'].unique()
for station in stations:
    station_data = df[df['Station'] == station]
    break_year = break_years[station]

    #divide->before&after
    before = station_data[station_data['Year'] <= break_year]['Temperature'].values
    after = station_data[station_data['Year'] > break_year]['Temperature'].values

    # mank&sen's slope before razryva
    if len(before) > 3:  
        mk_res_before = mk.original_test(before)
        sen_slope_before = mk_res_before.slope
    else:
        mk_res_before = None
        slope_before = None

    # mank&sen's slope after razryva
    if len(after) > 3:
        mk_res_after = mk.original_test(after)
        sen_slope_after = mk_res_after.slope
    else:
        mk_res_after = None
        slope_after = None

    # saving res
    results.append({
        'Station': station,
        'BreakYear': break_year,
        'MannK_bef': mk_res_before.trend if mk_res_before else 'Insufficient data',
        'p_bef': mk_res_before.p if mk_res_before else None,
        'SenSlope_bef': mk_res_before.slope if mk_res_before else None,
        'MannK_after': mk_res_after.trend if mk_res_after else 'Insufficient data',
        'p_aft': mk_res_after.p if mk_res_after else None,
        'SenSlope_aft': mk_res_after.slope if mk_res_after else None
    })


results_df = pd.DataFrame(results)
print(results_df)

# results_df.to_excel('macsen.xlsx', index=False)

