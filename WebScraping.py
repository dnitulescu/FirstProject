import requests
import pandas
from bs4 import BeautifulSoup


r = requests.get("http://www.emag.ro/telefoane-mobile/")
c=r.content
soup = BeautifulSoup(c,"html.parser")

pagelist = soup.find("div",{"id":"emg-pagination-numbers"}).find_all("a",{"class":"emg-pagination-no"})
for page in pagelist:
    lastpage = page.text.replace("\n","").replace(" ","")


list=[]
for page in range(0,int(lastpage)+1,1):
    r = requests.get("http://www.emag.ro/telefoane-mobile/"+"p"+str(page)+"/c")
    #print("http://www.emag.ro/telefoane-mobile/"+"p"+str(page)+"/c")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div",{"class":"product-holder-grid"})
    #print(len(all))

    for product in all:
        d={}
        price =product.find("span",{"class":"money-int"}).text.replace("\n","").replace(" ","")
        name = product.find("div",{"class":"middle-container"}).find("h2").text.replace("\n","").replace(" ","")
        d["price"]=price
        d["name"]=name
        list.append(d)

dataframe=pandas.DataFrame(list)
dataframe.to_csv("telefoane_emag.csv")