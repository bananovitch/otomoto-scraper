import requests, bs4, sys, csv, datetime

now = datetime.datetime.now()

#the scraper axcepts two command line arguments - maker and model
#TO DO: validate input, apparently argparse is helpful
maker = sys.argv[1]
model = sys.argv[2]

path = 'https://www.otomoto.pl/osobowe/' + maker + '/' + model 
fileName = maker + '-' + model + '-' + str(now.date()) + '.csv'


#prepare the file
carFile = open(fileName, 'w', newline="")
outputWriter = csv.writer(carFile)

res = requests.get(path)
res.raise_for_status()

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
        currentCarData = []
        price = car.find('span',class_='offer-price__number').text.strip().replace(" ", "")
        currentCarData.append(price)
        title = car.find('a',class_='offer-title__link').text.strip()
        currentCarData.append(title)

        #Iterate through parameters
        paramList = ["year", "mileage", "engine_capacity", "fuel_type"]
        for param in paramList:
            currentParameter = car.find('li', {"data-code": param})
            if (currentParameter):
                currentCarData.append(currentParameter.text.strip())
                print(currentParameter.text.strip())
            else:
                currentCarData.append("")

        outputWriter.writerow(currentCarData)
    
carFile.close()

