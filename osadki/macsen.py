import pandas as pd
import pymannkendall as mk

df = pd.read_excel('osadki1.xlsx')

break_years = {
    'Aral': 2023,
    'Zhosaly': 2008,
    'Zliha': 2014,
    'Kazaly': 2009,
    'Karak': 2007,
    'Kulandy': 2007,
    'Kyzylorda': 2013,
    'Shiely': 2010
}

results = []

stations = df['Station'].unique()
for station in stations:
    station_data = df[df['Station'] == station]
    break_year = break_years[station]

    #divide->before&after
    before = station_data[station_data['Year'] <= break_year]['MeanOsadki'].values
    after = station_data[station_data['Year'] > break_year]['MeanOsadki'].values

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