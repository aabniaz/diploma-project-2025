# import pandas as pd
# import numpy as np
# from pymannkendall import original_test, sens_slope

# df = pd.read_excel('pokrov_v.xlsx')

# break_years = {
#     'Арал тенизи': 2013,
#     'Жосалы': 2020,
#     'Злиха': 2015,
#     'Казалы': 2020,
#     'Карак': 2007,
#     'Куланды': 2015,
#     'Кызылорда': 2020,
#     'Шиели': 2007
# }

# results = []

# for station, break_year in break_years.items():
#     station_df = df[df['Station'] == station]

#     before_break = station_df[station_df['Year'] < break_year]
#     after_break = station_df[station_df['Year'] >= break_year]

#     if len(before_break) >= 8:
#         mk_before = original_test(before_break['MeanSnowDepth'])
#         sen_before = sens_slope(before_break['MeanSnowDepth'])
#         results.append({
#             'Station': station,
#             'Period': f"до {break_year}",
#             'p-value': mk_before.p,
#             'Trend': mk_before.trend,
#             'Sen_slope': sen_before.slope
#         })
#     else:
#         results.append({
#             'Station': station,
#             'Period': f"до {break_year}",
#             'p-value': None,
#             'Trend': 'Мало данных',
#             'Sen_slope': None
#         })

#     if len(after_break) >= 8:
#         mk_after = original_test(after_break['MeanSnowDepth'])
#         sen_after = sens_slope(after_break['MeanSnowDepth'])
#         results.append({
#             'Station': station,
#             'Period': f"с {break_year}",
#             'p-value': mk_after.p,
#             'Trend': mk_after.trend,
#             'Sen_slope': sen_after.slope
#         })
#     else:
#         results.append({
#             'Station': station,
#             'Period': f"с {break_year}",
#             'p-value': None,
#             'Trend': 'Мало данных',
#             'Sen_slope': None
#         })

# results_df = pd.DataFrame(results)

# results_df.to_excel('snowdepth_mk_sen_results.xlsx', index=False)

# print(results_df)


import pandas as pd
import pymannkendall as mk
from scipy.stats import linregress

df = pd.read_excel('pokrov_v.xlsx')

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

results = []

stations = df['Station'].unique()
for station in stations:
    station_data = df[df['Station'] == station]
    break_year = break_years[station]

    #divide->before&after
    before = station_data[station_data['Year'] <= break_year]['MeanSnowDepth'].values
    after = station_data[station_data['Year'] > break_year]['MeanSnowDepth'].values

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
        'MacK_bef': mk_res_before.trend if mk_res_before else 'Insufficient data',
        'p_bef': mk_res_before.p if mk_res_before else None,
        'SenSlope_bef': mk_res_before.slope if mk_res_before else None,
        'MacK_aft': mk_res_after.trend if mk_res_after else 'Insufficient data',
        'p_aft': mk_res_after.p if mk_res_after else None,
        'SenSlope_aft': mk_res_after.slope if mk_res_after else None
    })


results_df = pd.DataFrame(results)
print(results_df)

# results_df.to_excel('macsen.xlsx', index=False)

