from datetime import datetime, timedelta

FIX=1
URGENT=2
NONE_URGENT=3



def get_task(tasks,task_type):
    task_list=[]
    for task in tasks:
        if task['weight']== task_type:
            task_list.append(task)
    return task_list   


def get_shedual_fix_tasks(fix_tasks, start_date):
    shu_fix=[]
    for fix_task in fix_tasks:
        end_time=fix_task['start']+timedelta(minutes=fix_task['duration'])               #every fix task end time calculate
        shu_fix.append({'start_time': fix_task['start'].replace(year=start_date.year, month=start_date.month, day=start_date.day),'end': end_time.replace(year=start_date.year, month=start_date.month, day=start_date.day)})
    return shu_fix             #  every fix task list shedual [start_time1:end_time1,start_time2:end_time2]         

def get_full_time_list(tasks):
    full_time_list=[]
    for task in tasks:
        full_time_list.append(task['start_time'])
        full_time_list.append(task['end'])
    return full_time_list


def get_shedual_urgent_tasks(urgent_tasks,full_shedual, start_date):
    full_shedual_line=get_full_time_list(full_shedual)
    full_shedual_line.sort()
    start_time=start_date.replace(hour=7, minute=0)
    end_time=start_date.replace(hour=23, minute=0)
    for task in urgent_tasks:
        full_shedual_line=get_full_time_list(full_shedual)
        full_shedual_line.sort()
        if len(full_shedual_line):
            duration=timedelta(minutes=task['duration'])
            deadline=task['deadline'].replace(year=start_date.year, month=start_date.month, day=start_date.day)
            start_duration = full_shedual_line[0]- start_time
            if deadline > start_time and full_shedual_line[0] > deadline and start_duration >= duration:
                full_shedual.append({'start_time':start_time,'end':start_time+timedelta(minutes=task['duration']),'name':task['name']})

            elif deadline > start_time and full_shedual_line[0] <= deadline and deadline <= end_time:
                if full_shedual_line[0]!= start_time:
                    full_shedual_line.append(start_time)
                if full_shedual_line[len(full_shedual_line)-1]!=end_time:    
                    full_shedual_line.append(end_time)
                full_shedual_line.sort()
                index=0
                free_slots=[]
                for i in range(len(full_shedual_line)-1):
                    if deadline>full_shedual_line[i] and deadline<full_shedual_line[i+1]:
                        index=i
                print(index)        
                time_line_shu=[]
                time_line_shu=get_full_time_list(full_shedual)    
                time_line_shu.sort()    
                if start_time!=time_line_shu[0]:         
                    if index % 2:
                        free_slots=full_shedual_line[0:index]
                    elif (not(index % 2) )  and deadline-full_shedual_line[index] > duration:
                        free_slots=full_shedual_line[0:index]  
                        free_slots.append(deadline)
                    else:
                        free_slots=full_shedual_line[0:index-1]

                    value_list=[] 
                    for k in range(len(free_slots)-1):
                        td=free_slots[k+1]-free_slots[k] 
                        if free_slots[k+1]-free_slots[k] > duration and (not(k%2)):
                            value_list.append((k+1)*(k+1)*(td.total_seconds()/3600.0))

                        else :
                            value_list.append(500*(td.total_seconds()/10.00)) 

                    min_index = value_list.index(min(value_list))
                    if value_list[min_index]<500:
                        full_shedual.append({'start_time':free_slots[min_index],'end':free_slots[min_index]+timedelta(minutes=task['duration']),'name':task['name']})   

                    else:
                        print("overlap")

                else:

                    if not(index % 2):
                        free_slots=full_shedual_line[0:index+1]
                    elif (index % 2)  and deadline-full_shedual_line[index] > duration:
                        free_slots=full_shedual_line[0:index+1]  
                        free_slots.append(deadline)
                    else:
                        free_slots=full_shedual_line[0:index-1]

                    value_list=[] 
                    for k in range(len(free_slots)-1):
                        td=free_slots[k+1]-free_slots[k] 
                        if free_slots[k+1]-free_slots[k] > duration and (k%2):
                            value_list.append((k+1)*(k+1)*(td.total_seconds()/3600.0))

                        else :
                            value_list.append(500*(td.total_seconds()/10.00)) 

                    min_index = value_list.index(min(value_list))
                    if value_list[min_index]<500:
                        full_shedual.append({'start_time':free_slots[min_index],'end':free_slots[min_index]+timedelta(minutes=task['duration']),'name':task['name']})   

                    else:
                        print("overlap")                    

        else:
            end_time=start_time+timedelta(minutes=task['duration'])
            full_shedual.append({'start_time':start_time,'end':end_time,'name':task['name']})
            continue

    return full_shedual 

def main():
    tasks = []
    date_str = input("Enter the date (YYYY-MM-DD): ")
    start_date = datetime.strptime(date_str, '%Y-%m-%d')

    while True:
        name = input(f"Enter the task name or exit: ")
        if name.lower() == "exit":
            break

        weight = int(input("Enter the weight of the task (1-3): "))
        duration = int(input("Enter the duration of the task in minutes: "))
        
        if weight == 2:
            deadline_str = input("Enter the deadline (HH:MM): ")
            deadline = datetime.strptime(deadline_str, '%H:%M')
        else:
            deadline = start_date.replace(hour=22, minute=59)

        if weight == 1:
            start_time_str = input("Enter the start time (HH:MM): ")
            start_time = datetime.strptime(start_time_str, '%H:%M')
        else:
            start_time = start_date.replace(hour=7, minute=0)
        
        tasks.append({'name': name, 'weight': weight, 'duration': duration, 'deadline': deadline,'start':start_time})


    fix_tasks=get_task(tasks,FIX)                                                       # get only fix task list
    shedual_fix_tasks=get_shedual_fix_tasks(fix_tasks, start_date)

    urgent_tasks=get_task(tasks,URGENT)
    shu_ugent=get_shedual_urgent_tasks(urgent_tasks,shedual_fix_tasks, start_date)

    none_urgent_tasks=get_task(tasks,NONE_URGENT)
    shu_none_ugent=get_shedual_urgent_tasks(none_urgent_tasks,shu_ugent, start_date)

    sorted_shu = sorted(shu_none_ugent, key=lambda item: item['start_time'])
    print(sorted_shu)


if __name__ == "__main__":
    main()

