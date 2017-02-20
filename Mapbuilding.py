import folium
import pandas

df = pandas.read_csv("Volcanoes-USA.txt")
bmap = folium.Map(location=[df['LAT'].mean(), df['LON'].mean()], zoom_start=6)


def color(elevation):
    minimum = int(min(df['ELEV']))
    step = int((max(df['ELEV'])-min(df['ELEV']))/3)
    if elevation in range(minimum, minimum+step):
        mcolor = 'green'
    elif elevation in range(minimum+step, minimum+step*2):
        mcolor = 'orange'
    else:
        mcolor = 'red'
    return mcolor

for lat,lon,name,elev in zip(df['LAT'], df['LON'], df['NAME'], df['ELEV']):
    bmap.add_child(folium.Marker(location=[lat,lon], popup=name, icon=folium.Icon(color=color(elev))))

bmap.save(outfile='test.html')



