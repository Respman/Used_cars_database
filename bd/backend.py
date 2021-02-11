#! /usr/bin/env python3

import math
import psycopg2
from psycopg2.extras import DictCursor
from IPython import embed


def inform_about_car(id=0):

    def rec_func(id, table_name):
        cursor.execute(f"select * from {table_name} where id = {id}")
        
        rec = cursor.fetchall()

        if (len(rec)  == 0):
            return []
        
        rec = rec[0]
        
        cursor.execute(f"""select column_name from information_schema.columns
                            where information_schema.columns.table_name='{table_name}'""")

        names = [n[0] for n in cursor.fetchall()]

        res = dict([(names[i], rec[i]) for i in range(1,len(rec))])

        for field in names:
            if (field in ref) and (isinstance(res[field], int)):
                tmp = rec_func(res[field], field)
                key = [k for k in tmp.keys()]
                if  (len(key) == 1):
                    res[field] = tmp[key[0]]
                else:
                    res[field] = tmp

        return res

    conn = psycopg2.connect(dbname='used_cars', user='postgres', 
                            password='1234', host='localhost')
    cursor = conn.cursor(cursor_factory=DictCursor)

    ref = ['driver', 'craigslist_region', 'general_characteristics', 
           'condition', 'title_status', 'paint_color', 'listing_location', 
           'state', 'country', 'manufacturer', 'model', 'type', 'transmission',
           'fuel', 'drive', 'size']

    res = rec_func(id, "used_car")

    cursor.close()
    conn.close()

    return res
    

def most_popular_brand():
    conn = psycopg2.connect(dbname='used_cars', user='postgres', 
                            password='1234', host='localhost')
    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute("""SELECT distinct manufacturer FROM Manufacturer
                      where manufacturer is not null""")
    rec = cursor.fetchall()
    manufacturer_list = [r[0] for r in rec]
    
    amnt = []

    for m in manufacturer_list:
        cursor.execute(f"""SELECT count(*) FROM Used_car where 
                          general_characteristics in 
                          (select id from General_characteristics
                          where manufacturer = (select id from Manufacturer where manufacturer = '{m}'))""")
    
        rec = cursor.fetchall()
        amnt.append(rec[0][0])
    
    res = manufacturer_list[amnt.index(max(amnt))]

    cursor.close()
    conn.close()

    return res


def nearby_me(lat = 0, lon = 0, n=10):

    if (lat > 180) or (lat < -180) or (lon > 180) or (lon < -180):
        return []

    conn = psycopg2.connect(dbname='used_cars', user='postgres', 
                            password='1234', host='localhost')
    cursor = conn.cursor(cursor_factory=DictCursor)

    cursor.execute(f"SELECT id, listing_location FROM Used_car")
    idx = cursor.fetchall()

    if (n > len(idx)) or (n < 0):
        return []

    pos = []

    for i in idx:
        cursor.execute(f"SELECT latitude, longtitude FROM listing_location where id = {i[1]} and (latitude is not null or longtitude is not null)")
        place = cursor.fetchall()
        if (len(place) == 0):
            pos.append([0,0])
        else:
            for j in place:
                pos.append([float(_.replace(',', '.')) for _ in j])
    
    out_mas = []

    for i,p in enumerate(pos):
        dist = math.sqrt((p[0]-lat)**2+(p[1]-lon)**2)
        out_mas.append([dist, idx[i][0]])
    
    out_mas.sort()

    out = [i[1] for i in out_mas]


    cursor.close()
    conn.close()

    return out[:n]
    

def similar_ads(id=0, n=10):

    conn = psycopg2.connect(dbname='used_cars', user='postgres', 
                            password='1234', host='localhost')
    cursor = conn.cursor(cursor_factory=DictCursor)

#------id--check--------------
    cursor.execute(f"select * from used_car where id = {id}")
        
    rec = cursor.fetchall()

    if (len(rec)  == 0):
        return []

    string_par_used_car = ['driver', 'craigslist_region', 'condition', 'title_status',
                    'paint_color']
    string_par_gen_char = ['manufacturer', 'model', 'cylinders', 'types', 'transmission', 
                    'fuel', 'drive', 'sizes']
    string_par_listing_loc = ['state', 'country']
    
    digit_par_used_car = ['price', 'year', 'odometer']
    digit_par_listing_loc = ['longtitude', 'latitude']

