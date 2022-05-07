from bs4 import BeautifulSoup
import requests

# สร้าง function สำหรับการทำงานกับข้อมูล
def beautify(url):
    res = requests.get(url)
    res.encoding = "utf-8"
    # สร้าง list สำหรับเก็บข้อมูล
    lstData = []
    lstDate = []
    lstLink = []
    
    if res.status_code == 200:
      # ถ้ามีข้อมูลให้เก็บลง list
        soup = BeautifulSoup(res.text, 'html.parser')
        for link in soup.find_all('span', {"class": "field--type-string"}):
            lstData.append(link.text)
        for link in soup.find_all('a', {"rel": 'bookmark'}):
            lstLink.append("https://www.kmitl.ac.th"+link['href'])
        for link in soup.find_all('em'):
            text = link.text
            lstDate.append(text.strip())

        return zip(lstData, lstDate), lstLink
    else:
      # ถ้า page โหลดไม่ได้ให้ทำการ show error
        print("Error")


def displayInfo(data):
    index = 0

    # วนข้อใน list ที่ได้มาแสดงผล
    for i in data[0]:
        print("\n===========================")
        print("หัวข้อข่าว : %s \nเมื่อวันที่ : %s" % (i[0], i[1]))
        print("คลิกเพื่อดูข่าว => "+data[1][index])
        print("===========================\n")

        index += 1

# สร้าง function readPage และ readByKeyword เพื่อแยกการทำงานเพราะ link ของข่าวไม่เหมือนกัน
def readPage(url):
    isPrint = True
    pageIndex = 0

    while True:
        if isPrint:
            data = beautify(url+"&page="+str(pageIndex))
            displayInfo(data)
        else:
            isPrint = True

        # ถาม users ว่าจะทำการอ่านต่อหรือไม่
        inp = str(input("View next page? (y/n) : "))
        if inp.lower() == 'y':
            pageIndex += 1
        elif inp.lower() == 'n':
            return
        else:
            print("Invalid input")
            isPrint = False

def readByKeyword(url,keyword):
    print(url+str(keyword))
    data = beautify(url+str(keyword))
    displayInfo(data)


url = 'https://www.kmitl.ac.th/content/all?cat=All&keywords='
isExit = False

while not isExit:
    print("1. Read by keyword")
    print("2. Read by page")
    print("3. Exit")
    inp = str(input("Enter choice : "))

    if inp == '1':
        keyword = str(input("Enter keyword : "))
        readByKeyword(url,keyword)
    elif inp == '2':
        readPage(url)
    elif inp == '3':
        isExit = True
    else:
        print("Invalid input")
