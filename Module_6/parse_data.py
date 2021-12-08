
import time
from datetime import datetime
import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re



def convert_date(x):
    month_list_ru = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    month_list_ru_cap = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    # month_list_en = ['January','February','March','April','May','June','July',
    #                  'August','September','October','November','December']
    for item in month_list_ru:
        if item in x:
 
            month_num=month_list_ru.index(item)+1
            if month_num<10:
                month_num=str(0)+str(month_num)
#             ind = month_list_ru.index(item)

    nums = [int(x) for x in x.split() if x.isdigit()] 
    if nums[0]<10:
        num_day=str(0)+str(nums[0])
    else:
        num_day=str(nums[0])
    
    tr_to_date=datetime.strptime(num_day+str(".")+str(month_num)+str(".")+str(nums[1]), '%d.%m.%Y')
    return tr_to_date

def get_data(soup):
    all_cars_descriptions = []
    # переходим к парсингу файлов 
    # вытащим ссылку на объявление
    try:
        car_url = soup.find("link", {"rel":"canonical"})['href']
    except:
        car_url = np.NaN

    # получим номер объявления
    try:
        card_id = soup.find('div', class_='CardHead__infoItem CardHead__id').text[2:]
    except:
        card_id = np.NaN   
    
    # получим дату объявления
    try:
        card_data=soup.find('div', class_='CardHead__infoItem CardHead__creationDate').text + " 2021"
        card_data=convert_date(card_data)
    except:
        card_data = np.NaN

    # получим число просмотров объявления
    try:
        views = soup.find('div', class_='CardHead__infoItem CardHead__views').text.replace('\xa0','')
        views = re.findall(r'[0-9]+', str(views))
        card_views_total = views[0]
    except:
        card_views_total = np.NaN
        
    try:
        views = soup.find('div', class_='CardHead__infoItem CardHead__views').text.replace('\xa0','')
        views = re.findall(r'[0-9]+', str(views))
        card_views_today = views[1]
    except:
        card_views_today = np.NaN        
    
    # далее начнем извлекать доступную информацию с страницы  
    # поскольку информации может не быть, то сделаю через проверку выполнения.    
    
    # бренд автомобиля     
    try:    
        brand = soup.find('h1').text.split(' ')[0].upper()
    except:
        brand = np.NaN
  
    # имя модели
    try:
        model_name_full = soup.find('h1').text.split(' ')[1:]
        model_name = model_name_full[0]
    except:
        model_name_full = np.NaN 
        model_name = np.NaN 
    
    # цена автомобиля
    try:
        car_price = soup.find('span', class_='OfferPriceCaption__price').text.replace('\\xa0','').replace('₽','')
    except:
        car_price = np.NaN 
    
    # год выпуска автомобиля
    try:
        production_year = int(soup.find('li', class_='CardInfoRow CardInfoRow_year')\
                              .find_all('span', class_="CardInfoRow__cell")[1].text)
    except:
        production_year = np.NaN
        
    # пробег автомобиля
    try:
        mileage = str(soup.find('li', class_='CardInfoRow CardInfoRow_kmAge')\
                      .find_all('span', class_="CardInfoRow__cell")[1]\
                      .text.replace('\\xa0','')\
                      .replace('км',''))
    except:
        mileage = np.NaN
    
    # тип кузова
    try:
        bodyType = soup.find('li', class_='CardInfoRow CardInfoRow_bodytype')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text
    except:
        bodyType = np.NaN
    
    # цвет автомобиля
    try:
        color = soup.find('li', class_='CardInfoRow CardInfoRow_color')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text
    except:
        color = np.NaN
        
    # двигатель автомобиля
    try:
        eng = soup.find('li', class_='CardInfoRow CardInfoRow_engine')\
                       .find_all('span', class_="CardInfoRow__cell")[1]\
                       .text.replace('\\xa0','').split('/')
        engine_volume = eng[0].strip().replace(' л','')
        engine_power = eng[1].strip().replace('л.с.','')
        engine_type = eng[2].strip().lower()
    except:
        engine_volume = np.NaN
        engine_power = np.NaN
        engine_type = np.NaN
    
    # комплектация автомобиля
    try:
        complectation = soup.find('li', class_='CardInfoRow CardInfoRow_complectationOrEquipmentCount')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.replace('\xa0',' ')
    except:
        complectation = np.NaN
    
    # транспортный налог
    try:
        tax=soup.find('li', class_='CardInfoRow CardInfoRow_transportTax')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.replace('\xa0','') 
        transport_tax =  int(re.findall(r'[0-9]+', str(tax))[0])   
    except:
        transport_tax = np.NaN  
        
    # коробка автомобиля
    try:
        transmission = soup.find('li', class_='CardInfoRow CardInfoRow_transmission')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text
    except:
        transmission = np.NaN
        
    # привод автомобиля
    try:
        drive = soup.find('li', class_='CardInfoRow CardInfoRow_drive')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text
    except:
        drive = np.NaN    
    
     # привод автомобиля
    try:
        wheel = soup.find('li', class_='CardInfoRow CardInfoRow_wheel')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        wheel = np.NaN    
    
     # состояние автомобиля
    try:
        state = soup.find('li', class_='CardInfoRow CardInfoRow_state')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        state = np.NaN     

    # число владельцев автомобиля
    try:
        owners_count = soup.find('li', class_='CardInfoRow CardInfoRow_ownersCount')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        owners_count = np.NaN
        
    # ПТС автомобиля
    try:
        pts = soup.find('li', class_='CardInfoRow CardInfoRow_pts')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        pts = np.NaN
        
    # растаможен автомобиль
    try:
        customs = soup.find('li', class_='CardInfoRow CardInfoRow_customs')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        customs = np.NaN

    # обмен автомобиля
    try:
        exchange = soup.find('li', class_='CardInfoRow CardInfoRow_exchange')\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        exchange = np.NaN
    
    # 
    try:
        card_city = soup.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').text
    except:
        card_city = np.NaN
    
    # выделим время владения автомобилем
    try:
        Владение = soup.find('li', class_="CardInfoRow CardInfoRow_owningTime")\
                        .find_all('span', class_="CardInfoRow__cell")[1].text.lower()
    except:
        Владение = np.NaN
        
    # описание от продавца
    try: 
        description = soup.find('div',class_="CardDescriptionHTML").text
    except:
        description = np.NaN
        
    # ссылка на картинку
    try:
        image = soup.find("link", {"as":"image"})['href']
    except:
        image = np.NaN
    
    # сразу сделаем проверку на призна проданной машины
    try:
        sold_check = soup.find('div', class_ = "CardSold")
        if(sold_check is not None): 
            sold_check = 'Sold'
    except:
        sold_check = np.NaN
   
    
    # покопавшись в ответе на запрос нашел ещё кучку интересного
    # в тэгах script    
    # придется потом много поудалять, тк много дублирующейся информации
    # но это легче чем добавить отсутствующую информацию
    
    scr = soup.find_all("script")
        
    # комплектация
    try:
        complectation_dict = re.search(r'complectation":{"id.*?}',str(scr))[0][15:]
    except:
        complectation_dict = np.NaN
        
    # оборудование
    try:
        equipment_dict = re.search(r'equipment":{.*?}',str(scr))[0][11:]
    except:
        equipment_dict = np.NaN
  
    # пробег
    try:
        mileage_dict = re.search(r'"mileage":\d*',str(scr))[0][10:]
    except:
        try:
            mileage_dict = re.search(r'"mileage":\d*',str(scr))[0][10:]
        except:
            mileage_dict = np.NaN
            

    # информация о модели
    try:
        model_dict = re.search(r'model_info":{.*?}',str(scr))[0][12:]
    except:
        model_dict = np.NaN
            
    try:
        model_name_dict=eval(re.search(r'model_info":{.*?}',str(scr))[0][12:]+str('}'))['code']