#-----weights---for---parametrs--------------------------

    all_string = string_par_used_car+string_par_gen_char+string_par_listing_loc
    all_string_weight = [1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1]

    all_digit = digit_par_used_car+digit_par_listing_loc
    all_digit_weight = [1, 1, 1, 1, 1]
    
    cursor.execute(f"SELECT * FROM Used_car")
    cars = cursor.fetchall()
    
    if (n > len(cars)) or (n < 0):
        return []

    cursor.execute(f"""select column_name from information_schema.columns
                     where information_schema.columns.table_name='used_car'""")
    names_cars = [n[0] for n in cursor.fetchall()]

    cursor.execute(f"""select column_name from information_schema.columns
                     where information_schema.columns.table_name='general_characteristics'""")
    names_char = [n[0] for n in cursor.fetchall()]

    cursor.execute(f"""select column_name from information_schema.columns
                     where information_schema.columns.table_name='listing_location'""")
    names_loc = [n[0] for n in cursor.fetchall()]
    
    tmp_list = []
    for cur_car in cars:
        res_cars = dict([(names_cars[i], cur_car[i]) for i in range(len(cur_car))])
        tmp = {}
        for key in ['id']+string_par_used_car+digit_par_used_car:
            tmp.update({key:res_cars[key]})

        cursor.execute(f"""select * from general_characteristics 
                           where id={res_cars["general_characteristics"]}""")
        char = cursor.fetchall()[0]
        res_char = dict([(names_char[i], char[i]) for i in range(1,len(char))])

        for key in string_par_gen_char:
            tmp.update({key:res_char[key]})

        cursor.execute(f"""select * from listing_location 
                           where id={res_cars["listing_location"]}""")
        loc = cursor.fetchall()[0]
        res_loc = dict([(names_loc[i], loc[i]) for i in range(1,len(loc))])

        for key in string_par_listing_loc+digit_par_listing_loc:
            tmp.update({key:res_loc[key]})

        tmp_list.append(tmp)

#--------------find---max--and--min--val-----------------
    max_val = {}
    min_val = {}

    for key in digit_par_used_car+digit_par_listing_loc:
        if tmp_list[0][key] is None:
            tmp_list[0][key] = 0
        
        if (key in digit_par_listing_loc):
            max_val.update({key:-180})
            min_val.update({key:180})
        else:
            max_val.update({key:tmp_list[0][key]})
            min_val.update({key:tmp_list[0][key]})

    for car in tmp_list:
        #print(car)
        for key in digit_par_used_car+digit_par_listing_loc:
            #print(f"car[key]: {car[key]}")
            if car[key] is None:
                car[key] = 0
            elif (key in digit_par_listing_loc):
                #print(f"key: {key}")
                car[key] = float(car[key].replace(',', '.'))
                if (car[key]>180) or (car[key] < -180):
                    car[key] = car[key]/1000
                    #print(car[key])

            if (car[key] > max_val[key]):
                max_val[key] = car[key]
            if (car[key] < min_val[key]):
                min_val[key] = car[key]
        #print(car)
        if (car['id'] == id):
            my_car = car
               
    tmp_list.remove(my_car)
       
#-------calculating metrics--for--each--listing------------------------

    fin_list = [[] for _ in tmp_list]

    for i,car in enumerate(tmp_list):
        tmp = {}
        for j,key in enumerate(all_string):
            if (car[key] != my_car[key]):
                val = 1
            else:
                val = 0
            val *= all_string_weight[j]
            tmp.update({key:val})
        
        for j,key in enumerate(all_digit):
            val = abs(car[key]-my_car[key])/(abs(max_val[key]-min_val[key]))
            val *= all_digit_weight[j]
            tmp.update({key:val})
        
        val = 0
        for key in tmp.keys():
            val += tmp[key]
        
        fin_list[i].append(val)
        fin_list[i].append(car['id'])
    
    fin_list.sort()
    out = [i[1] for i in fin_list]

    cursor.close()
    conn.close()

    return out[:n]


def print_car(car):
    
    def tmp_func(tab_str, tmp_dict):
        for key in tmp_dict.keys():
            if isinstance(tmp_dict[key], dict):
                print(f"{tab_str}'{key}':")
                tmp_func(tab_str+"    ",tmp_dict[key])
            else:
                print(f"{tab_str}'{key}' -> {tmp_dict[key]}")
    
    if isinstance(car, dict):
        tmp_func("",car)
    
    return


def main():
    print("""
Функции, которые позволяют работать с базой данных:
[1] inform_about_car(int id) - вывод информации о машине по её id в базе
в виде словаря, состоящего из пар "ключ-значение".

[2] print_car(dict car) - красивый вывод на экран информации о выбранной машине,
полученной при помощи функции inform_about_car().
          
[3] most_popular_brand() - вывод самой популярной марки автомобиля.
         
[4] nearby_me(int latitude, int longtitude, int amount) - 
функция, которая позволяет найти n объявлений, расположенных 
максимально близко к указанной точке координат. Выводит список индексов
машин в порядке их близости к указанной точке. 

[5] similar_ads(int id, int amount) - находит n машин, которые максимально 
похожи на машину с выбранным id. Выводит список индексов машин, максимально
похожих на выбранную, в порядке убывания.
""")
 
    embed()


if __name__ == '__main__':
    main()