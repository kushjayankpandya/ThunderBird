



'''
import gmplot
import requests
import pandas as pd
from tkinter import *
from tkinter.filedialog import askopenfilename
root = Tk()
import tkinter as Tkin
from tkinter.ttk import *
global w
import os
import datetime
root.title("Heart Beat")
filename=''

apikey='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'    # Use google Cloud API console to generate a javamaps api for your project 
start=0
stop=0
lb=0
sb=0




def markers(df,types,gmap):
	global start
	global stop
	
	for x,y,z,n in zip(df['latitude'],df['longitude'],df[types],df['place']):
		gmap.marker(x,y,color='#3B0B39',title=f'Location = {n} Start day={start}  End day={stop}    {types} = {z}')

def circle(df,color,r,gmap,types):
	
	for x,y,z in zip(df['latitude'],df['longitude'],df[types]):
		gmap.circle(x,y,z*r,color=color,alpha=0.2)


def geocoding(a):
	response = requests.get(f'https://geocoder.api.here.com/6.2/geocode.json?app_id=\{your api key\}&app_code=\{yourapicode\}&searchtext={a}')
	resp_json_payload=response.json()
	print(a,end=' ')
	try:
		lat=resp_json_payload['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Latitude']
		lan=resp_json_payload['Response']['View'][0]['Result'][0]['Location']['NavigationPosition'][0]['Longitude']
		print(f'Latitude:- {lat}  Lomgitude:- {lan}')
		return (lat,lan)
	except:
		print("nothing available")
		return (pd.to_numeric(0.00),pd.to_numeric(0.00))






def excalibur(data,filename,attribute,maxl,minl,types):
	
	
	#getting radius
	
	radius=150000/max(data[f'{types}'])
	#filename='\\'.split(filename)[-1]
	#filtering
	#markers
	#heatmap
	#circle


	#settin the file path and creating the folder
	print(filename)
	filename=filename.split('/')
	print(filename)
	filetemp=filename.pop()
	filepath='/'.join(filename)
	filename=filetemp
	datime=str(datetime.datetime.now())
	datime=datime.replace(':','_')
	filepath=filepath+f'\\ Analysis {filename}'+datime[:20]
	os.makedirs(filepath)




	gmap = gmplot.GoogleMapPlotter(21.170240,72.831062,8)
	gmap.apikey=apikey
	data1=data[data[f'{types}']>maxl]
	print('\n\n   Excellent performing Data\n')
	print(data1)
	markers(data1,types,gmap)
	circle(data1,'green',radius,gmap,types)
	gmap.heatmap(data1['latitude'],data1['longitude'],radius=40)
	gmap.draw(filepath+f'/Excellent_perfor {types} {filename}.html')
	
	gmap = gmplot.GoogleMapPlotter(21.170240,72.831062,8)
	gmap.apikey=apikey
	data2=data[data[f'{types}']<minl]
	print('\n\n    Badly performing data\n')
	print(data2)
	markers(data2,types,gmap)
	gmap.heatmap(data2['latitude'],data2['longitude'],radius=40)
	circle(data2,'red',radius,gmap,types)
	gmap.draw(filepath+f'/Badly_perfor {types} {filename}.html')
	
	gmap = gmplot.GoogleMapPlotter(21.170240,72.831062,8)
	gmap.apikey=apikey
	data3=data[(data[f'{types}']>minl) & (data[f'{types}']<maxl)]
	print('\n\n   Medium performing data\n')
	print(data3)
	markers(data3,types,gmap)
	gmap.heatmap(data3['latitude'],data3['longitude'],radius=40)
	circle(data3,'yellow',radius,gmap,types)
	gmap.draw(filepath+f'/Medium_perfor {types} {filename}.html')
	#saving
	


	return 1

def aorta(filename,attribute,maxl,minl,v1,v2,v3,lb,sb):
	#excalibur(filename,attribute,maxl,minl,'diffdate')




	global start
	global stop
	lb.configure(text='     Reading File     ')
	df=pd.read_csv(filename)
	df=df.drop(0)

	df['Date']=pd.to_datetime(df['Date'])
	df['Date']=df['Date'].dt.date
	lb.configure(text='      Extracting       ')
	df.index=df['Date']
	start=df.index[0]
	stop=df.index[-1]
	data=pd.DataFrame(index=['sum','diffdate','maxmindiff','latitude','longitude'])
	lifetimelikesbycitesdf=[]

	t=attribute
	for x,y in df.iteritems():
	    if t in x:
	        x=x[len(t)+1:]
	        y=pd.to_numeric(y, errors='ignore')
	        data[x]=pd.Series({'sum':sum(y),'maxmindiff':max(y)-min(y),'diffdate':y.iloc[-1]-y.iloc[0],'latitude':None,'longitude':None})



	data=data.transpose()
	print(data)

	data['place']=data.index.copy()
	data.index=list(range(0,len(data)))

	lb.configure(text='Geocoding(aquiring coordinates)')

	print('\n GEOCODING')

	k=list(map(geocoding,data['place']))
	
	k=pd.DataFrame(k)
	data['latitude'],data['longitude']=k[0],k[1]
	data=data[(data['latitude']!=pd.to_numeric(0.00)) & (data['longitude']!=pd.to_numeric(0.00))]
	
	data=data.fillna(0)

	print(data,end='\n\n')
	print('Basic description\n')
	print(data.describe())

	lb.configure(text='Final render and saving')
	if v1==1:
		a=excalibur(data,filename,attribute,maxl,minl,'sum')
		
	if v2==1:
		b=excalibur(data,filename,attribute,maxl,minl,'diffdate')

	if v3==1:
		c=excalibur(data,filename,attribute,maxl,minl,'maxmindiff')
	sb.config(state='normal')	
	lb.configure(text='       DONE!      ')

#######################################################################
#######################################################################

#								GUI 

#########################################################################
########################################################################

print('Staring process. . . . ') 
print('About - Created by Kush Pandya')
print('If found glitch please please report on\n  Email-kpandya7@gmail.com    Contact No-9913515325')
print('GITHUB issue can also be raised on :- https://github.com/kushjayankpandya/ThunderBird/issues')





x=Canvas(root,height=50)


####         functions

def func1(g1,run):
    fn =  askopenfilename(filetypes = (("CSV Files","*.csv"),))
    global filename
    print(fn)
    if fn== '' and filename=='':
        
        root2=Tk()
        Label(root2,text='Please select a file' ).pack(fill=Tkin.X,padx=10,pady=10)
        Button(root2, text='OK!', width=25, command=root2.destroy).pack(fill=Tkin.X,padx=10,pady=10) 
        root2.mainloop()
    
    elif fn!='':
        filename=fn
        run.config(state='normal')
        g1.config(text = f"File selected:-{filename}", )
        
def func2():
    global w
    global filename
    print(filename,g5.get(),int(g8high.get()),int(g10low.get()),var1.get(),var2.get(),var3.get())
    root2=Tk()
    lb=Label(root2,text='Process started' )
    sb=Button(root2, text='OK!', width=25, command=root2.destroy,state=DISABLED)
    print(type(lb),type(sb))
    lb.pack(fill=Tkin.X,padx=10,pady=10)
    aorta(filename,g5.get(),int(g8high.get()),int(g10low.get()),var1.get(),var2.get(),var3.get(),lb,sb)
    sb.pack(fill=Tkin.X,padx=10,pady=10) 
    root2.mainloop()

    

    
    

def callbackfunc(arg):
    global g7
    global g9
    a={"Lifetime Likes by City -":'Likes',"Weekly Reach by City -":'people',"Daily City: People Talking About This -":'daily people talking'}
    print(a[arg.get()])
    g7.configure(text=f'choose the lower limit of {a[arg.get()]} above which performance is good')
    g9.configure(text=f'choose the lower limit of {a[arg.get()]} below which performance is bad')

def printf(a):
    print(a)
    

###   Instance

g1 = Label(root, text='Please choose CSV file for Facebook Insight -',font=("Arial Bold", 12)) 
g2=Button(root, text='Select a file', width=20, command=lambda :func1(g1,run))
g3=x.create_line(0, 18, 200, 18 ) 
g4=Label(root, text='Please choose the attribute on which you want the map',font=("Arial Bold", 12))

g5 = Combobox(root, values=["Lifetime Likes by City -", "Weekly Reach by City -","Daily City: People Talking About This -"])
g5.current(1)
g5.bind("<<ComboboxSelected>>",lambda arg: callbackfunc(g5))
g6=Label(root, text='Choose the limits for different performance',font=("Arial Bold", 12))
g7=Label(root, text='Choose the lower Limit above which performance is Good')
g8high=Spinbox(root, from_ = -10000, to = 100000)
g9=Label(root, text='Choose the Limit below which performance is bad')
g10low=Spinbox(root, from_ = -10000, to = 100000)

var1 = IntVar() 
g11=Checkbutton(root, text='summation', variable=var1,command=printf(var1.get())) 
var2 = IntVar() 
g12=Checkbutton(root, text='Difference of starting and ending Dates', variable=var2,command=printf(var2.get()))
var3 = IntVar() 
g13=Checkbutton(root, text='Difference of Maximum and Minimum Dates', variable=var3,command=printf(var3.get()))


run=Button(root, text='Create graph', width=20, command=func2,state=DISABLED)



### packing


g1.pack(fill=Tkin.X,padx=10,pady=10)
g2.pack(fill=Tkin.X,padx=5,pady=4)        
x.pack(fill=Tkin.X,padx=0,pady=0)   #g3
g4.pack(fill=Tkin.X,padx=10,pady=4)
g5.pack(fill=Tkin.X,padx=10,pady=10)
g6.pack(fill=Tkin.X,padx=10,pady=10)
g7.pack(fill=Tkin.X)
g8high.pack(fill=Tkin.X,padx=10,pady=10)
g9.pack(fill=Tkin.X)
g10low.pack(fill=Tkin.X,padx=10,pady=10)
g11.pack(fill=Tkin.X,padx=4,pady=4)
g12.pack(fill=Tkin.X,padx=4,pady=4)
g13.pack(fill=Tkin.X,padx=4,pady=4)
run.pack(fill=Tkin.X,padx=4,pady=4)


root.mainloop() 
'''
