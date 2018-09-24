import requests, bs4, io, sys

#the scraper axcepts two command line arguments - maker and model
#TO DO: validate input
maker = sys.argv[1]
model = sys.argv[2]
path = 'https://www.otomoto.pl/osobowe/' + maker + '/' + model 

res = requests.get(path)
res.raise_for_status()

#prepare the file
carFile = io.open('carData.txt', 'w', encoding="utf-8")


#check how many pages are there
carSoup = bs4.BeautifulSoup(res.text, features="lxml")
lastPage = int(carSoup.select('.page')[-1].text)

#iterate through pages
for i in range(1, lastPage):
    res = requests.get(path + '?page=' + str(i))
    res.raise_for_status()
    currentPage = bs4.BeautifulSoup(res.text, features='lxml')
    carList = currentPage.select('article.offer-item')
    print("parsing page " + str(i))
    for car in carList:
        #get the interesting data and write to file
        #TO DO: Create a nicer file, like an MS Excel file
        price = car.find('span',class_='offer-price__number').text.strip().replace(" ", "")
        carFile.write(price + ',' )
        title = car.find('a',class_='offer-title__link').text.strip()
        carFile.write(title + ',' )
        params = car.find_all("li", class_='offer-item__params-item')
        #Iterate through parameters
        #TO DO: account for missing parameters
        for param in params:
            carFile.write(param.text.strip()+ ',')
        carFile.write('\n')
    
carFile.close()

