class TaskObject:
    task_name = None
    start_time = None
    duration = None
    deadline = None
    value = None
    weight = None



    def print_name(self):
        print(self.name  + "add")

    def update_weight(self):
        if self.value =="1":
            self.deadline = 1
        self.weight = int(self.duration) * (1/int(self.deadline))    