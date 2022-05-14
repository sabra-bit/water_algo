
import csv

from matplotlib.pyplot import table
import Tool_refactor_v3
from prettytable import PrettyTable
import random
import pandas as pd
import draw_graph

#dfghjklkjhgfdfghjklkjhgfdfghjkjhgfdfghjkjhgffghj
from matplotlib.pyplot import axes
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
#--- Main ---
def app():
    #---- Settings ----- 
    start = 0
    end = 0
    m = 0
    city_counter = 0
    print('''

    ------ Welcome -------
    -------- v2 ---------

    ''')
    Tool_obj = Tool_refactor_v3.OR()

    def call_algo(x,y,z):
        
        Tool_obj.current_seasson = z
        Tool_obj.Read_Data_Set()
        #Tool_obj.return_dataset()
        #Tool_obj.Total()
        Tool_obj.preprocessing()
        #Tool_obj.return_sorted_dataset()
        #Tool_obj.Total()
        Tool_obj.Algo(x,y)
        #draw_graph.draw_graph(te)
        Tool_obj.Total()

    
    st.header('Compare Solution')
    st.subheader('helpful?')

    instart = st.text_input('Enter Range From :', '0')
    inend = st.text_input('Enter Range End : ', '0')

    inm = st.text_input('Enter Increased Value Range of Production : ', '0')

    incity_counter =st.text_input('Enter city skip from : ', '0')
    incity_counter_to = st.text_input('Enter city skip to : ', '0')

    start = float(instart)
    end = float(inend)
    m = float(inm)
    city_counter = int(incity_counter)
    city_counter_to = int(incity_counter_to)
    #seassons = ['Nile','Permanent','Winter','Summer',]
    if instart != '0' or incity_counter_to !='0':
        seassons = ['Winter','Summer']
    else:
        seassons = []
    start_o = start
    end_o = end
    m_o = m
    city_counter_o = city_counter
    city_counter_to_o = city_counter_o

    global_selected_sol = []



    def draw_final_results():
        table = PrettyTable()
        table.field_names = ['Sol no','Before','After','Diff']
        counter = 0
        seperator_counter = 0
        solution_number = 1
        label = 'water'
        while counter < len(Tool_obj.b_results):
            diff = 0
            if seperator_counter == 0:
                label = 'water: '
            elif seperator_counter == 1:
                label = 'area: '
            elif seperator_counter == 2:
                label = 'production: '

            if seperator_counter == 3:
                table.add_row(['----------','----------','--------------','-------------'])
                solution_number += 1
                seperator_counter = 0
        
            if seperator_counter == 2:
                diff = Tool_obj.f_results[counter] - Tool_obj.b_results[counter]
            else:
                diff = Tool_obj.b_results[counter] - Tool_obj.f_results[counter]

            table.add_row([solution_number,label + str(round(Tool_obj.b_results[counter],2)),label + str(round(Tool_obj.f_results[counter],2)),label + str(round(diff,2))])
            counter += 1
            seperator_counter += 1
        print(table)
        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/all_solutions.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        print('Solution no: ',solution_number)


    def bubbleSort(arr):
        n = len(arr)
    
        # Traverse through all array elements
        for i in range(n-1):
        # range(n) also work but outer loop will repeat one time more than needed.
    
            # Last i elements are already in place
            for j in range(0, n-i-1):
    
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                x = arr[j]
                y = arr[j+1]

                if x[0] < y[0] and x[2] > y[2] :
                    x, y = y, x
        return arr

    def details_solution(sol,sol_index):
        # print sol
        for x in sol_index:
            solution = sol[x]
            print(solution)
            #print sol details
            print('------ solution number : ',x)
            #draw_table_trace(Tool_obj.final_solutions_details[x],x)
        
            file_name = 'output/'+Tool_obj.current_seasson+'/crops_solution_'+str(x)+'.csv'
            df = pd.DataFrame.from_dict(Tool_obj.final_solutions_details[x],orient='index')
            df = df.transpose()
            df.to_csv(file_name, index = False, header=True)

            '''
            csv_columns = ["water", "area","prod","city","rank","visited","name"]
            with open(file_name, 'w') as csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=csv_columns)
                writer.writeheader()
                for data in Tool_obj.final_solutions_details[x]:
                    #print(data)
                    writer.writerows(Tool_obj.final_solutions_details[x][data])

        
            '''
            print('----- Diff from orginal ---')
            draw_table_diff(Tool_obj.final_solutions_details[x])
            print('----- Summary ----')
            draw_summary(Tool_obj.final_solutions_details[x],x)
            
        
    def draw_table(data):
        table = PrettyTable()
        table.field_names = ["water", "area","prod","city","rank","visited","name"]
        i = 0
        while i < len(data['water']):
            table.add_row([data['water'][i],data['area'][i],data['prod'][i],data['city'][i],data['rank'][i],data['visited'][i],data['name'][i]])
            i += 1
        print(table)

    def draw_table_diff(data):
        table = PrettyTable()
        orginal_Dataset = Tool_obj.dataset
        table.field_names = ["water", "area","prod","city","name","visited","rank"]
        print('orginal',len(Tool_obj.dataset['water']))
        print('processed',len(data['water']))
        i = 0
        while i < len(data['water']):
            table.add_row([data['water'][i] - orginal_Dataset['water'][i],data['area'][i]- orginal_Dataset['area'][i],data['prod'][i]- orginal_Dataset['prod'][i],data['city'][i],data['name'][i],data['visited'][i],data['rank'][i]])
            i += 1
        print(table)


    def draw_summary(data,sol_no):
        crop = 'x'
        crop_water = 0
        crop_area = 0
        crop_prod = 0
        before_crop_Water = 0
        before_crop_area = 0
        before_crop_prod = 0
        counter = 0
        summary = []
        while counter < len(data['name']):
            if data['name'][counter] != crop:
                try:
                    # get orginal 
                    counter_orginal = 0
                    old_dataset = Tool_obj.dataset
                    while counter_orginal < len(old_dataset['name']):
                        if old_dataset['name'][counter_orginal] == crop:
                            before_crop_Water += old_dataset['water'][counter_orginal]
                            before_crop_area += old_dataset['area'][counter_orginal]
                            before_crop_prod += old_dataset['prod'][counter_orginal]
                        counter_orginal += 1
                
                    # print summary
                    temp = [crop,before_crop_Water,crop_water,before_crop_area,crop_area,before_crop_prod,crop_prod]
                    #print('Look here -> ', temp)
                    summary.append(temp)

                    # go to other product
                    #edit2
                    crop = data['name'][counter]
                    
                    crop_water = data['water'][counter]
                    crop_area = data['area'][counter]
                    crop_prod = data['prod'][counter]
                    
                    
                    before_crop_Water = 0
                    before_crop_area = 0
                    before_crop_prod = 0
                except:
                    pass
            else:
                #edit2
                if data['visited'][counter] == 1:
                    crop_water += data['water'][counter]
                    crop_area += data['area'][counter]
                    crop_prod += data['prod'][counter]
            
            counter += 1
        
        #pretty table
        table = PrettyTable()
        table.field_names = ["water_before","water_after","Diff_water","area_before","area_after","Diff_area","production_before","production_after","Diff_prod","name"]
        for x in summary:
            x[1] = round(x[1],2)
            x[2] = round(x[2],2)
            x[3] = round(x[3],2)
            x[4] = round(x[4],2)
            x[5] = round(x[5],2)
            x[6] = round(x[6],2)
            
            table.add_row([x[1],x[2],round((x[2]-x[1]),2),x[3],x[4],round((x[4]-x[3]),2),x[5],x[6],round((x[6]-x[5]),2),x[0]])
        print(table)
        
        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/summary_of_sol_no_'+str(sol_no)+'.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

    def process_final_results():
        print('''
            -------- Solution Filter stage ---------
        ''')

        counter = 0
        selected_solution_index = []
        temp_solutions = Tool_obj.f_results_list
        temp_prim = Tool_obj.b_results_list
        temp_achivments = Tool_obj.crop_achivements
        while counter < len(temp_solutions):
            solution = temp_solutions[counter]
            prim = temp_prim[counter]
            if prim[0] - solution[0] > 1 and solution[2] - prim[2] > 1:
                selected_solution_index.append(counter)
            counter += 1
        
        print('''-------- Selected Solution ---------''')

        table = PrettyTable()
        #table.border = False
        table.field_names = ['sol_index','Water','Area','Production','Target Achivement %','Normal Achivement %','solution target Percentage','city skip']
        file_name = 'output/'+Tool_obj.current_seasson+'/summary_of_details_solutions.csv'
        global global_selected_sol
        global_selected_sol = selected_solution_index
        for x in selected_solution_index:
            print('Sol No : ',x)
            sol = temp_solutions[x]
            b_sol = temp_prim[x]
            ach = temp_achivments[x]
            upnormal = Tool_obj.upnormal_crops[x]
            total_normal_production = b_sol[2]
            total_target_production = sol[2]
            total_upnormal = 0
            for key in upnormal.keys():
                total_upnormal += upnormal[key]
            
            upnormal_in_normal = total_upnormal/total_normal_production
            upnormal_in_target = total_upnormal/total_target_production

            percentage = round((((ach[0]*ach[3])+(ach[1]*1)+(ach[2]*0))/(Tool_obj.total_crop_count*ach[3]))*100,2)
            n_percentage = round((((ach[0]*1)+(ach[1]*1)+(ach[2]*0))/(Tool_obj.total_crop_count*1))*100,2)
            #percentage = round((((ach[0]*ach[3])+(ach[1]*1)+(upnormal_in_target))/(Tool_obj.total_crop_count*ach[3]))*100,2)
            #n_percentage = round((((ach[0]*1)+(ach[1]*1)+(upnormal_in_normal))/(Tool_obj.total_crop_count*1))*100,2)
            #----- draw table ------
            table.add_row([str(x),round(sol[0],2),round(sol[1],2),round(sol[2],2),percentage,n_percentage,ach[3],ach[4]])
            print(sol)
            print(ach)
            
            
            
            
            
            

        table.sortby = 'Target Achivement %'
        table.reversesort = True
        print(table)

        # draw_graph

        for x in selected_solution_index:
            #print(Tool_obj.f_all_table_dec_tree[x])
            draw_table_trace(Tool_obj.f_all_table_dec_tree[x],x)

        '''
        for x in selected_solution_index:
            draw_graph.draw_graph_tree(Tool_obj.f_result_graph[x],x,Tool_obj.f_graph_color[x])
            draw_graph.draw_graph_neato(Tool_obj.f_result_graph[x],x,Tool_obj.f_graph_color[x])
            draw_graph.draw_graph_circo(Tool_obj.f_result_graph[x],x,Tool_obj.f_graph_color[x])
            draw_graph.draw_graph_twopi(Tool_obj.f_result_graph[x],x,Tool_obj.f_graph_color[x])
            draw_graph.draw_graph_fdp(Tool_obj.f_result_graph[x],x,Tool_obj.f_graph_color[x])
        '''


        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/summary.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        details_solution(temp_solutions,selected_solution_index)

    def draw_table_trace(sol,sol_no):
        gov = ['Cairo','Alexandria','Portsaid','Suez','Damietta','Dakahlia','Sharkia','Quliubiya','Kafrelsheikh','Gharbia','Monoufia','Behaira','Ismailia','Giza','Benisweif','Fayoum','Minya','Assuit','Sohag','Qena','Aswan','Luxor']
        table = PrettyTable()
        table.title = 'Trace Algorithm'
        header = ['Goverment/Crop']
        for k in sol.keys():
            header.append(k)
        
        table.field_names = header
        for gover in gov:
            row = [gover]
            for k in sol.keys():
                data = sol[k]
                #print(data)
                if gover in data:
                    row.append(data[gover])
                else:
                    row.append('0')
            
            table.add_row(row)
        print(table)
        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/table_T_sol'+str(sol_no)+'.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

    def draw_final_tabel_percentage():
        #before data
        old_data = Tool_obj.b_results
        water_before = old_data[0]
        area_before = old_data[1]
        prod_before = old_data[2]
        old_crops_value = []
        crop = 'x'
        before_crop_Water = 0
        before_crop_area = 0
        before_crop_prod = 0
        counter_orginal = 0
        old_dataset = Tool_obj.dataset
        while counter_orginal < len(old_dataset['name']):
            if old_dataset['name'][counter_orginal] != crop :
            
                temp = []
                temp.append(crop)
                temp.append(before_crop_Water)
                temp.append(before_crop_area)
                temp.append(before_crop_prod)
                old_crops_value.append(temp)
                before_crop_Water = 0
                before_crop_area = 0
                before_crop_prod = 0
                crop = old_dataset['name'][counter_orginal]
            else:
                before_crop_Water += old_dataset['water'][counter_orginal]
                before_crop_area += old_dataset['area'][counter_orginal]
                before_crop_prod += old_dataset['prod'][counter_orginal]
            counter_orginal += 1
        
        del old_crops_value[0]
        del old_crops_value[-1]
        print(old_crops_value)

        table = PrettyTable()
        temp_feild_names = ['sol_index','Labels']
        temp_add_data_row = []
        temp_row_data_water = ['Orginal','water']
        temp_row_data_area = ['Orginal','area']
        temp_row_data_prod = ['Orginal','prod']
        total_prod = 0
        total_water = 0
        total_area = 0
        for x in old_crops_value:
            temp_feild_names.append(x[0])
            water_value = x[1]/water_before
            total_water += water_value
            temp_row_data_water.append(water_value)
            area_value = x[2]/area_before
            total_area += area_value
            temp_row_data_area.append(area_value)
            prod_value = x[3]/prod_before
            total_prod += prod_value
            temp_row_data_prod.append(prod_value)
        
        total_prod = round(total_prod,2)
        total_water = round(total_water,2)
        total_area = round(total_area,2)

        temp_row_data_prod.append(total_prod)
        temp_row_data_water.append(total_water)
        temp_row_data_area.append(total_area)
        temp_feild_names.append('Total')
        table.field_names = temp_feild_names
        table.add_row(temp_row_data_prod)
        table.add_row(temp_row_data_water)
        table.add_row(temp_row_data_area)
        #------- selected_solution -------
        global global_selected_sol
        for x in global_selected_sol:
            final_sol_result = Tool_obj.f_results_list[x]
            sol_total_water = final_sol_result[0]
            sol_total_area = final_sol_result[1]
            sol_total_production = final_sol_result[2]
            sol_dataset = Tool_obj.final_solutions_details[x]
            crop = 'x'
            before_crop_Water = 0
            before_crop_area = 0
            before_crop_prod = 0
            counter_orginal = 0
            all_sol_crops_data = []
            new_sol_data_water = [x,'water']
            new_sol_data_area =  [x,'area']
            new_sol_data_prod =  [x,'prod']
            while counter_orginal < len(sol_dataset['name']):
                if sol_dataset['name'][counter_orginal] != crop :
                    temp = []
                    temp.append(crop)
                    temp.append(before_crop_Water)
                    temp.append(before_crop_area)
                    temp.append(before_crop_prod)
                    all_sol_crops_data.append(temp)
                    before_crop_Water = 0
                    before_crop_area = 0
                    before_crop_prod = 0
                    crop = sol_dataset['name'][counter_orginal]
                else:
                    before_crop_Water += sol_dataset['water'][counter_orginal]
                    before_crop_area += sol_dataset['area'][counter_orginal]
                    before_crop_prod += sol_dataset['prod'][counter_orginal]
                counter_orginal += 1
            
            
            del all_sol_crops_data[0]
            total_prod = 0
            total_water = 0
            total_area = 0
            print(all_sol_crops_data)
            for x in all_sol_crops_data:
                water_value = x[1]/water_before
                total_water += water_value
                new_sol_data_water.append(water_value)
                area_value = x[2]/area_before
                total_area += area_value
                new_sol_data_area.append(area_value)
                prod_value = x[3]/prod_before
                total_prod += prod_value
                new_sol_data_prod.append(prod_value)

            total_prod = round(total_prod,2)
            total_water = round(total_water,2)
            total_area = round(total_area,2)

            new_sol_data_water.append(total_water)
            new_sol_data_area.append(total_area)
            new_sol_data_prod.append(total_prod)

            table.add_row(new_sol_data_prod)
            table.add_row(new_sol_data_water)
            table.add_row(new_sol_data_area)

        print(table)
        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/final_table_percentage.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

    def draw_final_tabel_numeric():
        #before data
        old_data = Tool_obj.b_results
        water_before = old_data[0]
        area_before = old_data[1]
        prod_before = old_data[2]
        old_crops_value = []
        crop = 'x'
        before_crop_Water = 0
        before_crop_area = 0
        before_crop_prod = 0
        counter_orginal = 0
        old_dataset = Tool_obj.dataset
        while counter_orginal < len(old_dataset['name']):
            if old_dataset['name'][counter_orginal] != crop :
            
                temp = []
                temp.append(crop)
                temp.append(before_crop_Water)
                temp.append(before_crop_area)
                temp.append(before_crop_prod)
                old_crops_value.append(temp)
                before_crop_Water = 0
                before_crop_area = 0
                before_crop_prod = 0
                crop = old_dataset['name'][counter_orginal]
            else:
                before_crop_Water += old_dataset['water'][counter_orginal]
                before_crop_area += old_dataset['area'][counter_orginal]
                before_crop_prod += old_dataset['prod'][counter_orginal]
            counter_orginal += 1
        
        del old_crops_value[0]
        del old_crops_value[-1]
        print(old_crops_value)

        table = PrettyTable()
        temp_feild_names = ['sol_index','Labels']
        temp_add_data_row = []
        temp_row_data_water = ['orginal','water']
        temp_row_data_area = ['orginal','area']
        temp_row_data_prod = ['orginal','prod']
        total_prod = 0
        total_water = 0
        total_area = 0
        for x in old_crops_value:
            temp_feild_names.append(x[0])
            water_value = x[1]
            total_water += water_value
            temp_row_data_water.append(water_value)
            area_value = x[2]
            total_area += area_value
            temp_row_data_area.append(area_value)
            prod_value = x[3]
            total_prod += prod_value
            temp_row_data_prod.append(prod_value)
        
        total_prod = round(total_prod,2)
        total_water = round(total_water,2)
        total_area = round(total_area,2)

        temp_row_data_prod.append(total_prod)
        temp_row_data_water.append(total_water)
        temp_row_data_area.append(total_area)
        temp_feild_names.append('Total')
        table.field_names = temp_feild_names
        table.add_row(temp_row_data_prod)
        table.add_row(temp_row_data_water)
        table.add_row(temp_row_data_area)
        #------- selected_solution -------
        global global_selected_sol
        for x in global_selected_sol:
            final_sol_result = Tool_obj.f_results_list[x]
            sol_total_water = final_sol_result[0]
            sol_total_area = final_sol_result[1]
            sol_total_production = final_sol_result[2]
            sol_dataset = Tool_obj.final_solutions_details[x]
            crop = 'x'
            before_crop_Water = 0
            before_crop_area = 0
            before_crop_prod = 0
            counter_orginal = 0
            all_sol_crops_data = []
            new_sol_data_water = [x,'water']
            new_sol_data_area =  [x,'area']
            new_sol_data_prod =  [x,'prod']
            while counter_orginal < len(sol_dataset['name']):
                if sol_dataset['name'][counter_orginal] != crop :
                    temp = []
                    temp.append(crop)
                    temp.append(before_crop_Water)
                    temp.append(before_crop_area)
                    temp.append(before_crop_prod)
                    all_sol_crops_data.append(temp)
                    before_crop_Water = 0
                    before_crop_area = 0
                    before_crop_prod = 0
                    crop = sol_dataset['name'][counter_orginal]
                else:
                    before_crop_Water += sol_dataset['water'][counter_orginal]
                    before_crop_area += sol_dataset['area'][counter_orginal]
                    before_crop_prod += sol_dataset['prod'][counter_orginal]
                counter_orginal += 1
            
            
            del all_sol_crops_data[0]
            total_prod = 0
            total_water = 0
            total_area = 0
            print(all_sol_crops_data)
            for x in all_sol_crops_data:
                water_value = x[1]
                total_water += water_value
                new_sol_data_water.append(water_value)
                area_value = x[2]
                total_area += area_value
                new_sol_data_area.append(area_value)
                prod_value = x[3]
                total_prod += prod_value
                new_sol_data_prod.append(prod_value)

            total_prod = round(total_prod,2)
            total_water = round(total_water,2)
            total_area = round(total_area,2)

            new_sol_data_water.append(total_water)
            new_sol_data_area.append(total_area)
            new_sol_data_prod.append(total_prod)

            table.add_row(new_sol_data_prod)
            table.add_row(new_sol_data_water)
            table.add_row(new_sol_data_area)

        print(table)
        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/final_table_numeric.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        

    def draw_final_table_details_percentage():
        old_data = Tool_obj.b_results
        old_crops_value = []
        gov = ['Cairo','Alexandria','Port said','Suez','Damietta','Dakahlia','Sharkia','Quliubiya','Kafr el sheikh','Gharbia','Monoufia','Behaira','Ismailia','Giza','Beni sweif','Fayoum','Minya','Assuit','Sohag','Qena','Aswan','Luxor']

        crop = 'x'
        old_dataset = Tool_obj.dataset
        counter_orginal = 0
        temp_save_Data = []
        old_water_before = old_data[0]
        old_area_before = old_data[1]
        old_prod_before = old_data[2]
        while counter_orginal < len(old_dataset['name']):
            if old_dataset['name'][counter_orginal] != crop :
            
                temp = [crop]
                temp += temp_save_Data
                old_crops_value.append(temp)
                temp_save_Data = []
                crop = old_dataset['name'][counter_orginal]
            else:
                temp_save_Data.append(old_dataset['city'][counter_orginal])
                temp_save_Data.append(old_dataset['water'][counter_orginal])
                temp_save_Data.append(old_dataset['area'][counter_orginal])
                temp_save_Data.append(old_dataset['prod'][counter_orginal])
                
            counter_orginal += 1
        del old_crops_value[0]
        del old_crops_value[-1]

        table = PrettyTable()
        temp_feild_names = ['sol_index','City','Labels']
        rows = []
        for x in old_crops_value:
            temp_feild_names.append(x[0])
        
        
        label_index = 0
        
        for city in gov:
            
            
            counter_of_city_prop = 0
            while counter_of_city_prop < 3:
                label = ''
                if label_index == 0:
                    label = 'Water'
                    label_index += 1
                elif label_index == 1:
                    label = "Area"
                    label_index += 1
                elif label_index == 2:
                    label = 'Production'
                    label_index = 0
                
                d = ['Orginal',city,label]
                flag = 0

                for x in old_crops_value:
                    length = len(x)
                    counter = 0
                    
                    while counter < length:
                        
                        #city = city.replace(' ','')
                        #city = city.replace(' ','')
                        tar = str(x[counter])
                        #tar = tar.replace(' ','')
                        #tar = tar.replace(' ','')
                        
                        if tar == city: #found city
                            flag+=1
                            #flag += 1
                            index = 0
                            if label == 'Water':
                                index = counter + 1
                                d.append(x[index]/old_water_before)
                            elif label == 'Area':
                                index = counter + 2
                                d.append(x[index]/old_area_before)
                            elif label == 'Production':
                                index = counter + 3
                                d.append(x[index]/old_prod_before)
                            
                            
                        counter += 1
                    
                    
                print('No of x = ',flag)
                flag = 0
                counter_of_city_prop += 1
                rows.append(d)
                #break
        print(temp_feild_names)
        all_table_length = len(temp_feild_names)
        table.field_names = temp_feild_names
        for x in rows:
            if len(x) < all_table_length:
                sub = all_table_length - len(x)
                for g in range(0,sub):
                    x.append(0)
                    
            try:
                table.add_row(x)
            except:
                print('Error in add')

        # solutions 
        rows_2 = []
        global global_selected_sol
        for sol_index in global_selected_sol:
            final_sol_result = Tool_obj.f_results_list[sol_index]
            sol_total_water = final_sol_result[0]
            sol_total_area = final_sol_result[1]
            sol_total_production = final_sol_result[2]
            old_crops_value = []
            gov = ['Cairo','Alexandria','Port said','Suez','Damietta','Dakahlia','Sharkia','Quliubiya','Kafr el sheikh','Gharbia','Monoufia','Behaira','Ismailia','Giza','Beni sweif','Fayoum','Minya','Assuit','Sohag','Qena','Aswan','Luxor']
            crop = 'x'
            final_sol_result_dataset = Tool_obj.final_solutions_details[sol_index]
            counter_orginal = 0
            temp_save_Data = []
            while counter_orginal < len(final_sol_result_dataset['name']):
                if final_sol_result_dataset['name'][counter_orginal] != crop :
                    temp = [crop]
                    temp += temp_save_Data
                    old_crops_value.append(temp)
                    temp_save_Data = []
                    crop = final_sol_result_dataset['name'][counter_orginal]
                else:
                    temp_save_Data.append(final_sol_result_dataset['city'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['water'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['area'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['prod'][counter_orginal])

                counter_orginal += 1
            del old_crops_value[0]
            del old_crops_value[-1]
            label_index = 0
            for city in gov:
                
                counter_of_city_prop = 0
                while counter_of_city_prop < 3:
                    label = ''
                    if label_index == 0:
                        label = 'Water'
                        label_index += 1
                    elif label_index == 1:
                        label = "Area"
                        label_index += 1
                    elif label_index == 2:
                        label = 'Production'
                        label_index = 0
                    
                    sol = 'Solution '+ str(sol_index)
                    d = [sol,city,label]
                    for x in old_crops_value:
                        length = len(x)
                        counter = 0
                        while counter < length:
                            tar = str(x[counter])
                            if tar == city: #found city
                                index = 0
                                if label == 'Water':
                                    index = counter + 1
                                    d.append(x[index]/sol_total_water)
                                elif label == 'Area':
                                    index = counter + 2
                                    d.append(x[index]/sol_total_area)
                                elif label == 'Production':
                                    index = counter + 3
                                    d.append(x[index]/sol_total_production)
                                
                            counter += 1
                    counter_of_city_prop += 1
                    rows_2.append(d)
        
        all_table_length = len(temp_feild_names)
        for x in rows_2:
            if len(x) < all_table_length:
                sub = all_table_length - len(x)
                for g in range(0,sub):
                    x.append(0)
            
            try:
                table.add_row(x)
            except:
                print('Error in add')

        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/final_table_details.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        print(table)

    def draw_final_table_details_numeric():
        old_data = Tool_obj.b_results
        old_crops_value = []
        gov = ['Cairo','Alexandria','Port said','Suez','Damietta','Dakahlia','Sharkia','Quliubiya','Kafr el sheikh','Gharbia','Monoufia','Behaira','Ismailia','Giza','Beni sweif','Fayoum','Minya','Assuit','Sohag','Qena','Aswan','Luxor']

        crop = 'x'
        old_dataset = Tool_obj.dataset
        counter_orginal = 0
        temp_save_Data = []
        old_water_before = old_data[0]
        old_area_before = old_data[1]
        old_prod_before = old_data[2]
        while counter_orginal < len(old_dataset['name']):
            if old_dataset['name'][counter_orginal] != crop :
            
                temp = [crop]
                temp += temp_save_Data
                old_crops_value.append(temp)
                temp_save_Data = []
                crop = old_dataset['name'][counter_orginal]
            else:
                temp_save_Data.append(old_dataset['city'][counter_orginal])
                temp_save_Data.append(old_dataset['water'][counter_orginal])
                temp_save_Data.append(old_dataset['area'][counter_orginal])
                temp_save_Data.append(old_dataset['prod'][counter_orginal])
                
            counter_orginal += 1
        del old_crops_value[0]
        del old_crops_value[-1]

        table = PrettyTable()
        temp_feild_names = ['sol_index','City','Labels']
        rows = []
        for x in old_crops_value:
            temp_feild_names.append(x[0])
        
        
        label_index = 0
        
        for city in gov:
            
            
            counter_of_city_prop = 0
            while counter_of_city_prop < 3:
                label = ''
                if label_index == 0:
                    label = 'Water'
                    label_index += 1
                elif label_index == 1:
                    label = "Area"
                    label_index += 1
                elif label_index == 2:
                    label = 'Production'
                    label_index = 0
                
                d = ['Orginal',city,label]
                flag = 0

                for x in old_crops_value:
                    length = len(x)
                    counter = 0
                    
                    while counter < length:
                        
                        #city = city.replace(' ','')
                        #city = city.replace(' ','')
                        tar = str(x[counter])
                        #tar = tar.replace(' ','')
                        #tar = tar.replace(' ','')
                        
                        if tar == city: #found city
                            flag+=1
                            #flag += 1
                            index = 0
                            if label == 'Water':
                                index = counter + 1
                                d.append(x[index])
                            elif label == 'Area':
                                index = counter + 2
                                d.append(x[index])
                            elif label == 'Production':
                                index = counter + 3
                                d.append(x[index])
                            
                            
                        counter += 1
                    
                    
                print('No of x = ',flag)
                flag = 0
                counter_of_city_prop += 1
                rows.append(d)
                #break
        print(temp_feild_names)
        all_table_length = len(temp_feild_names)
        table.field_names = temp_feild_names
        for x in rows:
            if len(x) < all_table_length:
                sub = all_table_length - len(x)
                for g in range(0,sub):
                    x.append(0)
                    
            try:
                table.add_row(x)
            except:
                print('Error in add')

        # solutions 
        rows_2 = []
        global global_selected_sol
        for sol_index in global_selected_sol:
            final_sol_result = Tool_obj.f_results_list[sol_index]
            sol_total_water = final_sol_result[0]
            sol_total_area = final_sol_result[1]
            sol_total_production = final_sol_result[2]
            old_crops_value = []
            gov = ['Cairo','Alexandria','Port said','Suez','Damietta','Dakahlia','Sharkia','Quliubiya','Kafr el sheikh','Gharbia','Monoufia','Behaira','Ismailia','Giza','Beni sweif','Fayoum','Minya','Assuit','Sohag','Qena','Aswan','Luxor']
            crop = 'x'
            final_sol_result_dataset = Tool_obj.final_solutions_details[sol_index]
            counter_orginal = 0
            temp_save_Data = []
            while counter_orginal < len(final_sol_result_dataset['name']):
                if final_sol_result_dataset['name'][counter_orginal] != crop :
                    temp = [crop]
                    temp += temp_save_Data
                    old_crops_value.append(temp)
                    temp_save_Data = []
                    crop = final_sol_result_dataset['name'][counter_orginal]
                else:
                    temp_save_Data.append(final_sol_result_dataset['city'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['water'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['area'][counter_orginal])
                    temp_save_Data.append(final_sol_result_dataset['prod'][counter_orginal])

                counter_orginal += 1
            del old_crops_value[0]
            del old_crops_value[-1]
            label_index = 0
            for city in gov:
                
                counter_of_city_prop = 0
                while counter_of_city_prop < 3:
                    label = ''
                    if label_index == 0:
                        label = 'Water'
                        label_index += 1
                    elif label_index == 1:
                        label = "Area"
                        label_index += 1
                    elif label_index == 2:
                        label = 'Production'
                        label_index = 0
                    
                    sol = 'Solution '+ str(sol_index)
                    d = [sol,city,label]
                    for x in old_crops_value:
                        length = len(x)
                        counter = 0
                        while counter < length:
                            tar = str(x[counter])
                            if tar == city: #found city
                                index = 0
                                if label == 'Water':
                                    index = counter + 1
                                    d.append(x[index])
                                elif label == 'Area':
                                    index = counter + 2
                                    d.append(x[index])
                                elif label == 'Production':
                                    index = counter + 3
                                    d.append(x[index])
                                
                            counter += 1
                    counter_of_city_prop += 1
                    rows_2.append(d)
        
        all_table_length = len(temp_feild_names)
        for x in rows_2:
            if len(x) < all_table_length:
                sub = all_table_length - len(x)
                for g in range(0,sub):
                    x.append(0)
            
            try:
                table.add_row(x)
            except:
                print('Error in add')

        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/final_table_details_numeric.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        print(table)


    def extract_to_bi():
        
        old_crops_value = []
        crop = 'x'
        old_dataset = Tool_obj.dataset
        counter_orginal = 0
        temp_save_Data = []
        temp_orginal_water = 0
        temp_orginal_area = 0
        temp_orginal_production = 0
        while counter_orginal < len(old_dataset['name']):
            if old_dataset['name'][counter_orginal] != crop :
                if crop != 'x':
                    current_data = []
                    current_data.append('Orginal')
                    current_data.append(crop)
                    current_data.append(temp_orginal_water)
                    current_data.append(temp_orginal_area)
                    current_data.append(temp_orginal_production)
                    old_crops_value.append(current_data)

                temp_orginal_water = 0
                temp_orginal_area = 0
                temp_orginal_production = 0
                crop = old_dataset['name'][counter_orginal]
            else:
                temp_orginal_water += old_dataset['water'][counter_orginal]
                temp_orginal_area += old_dataset['area'][counter_orginal]
                temp_orginal_production += old_dataset['prod'][counter_orginal]
                
            counter_orginal += 1
        
        table = PrettyTable()
        temp_feild_names = ['sol_index','Crop_Name','Water','Area','Production']
        table.field_names = temp_feild_names
        for val in old_crops_value:
            table.add_row(val)
        
        global global_selected_sol
        print(global_selected_sol)
        for sol_index in global_selected_sol:
            final_sol_result_dataset = Tool_obj.final_solutions_details[sol_index]
            sol_crops_value = []
            crop = 'x'
            counter_orginal = 0
            sol_crop_water = 0
            sol_crop_area = 0
            sol_crop_production = 0
            while counter_orginal < len(final_sol_result_dataset['name']):
                if final_sol_result_dataset['name'][counter_orginal] != crop :
                    if crop != 'x':
                        current_data = []
                        current_data.append(str(sol_index))
                        current_data.append(crop)
                        current_data.append(sol_crop_water)
                        current_data.append(sol_crop_area)
                        current_data.append(sol_crop_production)
                        sol_crops_value.append(current_data)

                    sol_crop_water = 0
                    sol_crop_area = 0
                    sol_crop_production = 0
                    crop = final_sol_result_dataset['name'][counter_orginal]
                else:
                    sol_crop_water += final_sol_result_dataset['water'][counter_orginal]
                    sol_crop_area += final_sol_result_dataset['area'][counter_orginal]
                    sol_crop_production += final_sol_result_dataset['prod'][counter_orginal]
            
                counter_orginal += 1 

            for val in sol_crops_value:
                table.add_row(val)
            

        data = str(table.get_string())
        result = [tuple(filter(None, map(str.strip, splitline))) for line in data.splitlines() for splitline in [line.split("|")] if len(splitline) > 1]
        file_name = 'output/'+Tool_obj.current_seasson+'/summary_to_power_pi.csv'
        with open(file_name, 'w') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerows(result)

        print(table)

        
        

        


    def clean_data():
    #------ Edit Fuck 3-11-2021
        Tool_obj.achivement_target_count = 0
        Tool_obj.achivement_normal_count = 0
        Tool_obj.achivement_upnormal_count = 0
        Tool_obj.total_crop_count = 0
        Tool_obj.b_results = []
        Tool_obj.f_results = []
        Tool_obj.b_results_list = []
        Tool_obj.f_results_list = []
        Tool_obj.crop_achivements = []
        Tool_obj.final_solutions_details = []
        #graph
        Tool_obj.chid_graph = []
        Tool_obj.roots_graph = []
        Tool_obj.result_graph = []
        #Tool_obj.city_count = 0
            #------- End Edit 
    #

    if incity_counter_to !='0':
        for seasson in seassons:
            print('-------- Seasson: ',seasson ,' --------------')
            start = start_o
            end = end_o
            m = m_o
            city_counter = city_counter_o
            city_counter_to = city_counter_to_o
            while start <= end:
                for c in range(city_counter,22):
                    call_algo(round(start,2),c,seasson)
                    print('Start value -> ',c)
                start += m
                
            draw_final_results()
            process_final_results()
            print('Total Crop Count : ',Tool_obj.total_crop_count)
            draw_final_tabel_numeric()
            draw_final_tabel_percentage()
            draw_final_table_details_numeric()
            draw_final_table_details_percentage()
            extract_to_bi()
            clean_data()
                
                    
                
            print('-------- END Seasson: ',seasson ,' --------------')


    '''

    '''
