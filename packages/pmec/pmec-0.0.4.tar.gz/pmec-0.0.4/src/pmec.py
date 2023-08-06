import bs4
from bs4 import BeautifulSoup 
import requests
def cse():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/computer-science-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('p')
    for news in all_news:
        print(news.text)
def ce():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/civil-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
       print(news.text)

def ae():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/automobile-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
        print(news.text)
               
               
def che():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/chemical-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
              print(news.text)
               
def ee():
     from bs4 import BeautifulSoup
     import requests
     res=requests.get('http://pmec.ac.in/index.php/department/chemical-engineering')
     soup=BeautifulSoup(res.text,'lxml')
     news_box=soup.find('div',{'itemprop':'articleBody'})
     all_news=news_box.find_all('span')
     for news in all_news:
                print(news.text)
               

def etc():
     from bs4 import BeautifulSoup
     import requests
     res=requests.get('http://pmec.ac.in/index.php/department/electronics-telecommunication-engineering')
     soup=BeautifulSoup(res.text,'lxml')
     news_box=soup.find('div',{'itemprop':'articleBody'})
     all_news=news_box.find_all('span')
     for news in all_news:
         print(news.text)
              
def mech():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/mechanical-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
     print(news.text)
               
def mme():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/metallurgy-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
                print(news.text)
               
def pdc():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/production-engineering')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
                print(news.text)
                
def bsh():
    from bs4 import BeautifulSoup
    import requests
    res=requests.get('http://pmec.ac.in/index.php/department/bs-humanities')
    soup=BeautifulSoup(res.text,'lxml')
    news_box=soup.find('div',{'itemprop':'articleBody'})
    all_news=news_box.find_all('span')
    for news in all_news:
        print(news.text)
        
         