#       model_name_dict=re.search(r'model_info":{"code":".*?"',scr)[0][20:].strip('"')
    except:
        model_name_dict = np.NaN            

    # супер-ген
    try:
        super_gen_dict = re.search(r'tech_param":{".*?}',str(scr))[0][12:]
    except:
        super_gen_dict = np.NaN

    # производитель
    try:
        vendor_dict = re.search(r'vendor":".*?"',str(scr))[0][9:].strip('"')
    except:
        vendor_dict = np.NaN

    # каталог параметров
    try:
        catalogParams_dict = re.search(r'catalogParams":{.*?}',str(scr))[0][15:].strip('"')
    except:
        catalogParams_dict = np.NaN

    # информация по машине
    try:
        vehicle_info_dict = re.search(r'configuration":{.*?}',str(scr))[0][15:].strip('"')
    except:
        vehicle_info_dict = np.NaN

    # технические параметры
    try:
        tech_param_dict = re.search(r'tech_param":{"id".*?}',str(scr))[0][12:].strip('"')
    except:
        tech_param_dict = np.NaN           

    # engineDisplacement
    try:
        engineDisplacement = re.search(r'Displacement":".*?"',str(scr))[0][15:].strip('"')
#         engineDisplacement = re.search(r'"displacement":.*?,',str(scr))[0][15:-1]
    except:
        try:
            engineDisplacement = re.search(r'"displacement":.*?,',str(scr))[0][15:-1] 
        except:
            engineDisplacement = np.NaN   
        
    # enginePower
    try:
