def get_sum_of_previous_shedual_task(time_block_index,shedual_list):
    sum = 0
    for st in shedual_list:
        if time_block_index > st.index :
            sum = sum + (1/((st.weight*int(st.value))*10))
    return sum

def get_graph_value(index):
    graph_value= [1,1,25,25,25,25,50,62,75,100,100,100,62,50,25,25,1,1,25,25,50,75,100,100,75,75,62,50,50,50,25,25,1,1]
    return graph_value[int(index)-1]/100

def updat_free_time_block_weight(free_block_list,shedual_list):
    for ft in free_block_list:
        ft.weight = get_graph_value(ft.index)-(get_sum_of_previous_shedual_task(ft.index,shedual_list)/(len(free_block_list)+len(shedual_list)))

    return free_block_list

def select_max_weight_element(task_list,free_block=False,max_task=None):
    max_element = None
    max_weight = -1000000
    for task in task_list:

        if max_weight <= task.weight and free_block :
            if max_task.deadline > task.index:
                max_weight =  task.weight
                max_element = task


        elif max_weight <= task.weight :
            max_weight =  task.weight
            max_element = task

    return max_element

def decrement_duration(task):
    for t in task:
        t.duration = str(int(t.duration)-1)
    return task

def increment_start_time(task):
    for t in task:
        t.start_time = str(int(t.start_time)+1)
    return task


def remove_task_from_task_list(task_list,task):
    for t in task:

        if not int(t.duration):
            task_list.remove(t)
    return task_list


def find_smilar_starting_time_task(task_list,task):
    smilar_start_time_tasks =[]
    for t in task_list:
        if task.start_time == t.start_time:
            smilar_start_time_tasks.append(t)
    return smilar_start_time_tasks


def breck_update(free_block_list,shedual_list):
    for ft in free_block_list:

        if ft.weight < -0.8:
            ft.weight = -1
            ft.name = "sleep"
            ft.value ="-1"
            shedual_list.append(ft)
            free_block_list.remove(ft)


        elif ft.weight >= -0.8 and ft.weight < 0:
            ft.weight = -0.75
            ft.name = "normal break"
            ft.value ="-2"
            shedual_list.append(ft)
            free_block_list.remove(ft)           



    return free_block_list,shedual_list        

def shedual_time_block_list(free_block_list,task_list,shedual_list) :
    while len(task_list) and len(free_block_list) :
        free_block_list = updat_free_time_block_weight(free_block_list,shedual_list)
        #free_block_list,shedual_list = breck_update(free_block_list,shedual_list)
        #free_block_list = updat_free_time_block_weight(free_block_list,shedual_list)
        # if not len(free_block_list):
        #     break
        max_weight_task = select_max_weight_element(task_list,False,None)
        # if max_weight_task is None:
        #     break 
        overlap = True
        if max_weight_task.value == "1":
            for ft in free_block_list:
                if ft.index == int( max_weight_task.start_time):
                    ft.name = max_weight_task.task_name
                    ft.value = max_weight_task.value
                    smilar_start_task = find_smilar_starting_time_task(task_list,max_weight_task)
                    # for s in smilar_start_task:
                    #     print(s.task_name,s.duration)
                    smilar_start_task = decrement_duration(smilar_start_task)
                    smilar_start_task = increment_start_time(smilar_start_task)
                    shedual_list.append(ft)
                    # for s in shedual_list:
                    #     print("$$$",s.name,s.index)
                    free_block_list.remove(ft)
                    task_list = remove_task_from_task_list(task_list,smilar_start_task)
                    overlap = False
            if overlap:
                task_list.remove(max_weight_task)
        else:

            max_weight_free_block = select_max_weight_element(free_block_list,True,max_weight_task)  
            if max_weight_free_block is None and len(task_list) > 1:
                print("blabla")
                print(max_weight_task.task_name)
                task = []
                task.append(max_weight_task)
                task = decrement_duration(task)
                task_list = remove_task_from_task_list(task_list,task)
                continue
        

            max_weight_free_block.name = max_weight_task.task_name
            max_weight_free_block.value = max_weight_task.value
            shedual_list.append(max_weight_free_block)
            free_block_list.remove(max_weight_free_block)
            task = []
            task.append(max_weight_task)

            task = decrement_duration(task)

            task_list = remove_task_from_task_list(task_list,task)
            
            free_block_list = updat_free_time_block_weight(free_block_list,shedual_list)
            free_block_list,shedual_list = breck_update(free_block_list,shedual_list)
            free_block_list = updat_free_time_block_weight(free_block_list,shedual_list)


    return free_block_list,task_list,shedual_list





