import task_object
import time_block
import datetime
import shedual_time
import csv
def time_to_index(free_block_list,time):
    time = datetime.datetime.strptime(time,"%H:%M")
    for ft in free_block_list:
        if ft.start_time <= time and ft.end_time > time :
            return ft.index
    return None

def get_user_input(text):
    return input(text)

def get_input_according_to_value(value):
    if value == "1" :
        start_time = get_user_input("Enter start time: ")
        start_time = time_to_index(free_block_list,start_time)
        duration =get_user_input("Enter duration time : ")
        deadline = None
        return start_time,duration,deadline

    elif value == "2" :
        start_time = None
        duration =get_user_input("Enter duration time : ")
        deadline = get_user_input("Enter deadline: ")  
        deadline = time_to_index(free_block_list,deadline)
        return start_time,duration,deadline

    elif value == "3" :
        start_time = None
        duration =get_user_input("Enter duration time (min): ")
        deadline = "30"
        return start_time,duration,deadline

    else:
        print("error in value")
        return None,None,None

def get_time_block_list(day_start,bed_time):
    start = datetime.datetime.strptime(day_start,"%H:%M")
    bed_time = datetime.datetime.strptime(bed_time,"%H:%M") 
    time_block_list = []
    index = 1
    while start < bed_time :
        end = start + datetime.timedelta(minutes=30)
        t_block = time_block.TimeBlock()
        t_block.index = index
        t_block.start_time = start
        t_block.end_time = end
        time_block_list.append(t_block)
        start += datetime.timedelta(minutes=30)
        index += 1
    return time_block_list

def get_filtereded_object_list(task_list) :
    fixed_task_list =[]
    urgent_task_list = []
    non_urgent_task_list =[]

    for t in task_list:
        if t.value == '1':
            fixed_task_list.append(t)
        elif t.value == '2':
            urgent_task_list.append(t)
        elif t.value == '3':
            non_urgent_task_list.append(t)
        else:
            pass

    return fixed_task_list,urgent_task_list,non_urgent_task_list

def read_tasks_from_csv(file_path,free_block_list):
    task_list = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            task = task_object.TaskObject()
            task.task_name = row['Task Name']

            if row['Start Time'] != '':
                task.start_time = time_to_index(free_block_list,row['Start Time'])
            else:  
                task.start_time = time_to_index(free_block_list,"7:00")  

            task.duration =row['Duration']

            if  row['Deadline'] != '':
                task.deadline = time_to_index(free_block_list,row['Deadline'])
            else:
                  task.deadline = time_to_index(free_block_list,"21:59")  


            if  row['Start Time'] !='' and row['Deadline'] == '':
                task.value = "1"
                

            elif  row['Start Time']== '' and  row['Deadline'] !='':
                task.value = "2"
                
            elif   row['Start Time']== '' and  row['Deadline']== '':
                task.value = "3"


            task.update_weight()
            task_list.append(task)
    return task_list
    

if __name__ == "__main__" :
    task_list = []
    shedual_list = []
    day_start = "6:00"
    bed_time = "22:00"
    free_block_list=get_time_block_list(day_start,bed_time)
    # for t in free_block_list:
    #     print(t.index,t.start_time,t.end_time,t.weight)

    task_list = read_tasks_from_csv("task.csv",free_block_list)


    # while True:
    #     task_name = get_user_input("Enter task name or  q to exit: ")
    #     if task_name == "q" :
    #         break
    #     value = get_user_input("Enter value of task(1-fixed,2--urgent,3-not urgent): ")
    #     task = task_object.TaskObject()
    #     task.task_name = task_name
    #     task.value = value
    #     task.start_time,task.duration,task.deadline = get_input_according_to_value(value)
    #     task.update_weight()
    #     task_list.append(task)

    fixed_task_list,urgent_task_list,non_urgent_task_list =get_filtereded_object_list(task_list)
    free_block_list,task_list,shedual_list=shedual_time.shedual_time_block_list(free_block_list,fixed_task_list,shedual_list) 
    free_block_list,task_list,shedual_list=shedual_time.shedual_time_block_list(free_block_list,urgent_task_list,shedual_list)
    for t in urgent_task_list:
        print(t.task_name,t.start_time,t.weight) 
    free_block_list,task_list,shedual_list=shedual_time.shedual_time_block_list(free_block_list,non_urgent_task_list,shedual_list) 
    sorted_shedual_list=sorted(shedual_list, key=lambda x: x.index)
    # print("\n")
    # for t in free_block_list:
    #     print(t.index,t.start_time,t.end_time,t.weight)

    for i in range(len(sorted_shedual_list)):
        if not i:
            print("---------"+"Task_name: " +sorted_shedual_list[i].name+"---------")
            print("Start Time: " + sorted_shedual_list[i].start_time.strftime("%H:%M"))
        elif (((sorted_shedual_list[i].name != sorted_shedual_list[i-1].name) or ((sorted_shedual_list[i].name != sorted_shedual_list[i-1].name) )and (sorted_shedual_list[i].index - sorted_shedual_list[i-1].index) > 1)) and i != (len(sorted_shedual_list)-2) and i :
            print("End Time: " + sorted_shedual_list[i-1].end_time.strftime("%H:%M"))
            print("---------"+"Task_name: " +sorted_shedual_list[i].name+"---------")
            print("Start Time: " + sorted_shedual_list[i].start_time.strftime("%H:%M"))
            if i == (len(sorted_shedual_list)-1):
                print("End Time: " + sorted_shedual_list[i].end_time.strftime("%H:%M"))


  
        # print(sorted_shedual_list[i].name)  
        # print(sorted_shedual_list[i+1].name) 


    for t1 in sorted_shedual_list:
        #print(t1.task_name,t1.value,t1.start_time,t1.duration,t1.deadline) 
        print(t1.name,t1.start_time,t1.end_time)      
        
        
        

