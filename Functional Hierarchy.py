import numpy as np

# Exectuive Office Class
class ExecutiveOffice:
    # System has a common arrival rate as whole
    # Executive office class has lists of all functional managers
    def __init__(self, name, arrival_rate):
        self.name = name
        self.arrival_rate = arrival_rate
        self.functional_managers = []

    def add_functional_manager(self, functional_manager):
        self.functional_managers.append(functional_manager)
    
    # Top level simulation function that will run the simulation for given number of tasks
    def run_simulation(self, num_tasks):
        cost = 0   # cost for the whole simulation [includes coordination costs and failure costs i.e., vulneribility costs]
        interarrival_times = np.random.exponential(1/self.arrival_rate, num_tasks)   # interarrival times follows exponential distribution (Because Tasks are generated according to possion process)
        arrival_times = np.cumsum(interarrival_times)
        departure_times = np.zeros((len(self.functional_managers),num_tasks))
        exec_communication_success = np.random.binomial(num_tasks, (1-executiveoffice_failure_prob),1)[0]     # Failure of executive office (modeled accoridng to binomial distribution)
        exec_communication_failure = num_tasks - exec_communication_success
        cost += (exec_communication_failure*(executiveoffice_failure_cost - 4*communication_cost))  # extra cost of failure gets added
        for i in range(len(self.functional_managers)):   # Delegation of tasks to all the functional managers
            func_communication_success = np.random.binomial(num_tasks, (1-functionalmanager_failure_prob),1)[0]   # Failure of functional managers
            func_communication_failure = num_tasks - func_communication_success
            cost += (func_communication_failure*(functionalmanager_failure_cost - 2*communication_cost))
            temp = self.functional_managers[i].fm_run_simulation(arrival_times, num_tasks, cost)  # Second level simulation function which runs between the functional manager and processors
            cost = temp[1]   # Updated costs (addition of communication costs and processor failure costs)
            for j in range(num_tasks):
                departure_times[i][j] = temp[0][j]
        
        processing_times = np.zeros(num_tasks)
        for i in range(num_tasks):
            processing_times[i] = np.max(departure_times[:,i]) - arrival_times[i]   # Processing time of a tasks is just arrival time of task subtracted from max of departure time of all its different functional components  
        
        return processing_times,cost
    
# Functional Manager Class
class FunctionalManager:
    # All functional managers have ids
    # All functional managers have different service rates of their functional processors
    def __init__(self, manager_id, service_rate, num_processors):
        self.manager_id = manager_id
        self.service_rate = service_rate
        self.num_processors = num_processors
    
    def add_processor(self, processor):
        self.processors.append(processor)
    
    # Second level simulation function between functional manager and processors 
    def fm_run_simulation(self, arrival_times, num_tasks, cost):
        service_times = np.random.exponential(1/self.service_rate, num_tasks)   # Service time follows exponential distribution
        wait_times = np.zeros(num_tasks)
        departure_times = np.zeros(num_tasks)
        temp = arrival_times + service_times
        task_queue = temp[0:self.num_processors]   # We will generate the task queue accoridng to the number of processors a functional manager have under him/her
        current_time = 0
        proc_communication_success = np.random.binomial(num_tasks, (1-processor_failure_prob),1)[0]  # Failure of processors
        proc_communication_failure = num_tasks - proc_communication_success
        cost += (proc_communication_failure*(processor_failure_cost - communication_cost))
        
        for i in range(num_tasks):   # Simulation of tasks with tasks queue which has 'num_processors' processors
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
communication_cost = 7  # Communication costs between any two layers of hierarchy
processor_failure_cost = 20 # Cost of failing of processor
functionalmanager_failure_cost = 1000 # Cost of failing of functional manager
executiveoffice_failure_cost = 1000 # Cost of failing of executive office
processor_failure_prob = 0.05 # Probability of failing of processor
functionalmanager_failure_prob = 0.002 # Probabilty of failing of functional manager
executiveoffice_failure_prob = 0.0001 # Probabilty of failing of executive office

# Create Executive Office and Functional Manager
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
