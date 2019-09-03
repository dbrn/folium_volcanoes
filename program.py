# python 3.5+
import folium
import pandas as pd


def select_color(elevation):
    if elevation < 2000:
        return "green"
    elif 2000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


def main():
    volcanoes_df = pd.read_csv("volcanoes.txt")
    coordinates_list = []
    volcanoes_fg = folium.FeatureGroup("Volcanoes")
    lat_list = list(volcanoes_df["LAT"])
    lon_list = list(volcanoes_df["LON"])
    elev_list = list(volcanoes_df["ELEV"])
    for i in range(len(lat_list)):
        coordinates_list.append((lat_list[i], lon_list[i], elev_list[i]))
    volcanoes_map = folium.Map(location=(coordinates_list[0][0], coordinates_list[0][1]),
                               control_scale=True, tiles="Stamen Terrain", zoom_start=6)
    for coordinates in coordinates_list:
        volcanoes_fg.add_child(folium.CircleMarker(
            location=(coordinates[0], coordinates[1]), popup=f"{int(coordinates[2])} m",
            color="#000000", fill_color=select_color(coordinates[2]), fill_opacity=0.80, fill=True))
    countries_fg = folium.FeatureGroup(name="Countries")
    countries_fg.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                                          style_function=lambda x: {
                                               "fillColor": "green" if x["properties"]["POP2005"] < 25000000
                                               else "orange" if 50000000 > x["properties"]["POP2005"] >= 25000000
                                               else "red"}))
    volcanoes_map.add_child(countries_fg)
    volcanoes_map.add_child(volcanoes_fg)
    volcanoes_map.add_child(folium.LayerControl())
    volcanoes_map.save("volcanoes.html")


if __name__ == "__main__":
    main()
