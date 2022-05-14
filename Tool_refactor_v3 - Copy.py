#----------- OR Script ------------#
#imports
import os
import sys
import xlrd
import operator
from prettytable import PrettyTable

class OR:
    dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"piroty":[]}
    output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"rank":[]}
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
    
    #methods
    def Read_Data_Set(self):
        self.total_crop_count = 0
        dataset_location = os.path.dirname(os.path.abspath(__file__))+'\data_xls.xls'
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
        for cur_row in range(1, row_count): # escape first col [fields names]
            Readed_water.append(sheet.cell(cur_row, 2).value)
            Readed_area.append(sheet.cell(cur_row, 1).value)
            Readed_prod.append(sheet.cell(cur_row, 3).value)
            Readed_city.append(sheet.cell(cur_row, 0).value)
            Readed_name.append(sheet.cell(cur_row, 4).value)
            Readed_visited.append(0)
            Readed_piroty.append(sheet.cell(cur_row, 5).value)
        
        #test sort
        #print(Readed_name)
        crop_count = []
        for i in Readed_name:
            if i not in crop_count:
                crop_count.append(i)
        
        self.total_crop_count = len(crop_count)-1

        p,y,z,h,o,q,x = self.sort_piroty(Readed_water,Readed_area,Readed_prod,Readed_city,Readed_name,Readed_visited,Readed_piroty)

        # assine to dataset
        self.dataset['water'] = x
        self.dataset['area'] = y
        self.dataset['prod'] = z
        self.dataset['city'] = h
        self.dataset['name'] = o
        self.dataset['visited'] = q
        self.dataset['piroty'] = p
        
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
        
        for water in self.output_dataset['water']:
            Total_water_test += water
        for area in self.output_dataset['area']:
            Total_area_test += area
        for prod in self.output_dataset['prod']:
            Total_prod_test += prod
        
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
    
    def preprocessing(self):
        self.output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[],"rank":[]}
        Crop_name = 'X'
        Counter = 0
        table = PrettyTable()
        
        native_water = [];native_area = [];native_prod = [];native_city = [];native_name = []
        for i in self.dataset['name']:
            if i != Crop_name: # new crop
                #print(table)
                #self.sort_table(table)
                #print(i)
                
                Crop_name = i
                table = PrettyTable()
                table.field_names = ["water", "area","prod","city","name","visited"]
                table.add_row([self.dataset['water'][Counter],self.dataset['area'][Counter],self.dataset['prod'][Counter],self.dataset['city'][Counter],Crop_name,self.dataset['visited'][Counter]])
                #solution2
                self.sort_table_solution_2(native_water,native_area,native_prod,native_city,native_name,self.dataset['visited'])
                native_water = [];native_area = [];native_prod = [];native_city = [];native_name = []
                native_water.append(self.dataset['water'][Counter])
                native_area.append(self.dataset['area'][Counter]) 
                native_prod.append(self.dataset['prod'][Counter]) 
                native_city.append(self.dataset['city'][Counter]) 
                native_name.append(self.dataset['name'][Counter])
                         
            else:
                table.add_row([self.dataset['water'][Counter],self.dataset['area'][Counter],self.dataset['prod'][Counter],self.dataset['city'][Counter],Crop_name,self.dataset['visited'][Counter]])
                native_water.append(self.dataset['water'][Counter])
                native_area.append(self.dataset['area'][Counter]) 
                native_prod.append(self.dataset['prod'][Counter]) 
                native_city.append(self.dataset['city'][Counter]) 
                native_name.append(self.dataset['name'][Counter]) 
                 
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

    def sort_piroty(self,x,y,z,h,o,q,p):
        #p,y,z,h,o,q,x = [list(v) for v in zip(*sorted(zip(p,y,z,h,o,q,x)))]
        try:
            p,y,z,h,o,q,x = [list(v) for v in zip(*sorted(zip(p,y,z,h,o,q,x)))]
            return p,y,z,h,o,q,x
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

    def sort_table_solution_2(self,x,y,z,h,j,v):
        try:
            #prepare diviation
            i = 0
            while i < len(x):
                if x[i] != 0 or y[i] != 0:
                    x[i] = x[i]/y[i]
                    pass
                i += 1
            #sort by division
            x,y,z,h,j = [list(v) for v in zip(*sorted(zip(x,y,z,h,j)))]
            # restore real values
            i = 0
            while i < len(x):
                if x[i] != 0 or y[i] != 0:
                    x[i] = x[i] * y[i]
                    pass
                i += 1
            
            #assian sorted to test dataset
            #output_dataset = {"water":[],"area":[],"prod":[],"city":[],"name":[],"visited":[]}
            rank_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
            self.output_dataset['water'] += x
            self.output_dataset['area'] += y
            self.output_dataset['prod'] += z
            self.output_dataset['city'] += h
            self.output_dataset['name'] += j
            self.output_dataset['visited'] += v
            self.output_dataset['rank'] += rank_list
            
            
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
        while counter < len(self.output_dataset['name']):
            if self.output_dataset['name'][counter] == crop_name:
                production += self.output_dataset['prod'][counter]
            counter += 1
        return production

    def search(self,crop_name,city,achived_production,target,prime_city_index):
        
        counter = 0
        target_flag = 0
        

        while counter < len(self.output_dataset['name']):
            # search in area not in same crop
            if self.output_dataset['name'][counter] != crop_name:
                # get the target citys
                if self.output_dataset['city'][counter] == city and self.output_dataset['visited'][counter] == 0 and self.output_dataset['rank'][counter] > self.city_count and self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0:
                    # get target city prop
                    target_city_water = self.output_dataset['water'][counter]
                    target_city_area = self.output_dataset['area'][counter]
                    prime_cost_per_fadan = (self.output_dataset['prod'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    prime_water_per_fadan = (self.output_dataset['water'][prime_city_index]/self.output_dataset['area'][prime_city_index])
                    current_cost_per_fadan = (self.output_dataset['prod'][counter]/self.output_dataset['area'][counter])
                    #calculation
                    achived_production += (target_city_area * prime_cost_per_fadan)
                    if achived_production < target:
                        #update values 
                        self.output_dataset['area'][prime_city_index] += target_city_area
                        self.output_dataset['water'][prime_city_index] += (target_city_area*prime_water_per_fadan)
                        #save for if achived > target 
                        temp_water = self.output_dataset['water'][counter]
                        temp_area = self.output_dataset['area'][counter]
                        temp_prod = self.output_dataset['prod'][counter]
                        #replace target city with zeros
                        self.output_dataset['area'][counter] = 0
                        self.output_dataset['water'][counter] = 0
                        self.output_dataset['visited'][counter] = 1
                        self.output_dataset['visited'][prime_city_index] = 1
                        # edit
                        self.output_dataset['prod'][prime_city_index] += (target_city_area * prime_cost_per_fadan)
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
                            print('diff : ',diff)
                            achived_production -= diff
                            print('new ach prod: ',achived_production)
                            reverse_area = (diff/prime_cost_per_fadan) #prime
                            used_area = temp_area - reverse_area
                            print('R Area : ',reverse_area)
                            print('U Area : ',used_area)
                            #print('Look Here -> ',achived_production)
                            ##print('Reverse area : ',reverse_area)
                            #----- revese----
                            self.output_dataset['area'][prime_city_index] -= target_city_area
                            
                            self.output_dataset['water'][prime_city_index] -= (target_city_area*prime_water_per_fadan)
                            self.output_dataset['area'][prime_city_index] += used_area
                            self.output_dataset['water'][prime_city_index] += (used_area * prime_water_per_fadan)
                            #edit
                            print('current city prod : ',self.output_dataset['prod'][prime_city_index])
                            self.output_dataset['prod'][prime_city_index] -= (target_city_area * prime_cost_per_fadan)
                           
                            print('What will subtract : ', (target_city_area * prime_cost_per_fadan))
                            #edit
                            self.output_dataset['prod'][prime_city_index] += (used_area * prime_cost_per_fadan)
                            print('What will add : ', (used_area * prime_cost_per_fadan))
                            print('final prod : ', self.output_dataset['prod'][prime_city_index])
                            self.output_dataset['area'][counter] = reverse_area
                            self.output_dataset['water'][counter] = temp_water
                            self.output_dataset['visited'][counter] = 0
                            self.output_dataset['prod'][counter] = (reverse_area * current_cost_per_fadan)
                            self.output_dataset['visited'][prime_city_index] = 1
                            #edit
                            
                            ##print('new_achived_target: ',achived_production)
                            
                            
                        return achived_production

            counter += 1
        return achived_production

    def Algo(self,perc,co):
        #begine Algorithm 
        #take target percentage
        
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
                ##print(current_crop_name)
                ##print(current_crop_production)
                ##print(current_crop_target)
                #test
                #self.output_dataset['visited'][counter] = 1
                
                if new_achived_production >= current_crop_production:
                    ##print('normal achived')
                    if normal_flag != 1:
                        self.achivement_normal_count +=1
                        normal_flag = 1

                if self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0 and new_achived_production < current_crop_target :
                    new_achived_production += self.search(current_crop_name,current_city,new_achived_production,current_crop_target,counter)
                    #print(new_achived_production)
                
                if new_achived_production == current_crop_target and target_flag != 1:
                    self.achivement_target_count += 1
                    target_flag = 1
            else:
                current_city = self.output_dataset['city'][counter]
                #self.output_dataset['visited'][counter] = 1
                if new_achived_production >= current_crop_production:
                        ##print('normal achived')
                        if normal_flag != 1:
                            self.achivement_normal_count +=1
                            normal_flag = 1
                if self.output_dataset['water'][counter] != 0 and self.output_dataset['area'][counter] != 0 and new_achived_production < current_crop_target:
                    new_achived_production += self.search(current_crop_name,current_city,new_achived_production,current_crop_target,counter)
                    #print(new_achived_production)
                    
                if new_achived_production == current_crop_target and target_flag != 1:
                    self.achivement_target_count += 1
                    target_flag = 1

            counter += 1

    