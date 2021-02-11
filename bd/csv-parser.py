#! /usr/bin/env python3.8

import csv
import copy
import os

def main():
    csv_path = "./vehicles.csv"
    tabl = {}
    Key = ['manufacturer', 'model', 'condition', 'fuel', 'title_status', 'transmission', 'drive', 'size', 'type', 'paint_color', 'state', 'region']
    with open(csv_path, "r") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')

#construct unique values for different colums:

        tabl = dict.fromkeys(Key)
        for name in Key:
            tabl[name] = []

        for row in reader:
            for name in Key[:-1]:
                if row[name] not in tabl[name]:
                    tabl[name].append(row[name])
            if [row['region'],row['region_url']] not in tabl['region']:
                tabl['region'].append([row['region'],row['region_url']])

#make csv-tables for this unique val:

        for name in Key[:-1]:
            with open(f"./{name}.csv", "w") as csv_f:
                field = ["Id", name]
                writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field)
                writer.writeheader()
                for i in range(len(tabl[name])):
                    row = {}
                    row.update({"Id": i})
                    row.update({name: tabl[name][i]})
                    writer.writerow(row)
            
        with open(f"./region.csv", "w") as csv_f:
            field = ["Id", "region", "region_url"]
            writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field)
            writer.writeheader()
            for i in range(len(tabl["region"])):
                row = {}
                row.update({"Id": i})
                row.update({"region": tabl["region"][i][0]})
                row.update({"region_url": tabl["region"][i][1]})
                writer.writerow(row)
        


    with open(csv_path, "r") as f_obj:
        reader = csv.DictReader(f_obj, delimiter=',')
        with open(f"./used_car_tmp.csv", "w") as csv_f:
            field = reader.fieldnames
            field.append("DriverId")
            field.append("country")
            writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field)
            writer.writeheader()
            i = 0
            for row in reader:
                row["id"] = i
                i += 1
                row.update({"DriverId":0})
                row.update({"country":0})
                row["region"]= tabl["region"].index([row["region"],row["region_url"]])
                row["description"]=row["description"][:(30,len(row["description"]))[len(row["description"])<=30]]+"..."

                for name in Key[:-1]:
                    row[name] = tabl[name].index(row[name])
                writer.writerow(row)
        
        with open("./used_car_tmp.csv", "r") as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            field = copy.deepcopy(reader.fieldnames)
            field.remove("region_url")
            with open("./used_car.csv", "w") as csv_f:
                writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field)
                writer.writeheader()
                for row in reader:
                    row.pop("region_url")
                    writer.writerow(row)

        os.system("mv ./used_car.csv ./used_car_tmp.csv")

        with open("./used_car_tmp.csv", "r") as f_obj:
            reader = csv.DictReader(f_obj, delimiter=',')
            field_used_car = ['id', 'DriverId', 'url', 'region', 'price', 'year', 'general_characteristics', 
            'condition', 'odometer', 'title_status',
            'vin', 'image_url', 'paint_color',
            'description', 'listing_location']
            field_list_loc = ['id', 'state', 'country', 'long', 'lat']
            field_gen_char = ['id', 'manufacturer', 'model',
            'cylinders', 'type', 'transmission', 'fuel', 'drive', 'size']
            
            tmp_mas = []
            for raw in reader:
                tmp_mas.append(raw)

            loc_dict = []
            char_dict = []

            with open("./general_characteristics.csv", "w") as csv_f:
                writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field_gen_char)
                writer.writeheader()
                j = 0
                for row in tmp_mas:
                    my_row = {}
                    for i in field_gen_char[1:]:
                        my_row.update({i:row[i]})
                    
                    if my_row not in char_dict:
                        char_dict.append(my_row)
                        tmp_row = {"id":str(j)}
                        j += 1
                        for k in my_row.keys():
                            tmp_row.update({k:my_row[k]})
                        writer.writerow(tmp_row)

            with open("./listing_location.csv", "w") as csv_f:
                writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field_list_loc)
                writer.writeheader()
                j = 0
                for row in tmp_mas:
                    my_row = {}
                    for i in field_list_loc[1:]:
                        my_row.update({i:row[i]})
                    if my_row not in loc_dict:
                        loc_dict.append(my_row)
                        tmp_row = {"id":str(j)}
                        j += 1
                        for k in my_row.keys():
                            tmp_row.update({k:my_row[k]})
                        writer.writerow(tmp_row)

            with open("./used_car.csv", "w") as csv_f:
                writer = csv.DictWriter(csv_f, delimiter=',', fieldnames=field_used_car)
                writer.writeheader()
                for row in tmp_mas:
                    my_row = {}
                    for i in field_used_car[:6]:
                        my_row.update({i:row[i]})
                    
                    char_row = {}
                    for i in field_gen_char[1:]:
                        char_row.update({i:row[i]})
                    
                    #print(str(char_dict.index(char_row)))
                    my_row.update({field_used_car[6]: str(char_dict.index(char_row))})
                    
                    for i in field_used_car[7:-1]:
                        my_row.update({i:row[i]})
                    
                    loc_row = {}
                    for i in field_list_loc[1:]:
                        loc_row.update({i:row[i]})
                    
                    my_row.update({field_used_car[-1]: str(loc_dict.index(loc_row))})
                    writer.writerow(my_row)
                    #print(my_row)
                    #inp = input()


        os.system("rm ./used_car_tmp.csv") 



if __name__ == "__main__":
    main()