#         enginePower = re.search(r'power":".*?"',str(scr))[0][14:].strip('"')
        enginePower = re.search(r'Power":".*?"',str(scr))[0][8:].strip('"')
    except:
        try:
            enginePower = re.search(r'power":.*?,',str(scr))[0][7:-1].strip('"')
        except:
            enginePower = np.NaN
        
    # vehicleEngine
    try:
        vehicleEngine = re.search(r'"vehicleEngine":{.*?}',str(scr))[0][16:]
    except:
        vehicleEngine = np.NaN
                
    # fuelType
    try:
#         fuelType = re.search(r'fuelType":".*?"',str(scr))[0][11:].strip('"')
        fuelType = re.search(r'engine_type":".*?"',str(scr))[0][13:].strip('"')
    except:
        fuelType = np.NaN
            
    # lk_summary
    try:
#         lk_summary = re.search(r'lk_summary":".*?"',str(scr))[0][13:].strip(',').replace("\\xa0"," ").partition(',')[0]
        lk_summary = re.search(r'lk_summary":".*?"',str(scr))[0][13:]#.strip(',').replace("\\xa0"," ").partition(',')[0]
    except:
        lk_summary = np.NaN
            
    # doors_count
    try:
        doors_count = re.search(r'doors_count":.*?"',str(scr))[0][13:].strip(',"')
    except:
        doors_count = np.NaN
            
    # offers_dict
    try:
        text=' '.join(re.findall(r'"offers":{([^<>]+)}}', str(scr)))

        offers_dict = {}
        for item in text.split(','):#range(len(text.split(','))):
            key = item.split(':',1)[0]
            value = item.split(':',1)[1]
            offers_dict[key] = value
                
#         scripts_all.append(str(script))
    except:
        offers_dict = np.NaN
            
    # справочник прайса
    try:
        price_info_dict = re.search(r'price_info":{".*?}',str(scr))[0][12:]
    except:
        price_info_dict = np.NaN
        
    # справочник изменения цены предложения
    try:
        price_history_dict = re.search(r'price_history":.*?}',str(scr))[0][16:]
    except:
        price_history_dict = np.NaN
        
    # год производства
    try:
        productionDate = re.search(r'"productionDate":.*?,',str(scr))[0][17:-1]
    except:
        productionDate = np.NaN         
        
    # конфигурация автомобиля
    try:
        vehicleConfiguration = eval(re.search(r'configuration":{.*?}',str(scr))[0][15:].strip('"') + str('}}'))['body_type'] + ' ' + \
                                eval(re.search(r'tech_param":{".*?}',str(scr))[0][12:])['transmission'] + ' ' + \
                                (eval(re.search(r'tech_param":{".*?}',str(scr))[0][12:])['human_name']).split(' ')[0]
