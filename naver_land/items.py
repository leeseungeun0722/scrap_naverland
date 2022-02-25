import scrapy 

class NaverLandItem(scrapy.Item):

    type_List = scrapy.Field()
    pyeongName = scrapy.Field()                           
      
    price = scrapy.Field()               
    apartment_Name = scrapy.Field()
    dong_Name = scrapy.Field() 

    year =scrapy.Field()  
    month = scrapy.Field()  
    date = scrapy.Field()  
    floor = scrapy.Field()
        
    dealPrice = scrapy.Field()
    leasePrice = scrapy.Field()
    monthly = scrapy.Field()
    DONG_NAME = scrapy.Field() 
    UPDATETIME = scrapy.Field()
    

    