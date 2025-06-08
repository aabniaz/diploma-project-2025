import folium
import webbrowser

stations = {
    "Aral": (46.8012, 61.6751),
    "Zhosaly": (45.48778, 64.07806),
    "Zliha": (45.250, 67.067),
    "Kazaly": (45.7667, 62.1167),
    "Karak": (44.8833, 63.1667),
    "Kulandy": (46.096, 59.517),
    "Kyzylorda": (44.8247, 65.5272),
    "Shiely": (44.1631, 66.7453)
}

m = folium.Map(location=[44.8247, 65.5272], zoom_start=6)

colors = ['red', 'blue', 'green', 'orange', 'purple', 'darkred', 'cadetblue', 'darkblue']

for (name, coords), color in zip(stations.items(), colors):
    folium.CircleMarker(
        location=coords,
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        popup=name
    ).add_to(m)

legend_html = '''
<div style="
position: fixed; 
bottom: 50px; left: 50px; width: 150px; height: 280px; 
background-color: white; border:2px solid grey; z-index:9999; font-size:10px;
padding: 10px;">

<b>Meteostations</b><br><br>
<div style="display: flex; align-items: center;"><div style="background:red; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Aral</div><br>
<div style="display: flex; align-items: center;"><div style="background:blue; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Zhosaly</div><br>
<div style="display: flex; align-items: center;"><div style="background:green; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Zliha</div><br>
<div style="display: flex; align-items: center;"><div style="background:orange; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Kazaly</div><br>
<div style="display: flex; align-items: center;"><div style="background:purple; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Karak</div><br>
<div style="display: flex; align-items: center;"><div style="background:darkred; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Kulandy</div><br>
<div style="display: flex; align-items: center;"><div style="background:cadetblue; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Kyzylorda</div><br>
<div style="display: flex; align-items: center;"><div style="background:darkblue; width:10px; height:10px; border-radius:50%; margin-right:8px;"></div>Shiely</div>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))
m.save("meteostations_map.html")


webbrowser.open("meteostations_map.html")