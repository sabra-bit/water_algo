#----------- OR Script ------------#
#imports
import os
import sys
from typing import Counter
from networkx.classes import graph
import xlrd
import operator
from prettytable import PrettyTable
import pandas as pd
from collections import defaultdict

class OR:
    dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"piroty":[],"season":[],"region_name":[]}
    output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"rank":[],"season":[],"region_name":[]}
    f_table_dec_tree = defaultdict(dict)
    f_all_table_dec_tree = []
    achivement_target_count = 0
    achivement_normal_count = 0
    achivement_upnormal_count = 0
    total_crop_count = 0
    b_results = []
    f_results = []
    b_results_list = []
    f_results_list = []
    crop_achivements = []
    final_solutions_details = []
    city_count = 0
    current_algo_target_percentage = 0
    current_seasson = ''
    #graph
    roots_graph = []
    chid_graph = []
    result_graph = []
    graph_color = {}
    f_graph_color = []
    f_result_graph = []
    upnormal_crops = []
    
    #methods
    def Read_Data_Set(self):
        self.total_crop_count = 0
        dataset_location = os.path.dirname(os.path.abspath(__file__))+'\data_final.xls'
        work_book = xlrd.open_workbook(dataset_location)
        sheet = work_book.sheet_by_index(0)
        row_count = sheet.nrows
        col_count = sheet.ncols
        Readed_water = []
        Readed_area = []
        Readed_prod = []
        Readed_city = []
        Readed_name = []
        Readed_visited = []
        Readed_piroty = []
        readed_seasoon = []
        readed_region = []
        for cur_row in range(1, row_count): # escape first col [fields names]
            
            if sheet.cell(cur_row, 6).value == self.current_seasson:
                Readed_water.append(sheet.cell(cur_row, 2).value)
                Readed_area.append(sheet.cell(cur_row, 1).value)
                Readed_prod.append(sheet.cell(cur_row, 3).value)
                Readed_city.append(sheet.cell(cur_row, 0).value)
                Readed_name.append(sheet.cell(cur_row, 4).value)
                Readed_visited.append(0)
                Readed_piroty.append(sheet.cell(cur_row, 5).value)
                readed_seasoon.append(sheet.cell(cur_row, 6).value)
                readed_region.append(sheet.cell(cur_row, 7).value)
                
        #test sort
        #print(Readed_name)
        crop_count = []
        for i in Readed_name:
            if i not in crop_count:
                crop_count.append(i)
        
        self.total_crop_count = len(crop_count)-1

        p,y,z,h,o,q,x,l,m = self.sort_piroty(Readed_water,Readed_area,Readed_prod,Readed_city,Readed_name,Readed_visited,Readed_piroty,readed_seasoon,readed_region)

        # assine to dataset
        self.dataset['water'] = x
        self.dataset['area'] = y
        self.dataset['prod'] = z
        self.dataset['city'] = h
        self.dataset['name'] = o
        self.dataset['visited'] = q
        self.dataset['piroty'] = p
        self.dataset['season'] = l
        self.dataset['region_name'] = m
        
    def return_dataset(self):
        table = PrettyTable()
        table.field_names = ["water", "area","prod","city","name","visited","piroty"]
        i = 0
        while i < len(self.dataset['water']):
            table.add_row([self.dataset['water'][i],self.dataset['area'][i],self.dataset['prod'][i],self.dataset['city'][i],self.dataset['name'][i],self.dataset['visited'][i],self.dataset['piroty'][i]])
            i += 1
        print(table)

    def Total(self):
        Total_water = 0; Total_area = 0; Total_prod = 0
        Total_water_test = 0; Total_area_test = 0; Total_prod_test = 0

        for water in self.dataset['water']:
            Total_water += water
        for area in self.dataset['area']:
            Total_area += area
        for prod in self.dataset['prod']:
            Total_prod += prod
        
        counter = 0
        while counter < len(self.output_dataset['name']):
            Total_water_test += self.output_dataset['water'][counter]
            Total_prod_test += self.output_dataset['prod'][counter]
            if self.output_dataset['visited'][counter] == 1 and self.output_dataset['water'][counter] != 0:
                Total_area_test += self.output_dataset['area'][counter]
            
            #if self.output_dataset['visited'][counter] == 0 and self.output_dataset['area'][counter] != 0 and self.output_dataset['water'][counter] != 0:
                #print('----------- Fuck Here ----------')
                #print(self.output_dataset['city'][counter])
                #print('----------- Fuck Here ----------')
            #else:
            #    print('City: ',self.output_dataset['city'][counter],' Area: ',self.output_dataset['area'][counter])
            counter += 1
        
        ##print('Total_Water: ',Total_water)
        ##print('Total_area: ',Total_area)
        ##print('Total_prod: ',Total_prod)
        ##print('----- After Sort -----')
        ##print('Total_Water_Test_data_set: ',Total_water_test)
        ##print('Total_area_Test_data_set: ',Total_area_test)
        ##print('Total_prod_Test_data_set: ',Total_prod_test)

        # add to final results
        before_results = [Total_water,Total_area,Total_prod]
        after_results = [Total_water_test,Total_area_test,Total_prod_test]
        for x in before_results:
            self.b_results.append(x)
        
        for x in after_results:
            self.f_results.append(x)
        
        self.b_results_list.append(before_results)
        self.f_results_list.append(after_results)
        # add to final solution 
        self.final_solutions_details.append(self.output_dataset)
        
        # add count of achivments
        calc_normal_achive = abs(self.achivement_target_count-self.achivement_normal_count)
        calc_upnormal = abs(self.total_crop_count-(self.achivement_target_count + calc_normal_achive))
        temp_achivments = [self.achivement_target_count,calc_normal_achive,calc_upnormal,self.current_algo_target_percentage,self.city_count]
        self.crop_achivements.append(temp_achivments)
        self.achivement_target_count = 0
        self.achivement_normal_count = 0
        # graph
        
        f_g = self.roots_graph + self.chid_graph
        self.f_result_graph.append(f_g)
        self.roots_graph = []
        self.chid_graph = []
        self.result_graph = []
        #print(self.f_table_dec_tree)
        self.f_all_table_dec_tree.append(self.f_table_dec_tree)
        self.f_table_dec_tree = defaultdict(dict)
        self.f_graph_color.append(self.graph_color)
        self.graph_color = {}
        
        
        
        '''
        # add count of achivments
        calc_upnormal = abs(self.total_crop_count-(self.achivement_target_count + self.achivement_normal_count))
        temp_achivments = [self.achivement_target_count,self.achivement_normal_count,calc_upnormal,self.current_algo_target_percentage,self.city_count]
        self.crop_achivements.append(temp_achivments)
        self.achivement_target_count = 0
        self.achivement_normal_count = 0

        '''


    def preprocessing(self):
        self.output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"rank":[],"season":[],"region_name":[]}
        Crop_name = 'X'
        Counter = 0
        table = PrettyTable()
        
        native_water = [];native_area = [];native_prod = [];native_city = [];native_name = [];native_region = []
        for i in self.dataset['name']:
            if i != Crop_name: # new crop
                #print(table)
                #self.sort_table(table)
                #print(i)
                
                Crop_name = i
                table = PrettyTable()
                table.field_names = ["water", "area","prod","city","name","visited","region_name"]
                table.add_row([self.dataset['water'][Counter],self.dataset['area'][Counter],self.dataset['prod'][Counter],self.dataset['city'][Counter],Crop_name,self.dataset['visited'][Counter],self.dataset['region_name'][Counter]])
                #solution2
                self.sort_table_solution_2(native_water,native_area,native_prod,native_city,native_name,self.dataset['visited'],native_region)
                native_water = [];native_area = [];native_prod = [];native_city = [];native_name = []
                native_water.append(self.dataset['water'][Counter])
                native_area.append(self.dataset['area'][Counter]) 
                native_prod.append(self.dataset['prod'][Counter]) 
                native_city.append(self.dataset['city'][Counter]) 
                native_name.append(self.dataset['name'][Counter])
                native_region.append(self.dataset['region_name'][Counter])
                        
            else:
                table.add_row([self.dataset['water'][Counter],self.dataset['area'][Counter],self.dataset['prod'][Counter],self.dataset['city'][Counter],Crop_name,self.dataset['visited'][Counter],self.dataset['region_name'][Counter]])
                native_water.append(self.dataset['water'][Counter])
                native_area.append(self.dataset['area'][Counter]) 
                native_prod.append(self.dataset['prod'][Counter]) 
                native_city.append(self.dataset['city'][Counter]) 
                native_name.append(self.dataset['name'][Counter]) 
                native_region.append(self.dataset['region_name'][Counter])
                 
            Counter += 1    

        #self.output_dataset = self.dataset
        #a,b,c,d = [list(v) for v in zip(*sorted(zip(dataset['water'],dataset['area'],dataset['prod'],dataset['city'])))]

    def sort_table(self,table):
        #table = table.get_string(sortby = 'water')
        #self.update_temp_dataset(table)
        try:
            pass
            #another way to sort
            #sorted_water,sorted_aread,sorted_prod,sorted_city = [list(v) for v in zip(*sorted(zip(self.dataset['water'],self.dataset['area'],self.dataset['prod'],self.dataset['city'])))]
            #sort multiple fields 
            #print table.get_string(sort_key=operator.itemgetter(1, 0), sortby="Grade")
            #table = table(sortby = 'water')
            #table.sortby = 'water'
            #self.update_temp_dataset(table)
        except Exception as e:
            #e = sys.exc_info()[0]
            print(str(e))

    def sort_piroty(self,x,y,z,h,o,q,p,l,m):
        #p,y,z,h,o,q,x = [list(v) for v in zip(*sorted(zip(p,y,z,h,o,q,x)))]
        try:
            p,y,z,h,o,q,x,l,m = [list(v) for v in zip(*sorted(zip(p,y,z,h,o,q,x,l,m)))]
            return p,y,z,h,o,q,x,l,m
        except:
            pass

    def update_temp_dataset(self,table):
        #prepare table to extract values
        print(table)
        table.border = False
        table.hedaer = False
        
        for row in table:
            table.sortby = 'water'
            x =  row.get_string()
            print(x)
        #for x in table :
        #   print(x[0]['water'])

    def sort_table_solution_2(self,x,y,z,h,j,v,l):
        try:
            #prepare diviation
            i = 0
            while i < len(x):
                if x[i] != 0 or y[i] != 0:
                    x[i] = x[i]/y[i]
                else:
                    x[i] = 9999999
                    y[i] = 9999999
                
                i += 1
            #sort by division
            x,y,z,h,j,l = [list(v) for v in zip(*sorted(zip(x,y,z,h,j,l)))]
            # restore real values
            i = 0
            while i < len(x):
                if x[i] == 9999999:
                    x[i] = 0
                    y[i] = 0

                if x[i] != 0 or y[i] != 0:
                    x[i] = x[i] * y[i]
                
                i += 1
            
            #assian sorted to test dataset
            #output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[]}
            rank_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
            seasson_list = [self.current_seasson]*22
            self.output_dataset['water'] += x
            self.output_dataset['area'] += y
            self.output_dataset['prod'] += z
            self.output_dataset['city'] += h
            self.output_dataset['name'] += j
            self.output_dataset['visited'] += v
            self.output_dataset['rank'] += rank_list
            self.output_dataset['seasson'] += seasson_list
            self.output_dataset['region_name'] += l
            
            
            #print(table)
        except:
            pass
    
    def return_sorted_dataset(self):
        table = PrettyTable()
        table.field_names = ["water", "area","prod","city","name","visited","Rank"]
        i = 0
        while i < len(self.output_dataset['water']):
            table.add_row([self.output_dataset['water'][i],self.output_dataset['area'][i],self.output_dataset['prod'][i],self.output_dataset['city'][i],self.output_dataset['name'][i],self.output_dataset['visited'][i],self.output_dataset['rank'][i]])
            i += 1
        print(table)
    
    def get_crop_old_production(self,crop_name):
        production = 0
        counter = 0
        while counter < len(self.dataset['name']):
            if self.dataset['name'][counter] == crop_name:
                production += self.dataset['prod'][counter]
            counter += 1
        return production
    
    def get_crop_new_prod(self,crop_name):
        production = 0
        counter = 0
        while counter < len(self.output_dataset['name']):
            if self.output_dataset['name'][counter] == crop_name:
                production += self.output_dataset['prod'][counter]
            counter += 1
        return production

    def search(self,crop_name,city,achived_production,target,prime_city_index,prime_cost_per_fadan,prime_water_per_fadan):
        
        counter = 0
        target_flag = 0
        

        while counter < len(self.output_dataset['name']):
            # search in area not in same crop
            if self.output_dataset['name'][counter] != crop_name:
            # get the target citys
                if self.output_dataset['city'][counter] == city and self.output_dataset['visited'][counter] == 0 and self.output_dataset['rank'][counter] > self.city_count  and self.output_dataset['area'][counter] != 0:
                    # get target city prop
                    #print('Cost per fadan: ',prime_cost_per_fadan ,' target area: ',self.output_dataset['area'][counter] , 'City: ',city)
                    target_city_water = self.output_dataset['water'][counter]
                    target_city_area = self.output_dataset['area'][counter]
                    #prime_cost_per_fadan = (self.output_dataset['prod'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    #prime_water_per_fadan = (self.output_dataset['water'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    current_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                    #calculation
                    achived_production += (target_city_area * prime_cost_per_fadan)
                    #update values 
                    self.output_dataset['area'][prime_city_index] += target_city_area
                    self.output_dataset['water'][prime_city_index] += (target_city_area*prime_water_per_fadan)
                        # edit
                    self.output_dataset['prod'][prime_city_index] += (target_city_area * prime_cost_per_fadan)

                    #save for if achived > target 
                    temp_water = self.output_dataset['water'][counter]
                    temp_area = self.output_dataset['area'][counter]
                    temp_prod = self.output_dataset['prod'][counter]
                    #replace target city with zeros
                    self.output_dataset['area'][counter] = 0
                    self.output_dataset['water'][counter] = 0
                    self.output_dataset['visited'][counter] = 1
                    self.output_dataset['visited'][prime_city_index] = 1
                    
                    g_city = city.replace(' ','')
                    #self.f_table_dec_tree[g_city][crop_name] = 1
                    self.f_table_dec_tree[crop_name][g_city] = 1
                    
                    graph_node = (crop_name,g_city)
                    if graph_node in self.chid_graph:
                        pass
                    else:
                        graph_node = (crop_name,g_city)
                        self.chid_graph.append(graph_node)
                        self.graph_color[g_city] = 0.8
                        #self.graph_color.append('green')
                    ##print('Normal:',achived_production)
                    #edit
                    self.output_dataset['prod'][counter] = 0
                    
                    #check target
                    if achived_production >= target:
                        ##print('achived target')
                        ##print(achived_production)
                        #self.output_dataset['water'][prime_city_index] = achived_production
                        # check_diffrence 
                        if achived_production > target:
                            
                            diff = achived_production - target
                            
                            achived_production -= diff
                            
                            reverse_area = (diff/prime_cost_per_fadan) #prime
                            used_area = temp_area - reverse_area
                            
                            #print('Look Here -> ',achived_production)
                            ##print('Reverse area : ',reverse_area)
                            #----- revese----
                            self.output_dataset['area'][prime_city_index] -= target_city_area
                            
                            self.output_dataset['water'][prime_city_index] -= (target_city_area*prime_water_per_fadan)
                            self.output_dataset['area'][prime_city_index] += used_area
                            self.output_dataset['water'][prime_city_index] += (used_area * prime_water_per_fadan)
                            #edit
                            
                            
                            
                            
                            #edit
                            self.output_dataset['prod'][prime_city_index] -= (target_city_area * prime_cost_per_fadan)
                            self.output_dataset['prod'][prime_city_index] += (used_area * prime_cost_per_fadan)
                            
                            self.output_dataset['area'][counter] = reverse_area
                            self.output_dataset['water'][counter] = temp_water
                            #edit 10/11/21
                            self.output_dataset['prod'][counter] = temp_prod
                            self.output_dataset['visited'][counter] = 0
                            self.output_dataset['prod'][counter] = (reverse_area * current_cost_per_fadan)
                            self.output_dataset['visited'][prime_city_index] = 1
                            #edit
                            
                            #print('Crop name: ', crop_name)
                            #print('new_achived_target: ',achived_production)
                            
                            
                        break
                        return achived_production
                else:
                    g_city = city.replace(' ','')
                    try:
                        if self.f_table_dec_tree[crop_name][g_city] != 1:
                            self.f_table_dec_tree[crop_name][g_city] = 0
                    except:
                        self.f_table_dec_tree[crop_name][g_city] = 0
                    
               

            counter += 1
        return achived_production


    def search_lost(self,crop_name,city,achived_production,target,prime_city_index,prime_cost_per_fadan,prime_water_per_fadan):
        
        counter = 0
        target_flag = 0
        

        while counter < len(self.output_dataset['name']):
            # search in area not in same crop
            if self.output_dataset['name'][counter] != crop_name:
            # get the target citys
                if self.output_dataset['city'][counter] == city and self.output_dataset['visited'][counter] == 0   and self.output_dataset['area'][counter] != 0:
                    # get target city prop
                    #print('Cost per fadan: ',prime_cost_per_fadan ,' target area: ',self.output_dataset['area'][counter] , 'City: ',city)
                    target_city_water = self.output_dataset['water'][counter]
                    target_city_area = self.output_dataset['area'][counter]
                    #print('City found for negative crop : ', city , ' area: ',target_city_area , 'Crop: ', crop_name)
                    #prime_cost_per_fadan = (self.output_dataset['prod'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    #prime_water_per_fadan = (self.output_dataset['water'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    current_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                    #calculation
                    achived_production += (target_city_area * prime_cost_per_fadan)
                    #update values 
                    self.output_dataset['area'][prime_city_index] += target_city_area
                    self.output_dataset['water'][prime_city_index] += (target_city_area*prime_water_per_fadan)
                        # edit
                    self.output_dataset['prod'][prime_city_index] += (target_city_area * prime_cost_per_fadan)

                    #save for if achived > target 
                    temp_water = self.output_dataset['water'][counter]
                    temp_area = self.output_dataset['area'][counter]
                    temp_prod = self.output_dataset['prod'][counter]
                    #replace target city with zeros
                    self.output_dataset['area'][counter] = 0
                    self.output_dataset['water'][counter] = 0
                    self.output_dataset['visited'][counter] = 1
                    self.output_dataset['visited'][prime_city_index] = 1
                    
                    ##print('Normal:',achived_production)
                    #edit
                    self.output_dataset['prod'][counter] = 0
                    
                    #check target
                    if achived_production >= target:
                        ##print('achived target')
                        ##print(achived_production)
                        #self.output_dataset['water'][prime_city_index] = achived_production
                        # check_diffrence 
                        if achived_production > target:
                            
                            diff = achived_production - target
                            
                            achived_production -= diff
                            
                            reverse_area = (diff/prime_cost_per_fadan) #prime
                            used_area = temp_area - reverse_area
                            
                            #print('Look Here -> ',achived_production)
                            #print('Reverse area : ',reverse_area)
                            #----- revese----
                            self.output_dataset['area'][prime_city_index] -= target_city_area
                            
                            self.output_dataset['water'][prime_city_index] -= (target_city_area*prime_water_per_fadan)
                            self.output_dataset['area'][prime_city_index] += used_area
                            self.output_dataset['water'][prime_city_index] += (used_area * prime_water_per_fadan)
                            #edit
                            
                            
                            
                            
                            #edit
                            self.output_dataset['prod'][prime_city_index] -= (target_city_area * prime_cost_per_fadan)
                            self.output_dataset['prod'][prime_city_index] += (used_area * prime_cost_per_fadan)
                            
                            self.output_dataset['area'][counter] = reverse_area
                            self.output_dataset['water'][counter] = temp_water
                            #edit 10/11/21
                            self.output_dataset['prod'][counter] = temp_prod
                            self.output_dataset['visited'][counter] = 0
                            self.output_dataset['prod'][counter] = (reverse_area * current_cost_per_fadan)
                            self.output_dataset['visited'][prime_city_index] = 1
                            #edit
                            
                            #print('Crop name: ', crop_name)
                            #print('new_achived_target: ',achived_production)
                            
                            
                        #break
                        return achived_production

            counter += 1
        return achived_production

    def Algo(self,perc,co):
        #begine Algorithm 
        #take target percentage
        
        
        self.graph_color[perc] = 1.0


        percentage = perc
        self.current_algo_target_percentage = perc
        self.city_count = co
        
        counter = 0
        current_crop_name = 'X'
        current_crop_production = 0
        current_crop_target = 0
        new_achived_production = 0
        normal_flag = 0
        target_flag = 0
        #graph edit
        
        while counter < len(self.output_dataset['name']):
            if current_crop_name != self.output_dataset['name'][counter]:
                # Get Current crop prop
                current_crop_name = self.output_dataset['name'][counter]
                current_crop_production = self.get_crop_old_production(current_crop_name)
                current_crop_target = (percentage * current_crop_production)
                current_city = self.output_dataset['city'][counter]
                normal_flag = 0
                target_flag = 0
                new_achived_production = 0 # Editable values
                self.graph_color[current_crop_name] = 0.6
                graph_node = (percentage,current_crop_name)
                #self.graph_color.append('red')
                self.roots_graph.append(graph_node)
                #print(current_crop_name)
                #print(current_crop_production)
                #print(current_crop_target)
                #test
                #self.output_dataset['visited'][counter] = 1
                #edit2
                '''
                try:
                    prime_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                    prime_water_per_fadan = (self.output_dataset['water'][counter]/self.output_dataset['area'][counter])
                except:
                    prime_cost_per_fadan = 0
                    prime_water_per_fadan = 0
                    '''
                # zero city
                
                
                

                if new_achived_production < current_crop_target:
                    new_achived_production += self.output_dataset['prod'][counter]
                    if new_achived_production < current_crop_target:
                        if self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0 and self.output_dataset['visited'][counter] == 0:
                            prime_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                            prime_water_per_fadan = (self.output_dataset['water'][counter]/self.output_dataset['area'][counter])
                            #self.output_dataset['prod'][counter] = 0
                            #self.output_dataset['water'][counter] = 0
                            #self.output_dataset['area'][counter] = 0
                            self.output_dataset['visited'][counter] = 1
                            #edit2
                            new_achived_production = self.search(current_crop_name,current_city,new_achived_production,current_crop_target,counter,prime_cost_per_fadan,prime_water_per_fadan)
                            #print('Fuck 1 -> ' , new_achived_production)
                
                else: #edit2
                    self.output_dataset['prod'][counter] = 0
                    pass

                if new_achived_production >= current_crop_production :
                    ##print('normal achived')
                    if normal_flag != 1:
                        self.achivement_normal_count +=1
                        normal_flag = 1
                
                if new_achived_production == current_crop_target and target_flag != 1:
                    self.achivement_target_count += 1
                    #edit
                    #self.achivement_normal_count -= 1
                    target_flag = 1
                
            else:
                '''
                try:
                    prime_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                    prime_water_per_fadan = (self.output_dataset['water'][counter]/self.output_dataset['area'][counter])
                except:
                    prime_cost_per_fadan = 0
                    prime_water_per_fadan = 0
                '''
                current_city = self.output_dataset['city'][counter]
                #self.output_dataset['visited'][counter] = 1
                
                

                if new_achived_production < current_crop_target:
                    new_achived_production += self.output_dataset['prod'][counter]
                    if new_achived_production < current_crop_target:
                        if self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0 and self.output_dataset['visited'][counter] == 0:
                            prime_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                            prime_water_per_fadan = (self.output_dataset['water'][counter]/self.output_dataset['area'][counter])
                            
                            #self.output_dataset['prod'][counter] = 0
                            #self.output_dataset['water'][counter] = 0
                            #self.output_dataset['area'][counter] = 0
                            self.output_dataset['visited'][counter] = 1
                            #edit2
                            new_achived_production = self.search(current_crop_name,current_city,new_achived_production,current_crop_target,counter,prime_cost_per_fadan,prime_water_per_fadan)
                            #print('Fuck 2 -> ' , new_achived_production)
                else: #edit2
                    self.output_dataset['prod'][counter] = 0
                    pass

                if new_achived_production >= current_crop_production :
                        ##print('normal achived')
                        if normal_flag != 1:
                            self.achivement_normal_count +=1
                            normal_flag = 1

                
                if new_achived_production == current_crop_target and target_flag != 1:
                    self.achivement_target_count += 1
                    #edit
                    #self.achivement_normal_count -= 1
                    target_flag = 1
                
                #print('Fuck 3 final -> ' , new_achived_production)
            counter += 1
        #print('------ First Loss ITeration -------')
        self.check_lost()
        #print('------ END First Loss ITeration -------')
        #print('--------- Second Loss Iteration ---------')
        #self.check_lost()
        #print('------ END Second Loss ITeration -------')

    def Algo_lost(self,perc,neg_crops):
        #begine Algorithm 
        #take target percentage
        
        percentage = perc
        counter = 0
        crop_old_prod = 0
        crop_current_prod = 0
        crop_target_prod = 0
        for crop in neg_crops:
            crop_old_prod = self.get_crop_old_production(crop)
            crop_current_prod = self.get_crop_new_prod(crop)
            crop_target_prod = crop_old_prod * percentage
            while counter < len(self.output_dataset['name']):
                if crop_current_prod < crop_target_prod:
                    
                    if crop == self.output_dataset['name'][counter]:
                        
                        city = self.output_dataset['city'][counter]
                        
                        if self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0 :
                            
                            prime_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                            prime_water_per_fadan = (self.output_dataset['water'][counter]/self.output_dataset['area'][counter])
                            crop_current_prod = self.search_lost(crop,city,crop_current_prod,crop_target_prod,counter,prime_cost_per_fadan,prime_water_per_fadan)
                             
                elif crop_current_prod >= crop_target_prod:
                    #print('negative crop target achived')
                    self.achivement_target_count += 1
                    break
                
                counter += 1
                
        
        


    def check_lost(self):
        current_crop_name = 'X'
        current_crop_production = 0
        neg_prod = []
        counter = 0
        while counter < len(self.output_dataset['name']):
            if current_crop_name != self.output_dataset['name'][counter]:
                current_crop_name = self.output_dataset['name'][counter]
                old_p = self.get_crop_old_production(current_crop_name)
                new_p = self.get_crop_new_prod(current_crop_name)
                diff = new_p - old_p
                if diff < 0 :
                    neg_prod.append(current_crop_name)

            counter += 1
        
        print(neg_prod)
        self.Algo_lost(self.current_algo_target_percentage,neg_prod)
        self.check_lost_upnormal()

    
    def check_lost_upnormal(self):
        current_crop_name = 'X'
        current_crop_production = 0
        neg_prod = {}
        counter = 0
        while counter < len(self.output_dataset['name']):
            if current_crop_name != self.output_dataset['name'][counter]:
                current_crop_name = self.output_dataset['name'][counter]
                old_p = self.get_crop_old_production(current_crop_name)
                new_p = self.get_crop_new_prod(current_crop_name)
                diff = new_p - old_p
                if diff < 0 :
                    #neg_prod.append(current_crop_name)
                    neg_prod[current_crop_name] = new_p

            counter += 1
        
        self.upnormal_crops.append(neg_prod)


                
