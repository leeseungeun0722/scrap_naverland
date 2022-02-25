import scrapy
import requests
from naver_land.items import NaverLandItem
from ast import literal_eval
from datetime import datetime

headers = {
                'input headers'
        }

MAIN_URL = 'https://new.land.naver.com/api/' #반복되는 MAIN URL

URL = MAIN_URL + 'regions/{}?cortarNo={}' #동들의 아파트

APART = MAIN_URL + 'complexes/overview/{}?complexNo={}'

DETAIL = MAIN_URL + 'complexes/{}/prices/real?complexNo={}&tradeType={}&year=5&priceChartChange=true&areaNo={}&type=table'

TYPE = ['A1','B1','B2']

REGION_FIRST_KEY = '1100000000' #서울시

REGION_SECOND_KEY = '1168000000' #강남구

REGION_FIRST_LIST = literal_eval(requests.get(URL.format('list',REGION_FIRST_KEY),headers=headers).text)

class SpiderSpider(scrapy.Spider):
    
    name = 'spider'
    
    def start_requests(self):
            
        for i in REGION_FIRST_LIST['regionList']:  
                
            if i['cortarNo'] == REGION_SECOND_KEY : 
                    
                cortarNo = i['cortarNo']
                REGION_SCOND_URL = URL.format('list',cortarNo) #읍 면 동이 나올 url (개포동,청담동) #https://new.land.naver.com/api/regions/list?cortarNo=1168011400
                    
                yield scrapy.Request(REGION_SCOND_URL, self.parse, dont_filter=True)

    def parse(self,response):
        items = []
        DONG_NAME = []

        REGION_SECOND_URL = literal_eval(response.text)

        for i in REGION_SECOND_URL['regionList']:
        
            ALL_DONG_NAME = i['cortarName']
            DONG_NAME.append(ALL_DONG_NAME)
           #if i['cortarNo'] == '1168011400':
            dong_Num = i['cortarNo']
            dong_Name = i['cortarName']

            dong_List = literal_eval(requests.get(URL.format('complexes',dong_Num),headers=headers).text)
                   
            for i in dong_List['complexList']: #https://new.land.naver.com/api/complexes/overview/119219?complexNo=119219

                if i['realEstateTypeName'] == '아파트': #유형 형태에서 아파트만 추출

                    apartment_Num = i['complexNo'] #아파트 번호
                    apartment_Name = i['complexName'] #아파트 명
                    apartment_List = literal_eval(requests.get(APART.format(apartment_Num,apartment_Num),headers=headers).text)
                                
                    for i in apartment_List['pyeongs']:

                        pyeongNo = i['pyeongNo'] #타입번호
                        pyeongName = i['pyeongName'] #면적

                        for type in TYPE:                                           
                            detail_List = literal_eval(requests.get(DETAIL.format(apartment_Num,apartment_Num,type,pyeongNo),headers=headers).text)

                            for i in detail_List['realPriceOnMonthList']:
                                detail_type = i['realPriceList']

                                for i in detail_type:

                                    item = NaverLandItem()
                                    current_time = datetime.now()
                                    year = i['tradeYear']
                                    month = i['tradeMonth']
                                    date = i['tradeDate']
                                    floor = i['floor']

                                    item['DONG_NAME'] = DONG_NAME
                                    item['dong_Name'] = dong_Name
                                    item['apartment_Name'] = apartment_Name      
                                    item['year'] = year
                                    item['month'] = month
                                    item['date'] = date
                                    item['floor'] = floor
                                    item['UPDATETIME'] = current_time
                                    
                                    
                                    items.append(item)

                                    if i['tradeType'] == 'A1': #매매

                                        price = i['dealPrice']
                                        item['pyeongName'] = pyeongName
                                        item['type_List'] = '매매'
                                        item['price'] = price
                                        item['monthly'] = '-'

                                        items.append(item)
                                        print(dong_Name,apartment_Num,apartment_Name,'매매 = ','타입 : ',detail_List['areaNo'],' 면적 : ',pyeongName, date,' 층수 : ',floor,' 가격 : ',price,current_time)
                                    
                                    elif i['tradeType'] == 'B1': #전세

                                        price = i['leasePrice']
                                        #print(dong_Name,apartment_Num,apartment_Name,'전세 = ','타입 : ',detail_List['areaNo'],' 면적 : ',pyeongName, date,' 층수 : ',floor,' 가격 : ',price)
                                        item['pyeongName'] = pyeongName
                                        item['type_List'] = '전세'
                                        item['price'] = price
                                        item['monthly'] = '-'
                                                
                                        items.append(item)

                                    else : #

                                        deposit = i['leasePrice']
                                        monthly = i['rentPrice']
                                        #print(dong_Name,apartment_Num,apartment_Name,'월세 = ','타입 : ',detail_List['areaNo'],' 면적 : ',pyeongName, date,' 층수 : ',floor,price)                  
                                        item['pyeongName'] = pyeongName
                                        item['type_List'] = '월세'
                                        item['price'] = deposit
                                        item['monthly'] = monthly

                                        items.append(item)
                                        
        
        return items
                                 
                    
            




      
                            
                            