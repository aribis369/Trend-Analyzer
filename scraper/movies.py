from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
import pymongo
from selenium import webdriver

# invididual movie finder
def search_moviename():
    user=input("Enter movie name:")

    mov_name=user.lower().replace(" ","+")
    url="http://www.imdb.com/find?ref_=nv_sr_fn&q="+mov_name+"&s=all"
    httpob = urlopen(url)
    decob = httpob.read().decode("utf-8")
    soup=BeautifulSoup(decob)
    td=soup.find_all("td",{"class":"result_text"})
    print(td)
    for q in td:
        movie=q.a.get("href")
        sel=movie.split("/")
        if sel[1]=="title":
            mov_link="http://www.imdb.com"+movie
            httpob_mov = urlopen(mov_link)
            decob_mov = httpob.read().decode("utf-8")
            soup=BeautifulSoup(decob_mov)
            pg=soup.find_all("td",{"class":"result_text"})

# imdb popular movie chart
def popular_chart():
    name=[]
    year=[]
    rating=[]
    url="http://www.imdb.com/chart/moviemeter"
    httpob = urlopen(url)
    decob = httpob.read().decode("utf-8")
    soup=BeautifulSoup(decob)
    col_name=soup.find_all("th")
    tbody=soup.find_all("tbody",{"class":"lister-list"})
    tr=tbody[0].find_all("tr")
    print(len(tr))
    for i in tr:
        name.append(i.find_all("td",{"class":"titleColumn"})[0].a.getText())
        year.append(i.find_all("span",{"class":"secondaryInfo"})[0].getText().replace("(","").replace(")",""))
        try:
            rating.append(i.find_all("td",{"class":"ratingColumn imdbRating"})[0].strong.getText())
        except:
            rating.append("NONE")
    print(name)
    print(year)
    print(rating)

# most anticipated movie(data collection for analysis)
def upcoming_movies():
    name=[]
    position=[]
    share=[]
    driver=webdriver.Firefox(executable_path="/home/arindam/geckodriver")

    url="http://www.imdb.com/india/upcoming?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=2748484262&pf_rd_r=17TM3MW58X4MDGGHCW5N&pf_rd_s=right-15&pf_rd_t=64301&pf_rd_i=upcoming&ref_=in_india_ss_wrap_india_tls_rhs_2"
    driver.get(url)
    decob=driver.page_source

    soup=BeautifulSoup(decob)
    name_span=soup.find_all("span",{"class":"trending-list-rank-item-name"})
    share_span=soup.find_all("span",{"class":"trending-list-rank-item-share"})
    for n in name_span:
        name.append(n.getText())

    for s in share_span:
        share.append(s.getText())
    
    time_span=soup.find("span",{"class":"ranking-last-update-time"})
    time=time_span.getText().replace("(","").replace(")","")


    dic_list={}
    movie_list={}
    '''
    for i in range(0,10):
        dic={}
        dic["movie_name"]=name[i]
        dic["share"]=share[i]
        dic["time"]=time
        print(dic)
        dic_list[str(i+1)]=dic
    '''
    for i in range(0,10):
        dic={}
        dic["rank"]=str(i+1)
        dic["share"]=share[i]
        dic["time"]=time
        movie_list[name[i]]=dic

    # saving in mongodb
    col=pymongo.MongoClient()["movierating"]["movieratings"]
    col.insert_one(movie_list)

    #closing driver
    driver.quit()


upcoming_movies()