#         re.search(r'vehicleConfiguration":.*?,',str(scr))[0][23:-2]
    except:
        vehicleConfiguration = np.NaN        
      
        
    # код валюты объявления
    try:
#         priceCurrency = json.loads(re.search(r'price_info":{".*?}',str(scr))[0][12:])['currency']
        priceCurrency = re.search(r'"priceCurrency":".*?"',str(scr))[0][17:-1]
    except:
#         pass
        priceCurrency = np.NaN
    
    # сохраним всё в словарь
    car_description = {'bodyType' : bodyType,
                       'brand' : brand,
                       'car_url' : car_url,
                       'color' : color,
                       'complectation_dict' : complectation_dict,
                       'description' : description,
                       'engineDisplacement' : engineDisplacement,
                       'enginePower' : enginePower,
                       'equipment_dict' : equipment_dict,
                       'fuelType' : engine_type,
                       'image' : image,    
                       'mileage' : mileage,
                       'modelDate' : production_year,    
                       'model_info' : model_dict,
                       'model_name' : model_name_dict,
                       'name' : lk_summary.split(",")[0],
                       'numberOfDoors' : doors_count,  
                       'parsing_unixtime': time.mktime(datetime.now().timetuple()), # формат unixtime
                       'priceCurrency' : priceCurrency, 
                       'productionDate' : productionDate,
                       'offers_dict' : offers_dict,
                       'sell_id' : card_id, # переименую,чтобы совпадало с тестовой выборкой
                       'super_gen' : super_gen_dict, # переименую,чтобы совпадало с тестовой выборкой
                       'vehicleConfiguration' : vehicleConfiguration,
                       'vehicleTransmission' : transmission,# переименую,чтобы совпадало с тестовой выборкой                       
                       'vendor' : vendor_dict,# переименую,чтобы совпадало с тестовой выборкой
                       'Владельцы' : owners_count,# переименую,чтобы совпадало с тестовой выборкой
                       'Владение' : Владение,
                       'ПТС' : pts,                       
                       'Привод' : drive,
                       'Руль' : wheel,
                       'Состояние' : state,
                       'Таможня' : customs, 
                       # последним будет признак который нам надо спрогнозировать на тестовой выборке
                       'car_price' : car_price, 

                       # дальше идут дополнительные признаки
                       # добавлю в их наименование первую буку "z_" 
                       # чтобы они всегда отображались в конце алфавитных списков
                       'z_card_data' : card_data,
                       'z_card_views_total' : card_views_total,
                       'z_card_views_today' : card_views_today,
                       'z_model_name_full' : model_name_full,
                       'z_model_name_short' : model_name,

                       'z_engine_volume' : engine_volume,
                       'z_engine_power' : engine_power,
                       'z_engine_type' : engine_type,
                       'z_complectation' : complectation,
                       'z_transport_tax' : transport_tax,
                       'z_card_city' : card_city,
                       'z_mileage_dict' : mileage_dict,
                       'z_catalogParams_dict' : catalogParams_dict,
                       'z_vehicle_info_dict' : vehicle_info_dict,
                       'z_tech_param_dict' : tech_param_dict,
                       'z_sold_check' : sold_check,
                       'z_price_info_dict' : price_info_dict,
                       'z_price_history_dict' : price_history_dict,
                       'z_vehicleEngine' : vehicleEngine
                      
                      }
    
#     all_cars_descriptions.append(car_description)
    
    # удалим непечатные пробелы '\xa0'    
#     for key, value in all_cars_descriptions[0].items():
#         all_cars_descriptions[0][key]=str(value).replace('\xa0','')
    
    for key, value in car_description.items():
        if '\xa0' in str(value):
            car_description[key]=str(value).replace('\xa0',' ')
    
    return car_description