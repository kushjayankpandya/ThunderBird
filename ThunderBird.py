import gmplot
import requests
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import datetime

root = tk.Tk()
root.title("Heart Beat")

filename = ''
apikey = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Use Google Cloud API console to generate a Javamaps API for your project
start = 0
stop = 0


def markers(df, types, gmap):
    """
    Add markers to the Google Map.

    Args:
        df (pd.DataFrame): DataFrame containing latitude, longitude, and other information.
        types (str): Type of data.
        gmap (gmplot.GoogleMapPlotter): Google Map object.

    Returns:
        None
    """
    global start
    global stop

    for x, y, z, n in zip(df['latitude'], df['longitude'], df[types], df['place']):
        gmap.marker(x, y, color='#3B0B39', title=f'Location = {n} Start day={start}  End day={stop}    {types} = {z}')


def circle(df, color, r, gmap, types):
    """
    Add circles to the Google Map.

    Args:
        df (pd.DataFrame): DataFrame containing latitude, longitude, and other information.
        color (str): Circle color.
        r (float): Circle radius.
        gmap (gmplot.GoogleMapPlotter): Google Map object.
        types (str): Type of data.

    Returns:
        None
    """
    for x, y, z in zip(df['latitude'], df['longitude'], df[types]):
        gmap.circle(x, y, z * r, color=color, alpha=0.2)


