import numpy as np

class ExecutiveOffice:
    def __init__(self, name, arrival_rate):
        self.name = name
        self.arrival_rate = arrival_rate
        self.functional_managers = []

    def add_functional_manager(self, functional_manager):
        self.functional_managers.append(functional_manager)
    
    def run_simulation(self, num_tasks):
        cost = 0
        interarrival_times = np.random.exponential(1/self.arrival_rate, num_tasks)
        arrival_times = np.cumsum(interarrival_times)
        departure_times = np.zeros((len(self.functional_managers),num_tasks))
        exec_communication_success = np.random.binomial(num_tasks, (1-executiveoffice_failure_prob),1)[0]
        exec_communication_failure = num_tasks - exec_communication_success
        cost += (exec_communication_failure*(executiveoffice_failure_cost - 4*communication_cost))
        for i in range(len(self.functional_managers)):
            func_communication_success = np.random.binomial(num_tasks, (1-functionalmanager_failure_prob),1)[0]
            func_communication_failure = num_tasks - func_communication_success
            cost += (func_communication_failure*(functionalmanager_failure_cost - 2*communication_cost))
            temp = self.functional_managers[i].fm_run_simulation(arrival_times, num_tasks, cost)
            cost = temp[1]
            for j in range(num_tasks):
                departure_times[i][j] = temp[0][j]
        
        processing_times = np.zeros(num_tasks)
        for i in range(num_tasks):
            processing_times[i] = np.max(departure_times[:,i]) - arrival_times[i]
        
        return processing_times,cost
    
class FunctionalManager:
    def __init__(self, manager_id, service_rate, num_processors):
        self.manager_id = manager_id
        self.service_rate = service_rate
        self.num_processors = num_processors
    
    def add_processor(self, processor):
        self.processors.append(processor)
    
    def fm_run_simulation(self, arrival_times, num_tasks, cost):
        service_times = np.random.exponential(1/self.service_rate, num_tasks)
        wait_times = np.zeros(num_tasks)
        departure_times = np.zeros(num_tasks)
        temp = arrival_times + service_times
        task_queue = temp[0:self.num_processors]
        current_time = 0
        proc_communication_success = np.random.binomial(num_tasks, (1-processor_failure_prob),1)[0]
        proc_communication_failure = num_tasks - proc_communication_success
        cost += (proc_communication_failure*(processor_failure_cost - communication_cost))
        
        for i in range(num_tasks):
            cost += (4*communication_cost)
            minimum = np.min(task_queue)
            current_time += minimum
            index = np.argmin(task_queue)
            task_queue = np.delete(task_queue,index)
            task_queue = task_queue - minimum
            if i+self.num_processors < num_tasks:
                if arrival_times[i+self.num_processors] > current_time:
                    task_queue = np.append(task_queue,[arrival_times[i+self.num_processors]-current_time+service_times[i+self.num_processors]])
                else:
                    task_queue = np.append(task_queue,[service_times[i+self.num_processors]])
                    wait_times[i+self.num_processors] = current_time - arrival_times[i+self.num_processors]
            departure_times[i] = current_time
        
        return departure_times,cost

# Simulation parameters
arrival_rate = 3.0  # Average arrival rate of tasks per time unit
service_rate1 = 0.8  # Average service rate per time unit
service_rate2 = 0.5  # Average service rate per time unit
service_rate3 = 0.6  # Average service rate per time unit
num_tasks = 100000  # Number of tasks to simulate
num_processors = 7  # Number of processors

# Different kinds of costs
communication_cost = 7
processor_failure_cost = 20
functionalmanager_failure_cost = 1000
executiveoffice_failure_cost = 1000
processor_failure_prob = 0.05
functionalmanager_failure_prob = 0.002
executiveoffice_failure_prob = 0.0001

# Create Divisions and ProductManagers
executiveoffice = {
    "TataMotors": ExecutiveOffice("TataMotors", arrival_rate)
}

bodies_manager = FunctionalManager("Bodies", service_rate1, num_processors)
engines_manager = FunctionalManager("Engines", service_rate2, num_processors)
tyres_manager = FunctionalManager("Tyres", service_rate3, num_processors)

executiveoffice["TataMotors"].add_functional_manager(bodies_manager)
executiveoffice["TataMotors"].add_functional_manager(engines_manager)
executiveoffice["TataMotors"].add_functional_manager(tyres_manager)

temp = executiveoffice["TataMotors"].run_simulation(num_tasks)
processing_times = temp[0]
cost = temp[1]
avg_processing_time = np.mean(processing_times)
print(avg_processing_time)
print(cost)