def geocoding(a):
    """
    Perform geocoding for a given address.

    Args:
        a (str): Address to geocode.

    Returns:
        tuple: Latitude and longitude of the address.
    """
    response = requests.get(f'https://geocoder.api.here.com/6.2/geocode.json?app_id=\{your api key\}&app_code=\{yourapicode\}&searchtext={a}')
    resp_json_payload = response.json()
    print(a, end=' ')

    try:
        lat = resp_json_payload['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
        lan = resp_json_payload['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
        print(f'Latitude: {lat}, Longitude: {lan}')
        return lat, lan
    except:
        print("Nothing available")
        return pd.to_numeric(0.00), pd.to_numeric(0.00)


def excalibur(data, filename, attribute, maxl, minl, types):
    """
    Perform data analysis and create Google Maps with markers, circles, and heatmaps.

    Args:
        data (pd.DataFrame): DataFrame containing the data.
        filename (str): Name of the file being analyzed.
        attribute (str): Attribute on which the analysis is performed.
        maxl (int): Upper limit for good performance.
        minl (int): Lower limit for bad performance.
        types (str): Type of data.

    Returns:
        int: Status code (1 for success).
    """
    # Getting radius
    radius = 150000 / max(data[f'{types}'])

    # Setting the file path and creating the folder
    print(filename)
    filename = filename.split('/')
    print(filename)
    filetemp = filename.pop()
    filepath = '/'.join(filename)
    filename = filetemp
    datime = str(datetime.datetime.now())
    datime = datime.replace(':', '_')
    filepath = filepath + f'\\ Analysis {filename}' + datime[:20]
    os.makedirs(filepath)

    gmap = gmplot.GoogleMapPlotter(21.170240, 72.831062, 8)
    gmap.apikey = apikey
    data1 = data[data[f'{types}'] > maxl]
    print('\n\n   Excellent performing Data\n')
    print(data1)
    markers(data1, types, gmap)
    circle(data1, 'green', radius, gmap, types)
    gmap.heatmap(data1['latitude'], data1['longitude'], radius=40)
    gmap.draw(filepath + f'/Excellent_perfor {types} {filename}.html')

    gmap = gmplot.GoogleMapPlotter(21.170240, 72.831062, 8)
    gmap.apikey = apikey
    data2 = data[data[f'{types}'] < minl]
    print('\n\n    Badly performing data\n')
    print(data2)
    markers(data2, types, gmap)
    gmap.heatmap(data2['latitude'], data2['longitude'], radius=40)
    circle(data2, 'red', radius, gmap, types)
    gmap.draw(filepath + f'/Badly_perfor {types} {filename}.html')

    gmap = gmplot.GoogleMapPlotter(21.170240, 72.831062, 8)
    gmap.apikey = apikey
    data3 = data[(data[f'{types}'] > minl) & (data[f'{types}'] < maxl)]
    print('\n\n   Medium performing data\n')
    print(data3)
    markers(data3, types, gmap)
    gmap.heatmap(data3['latitude'], data3['longitude'], radius=40)
    circle(data3, 'yellow', radius, gmap, types)
    gmap.draw(filepath + f'/Medium_perfor {types} {filename}.html')

    return 1


def aorta(filename, attribute, maxl, minl, v1, v2, v3, lb, sb):
    """
    Perform data extraction, geocoding, analysis, and rendering.

    Args:
        filename (str): Name of the file being analyzed.
        attribute (str): Attribute on which the analysis is performed.
        maxl (int): Upper limit for good performance.
        minl (int): Lower limit for bad performance.
        v1 (int): Flag for sum analysis.
        v2 (int): Flag for difference of starting and ending dates analysis.
        v3 (int): Flag for difference of maximum and minimum dates analysis.
        lb (tk.Label): Label to display process status.
        sb (tk.Button): Button to enable after completion.

    Returns:
        None
    """
    global start
    global stop
    lb.configure(text='Reading File')
    df = pd.read_csv(filename)
    df = df.drop(0)

    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.date
    lb.configure(text='Extracting')
    df.index = df['Date']
    start = df.index[0]
    stop = df.index[-1]
    data = pd.DataFrame(index=['sum', 'diffdate', 'maxmindiff', 'latitude', 'longitude'])

    t = attribute
    for x, y in df.iteritems():
        if t in x:
            x = x[len(t) + 1:]
            y = pd.to_numeric(y, errors='ignore')
            data[x] = pd.Series({'sum': sum(y), 'maxmindiff': max(y) - min(y), 'diffdate': y.iloc[-1] - y.iloc[0], 'latitude': None, 'longitude': None})

    data = data.transpose()
    print(data)

    data['place'] = data.index.copy()
    data.index = list(range(0, len(data)))

    lb.configure(text='Geocoding (acquiring coordinates)')

    print('\nGeocoding')

    k = list(map(geocoding, data['place']))

    k = pd.DataFrame(k)
    data['latitude'], data['longitude'] = k[0], k[1]
    data = data[(data['latitude'] != pd.to_numeric(0.00)) & (data['longitude'] != pd.to_numeric(0.00))]

    data = data.fillna(0)

    print(data, end='\n\n')
    print('Basic description\n')
    print(data.describe())

    lb.configure(text='Final render and saving')
    if v1 == 1:
        a = excalibur(data, filename, attribute, maxl, minl, 'sum')

    if v2 == 1:
        b = excalibur(data, filename, attribute, maxl, minl, 'diffdate')

    if v3 == 1:
        c = excalibur(data, filename, attribute, maxl, minl, 'maxmindiff')
    sb.config(state='normal')
    lb.configure(text='DONE!')


# GUI
print('Starting process...')
print('About - Created by Kush Pandya')
print('If found glitch, please report to:\nEmail: kpandya7@gmail.com, Contact No: 9913515325')
print('GitHub issue can also be raised at: https://github.com/kushjayankpandya/ThunderBird/issues')

x = tk.Canvas(root, height=50)


def func1(g1, run):
    fn = askopenfilename(filetypes=(("CSV Files", "*.csv"),))
    global filename
    print(fn)

    if fn == '' and filename == '':
        root2 = tk.Tk()
        Label(root2, text='Please select a file').pack(fill=tk.X, padx=10, pady=10)
        Button(root2, text='OK!', width=25, command=root2.destroy).pack(fill=tk.X, padx=10, pady=10)
        root2.mainloop()

    elif fn != '':
        filename = fn
        run.config(state='normal')
        g1.config(text=f"File selected: {filename}")


def func2():
    global w
    global filename
    print(filename, g5.get(), int(g8high.get()), int(g10low.get()), var1.get(), var2.get(), var3.get())
    root2 = tk.Tk()
    lb = tk.Label(root2, text='Process started')
    sb = tk.Button(root2, text='OK!', width=25, command=root2.destroy, state=tk.DISABLED)
    print(type(lb), type(sb))
    lb.pack(fill=tk.X, padx=10, pady=10)
    aorta(filename, g5.get(), int(g8high.get()), int(g10low.get()), var1.get(), var2.get(), var3.get(), lb, sb)
    sb.pack(fill=tk.X, padx=10, pady=10)
    root2.mainloop()


def callbackfunc(arg):
    global g7
    global g9
    a = {"Lifetime Likes by City -": 'Likes', "Weekly Reach by City -": 'people',
         "Daily City: People Talking About This -": 'daily people talking'}
    print(a[arg.get()])
    g7.configure(text=f'Choose the lower limit of {a[arg.get()]} above which performance is good')
    g9.configure(text=f'Choose the lower limit of {a[arg.get()]} below which performance is bad')


def printf(a):
    print(a)


g1 = tk.Label(root, text='Please choose CSV file for Facebook Insight -', font=("Arial Bold", 12))
g2 = tk.Button(root, text='Select a file', width=20, command=lambda: func1(g1, run))
g3 = x.create_line(0, 18, 200, 18)
g4 = tk.Label(root, text='Please choose the attribute on which you want the map', font=("Arial Bold", 12))

g5 = tk.Combobox(root, values=["Lifetime Likes by City -", "Weekly Reach by City -", "Daily City: People Talking About This -"])
g5.current(1)
g5.bind("<<ComboboxSelected>>", lambda arg: callbackfunc(g5))

g6 = tk.Label(root, text='Choose the limits for different performance', font=("Arial Bold", 12))
g7 = tk.Label(root, text='Choose the lower limit above which performance is Good')
g8high = tk.Spinbox(root, from_=-10000, to=100000)
g9 = tk.Label(root, text='Choose the limit below which performance is bad')
g10low = tk.Spinbox(root, from_=-10000, to=100000)

var1 = tk.IntVar()
g11 = tk.Checkbutton(root, text='Summation', variable=var1, command=printf(var1.get()))

var2 = tk.IntVar()
g12 = tk.Checkbutton(root, text='Difference of starting and ending dates', variable=var2, command=printf(var2.get()))

var3 = tk.IntVar()
g13 = tk.Checkbutton(root, text='Difference of maximum and minimum dates', variable=var3, command=printf(var3.get()))

run = tk.Button(root, text='Create graph', width=20, command=func2, state=tk.DISABLED)


# Packing GUI elements
g1.pack(fill=tk.X, padx=10, pady=10)
g2.pack(fill=tk.X, padx=5, pady=4)
x.pack(fill=tk.X, padx=0, pady=0)
g4.pack(fill=tk.X, padx=10, pady=4)
g5.pack(fill=tk.X, padx=10, pady=10)
g6.pack(fill=tk.X, padx=10, pady=10)
g7.pack(fill=tk.X)
g8high.pack(fill=tk.X, padx=10, pady=10)
g9.pack(fill=tk.X)
g10low.pack(fill=tk.X, padx=10, pady=10)
g11.pack(fill=tk.X, padx=4, pady=4)
g12.pack(fill=tk.X, padx=4, pady=4)
g13.pack(fill=tk.X, padx=4, pady=4)
run.pack(fill=tk.X, padx=4, pady=4)

root.mainloop()
