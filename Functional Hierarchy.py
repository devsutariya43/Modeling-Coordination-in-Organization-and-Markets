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
    
    # Top-level simulation function that will run the simulation for a given number of tasks
    def run_simulation(self, num_tasks):
        cost = 0   # cost for the whole simulation [includes coordination costs and failure costs i.e., vulnerability costs]
        interarrival_times = np.random.exponential(1/self.arrival_rate, num_tasks)   # interarrival times follow exponential distribution (Because Tasks are generated according to Poisson process)
        arrival_times = np.cumsum(interarrival_times)
        departure_times = np.zeros((len(self.functional_managers),num_tasks))
        exec_communication_success = np.random.binomial(num_tasks, (1-executiveoffice_failure_prob),1)[0]     # Failure of executive office (modeled according to binomial distribution)
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
            processing_times[i] = np.max(departure_times[:,i]) - arrival_times[i]   # Processing time of tasks is just the arrival time of the task subtracted from the max of departure time of all its different functional components  
        
        return processing_times,cost
    
# Functional Manager Class
class FunctionalManager:
    # All functional managers have ids
    # All functional managers have different service rates for their functional processors
    def __init__(self, manager_id, max_service_rate, service_rate_hm, service_rate_ai, num_processors_hm, num_processors_ai):
        self.manager_id = manager_id
        self.max_service_rate = max_service_rate
        self.service_rate_hm = service_rate_hm
        self.service_rate_ai = service_rate_ai
        self.num_processors_hm = num_processors_hm
        self.num_processors_ai = num_processors_ai  
    
    # Second-level simulation function between functional manager and processors 
    def fm_run_simulation(self, arrival_times, num_tasks, cost):
        service_times = np.zeros(num_processors_hm+num_processors_ai)
        for i in range(self.num_processors_hm):
            service_times[i] = np.random.exponential(1/self.service_rate_hm[i], 1)
        ai_service = np.random.exponential(1/self.service_rate_ai, self.num_processors_ai)
        for i in range(self.num_processors_ai):
            service_times[i+self.num_processors_hm] = ai_service[i]
        wait_times = np.zeros(num_tasks)
        departure_times = np.zeros(num_tasks)
        temp = arrival_times[0:(self.num_processors_hm+self.num_processors_ai)] + service_times
        task_queue = temp   # We will generate the task queue according to the number of processors a functional manager have under him/her
        tasks_performed = [0]*(1+self.num_processors_hm)
        initial_rates_hm = self.service_rate_hm
        initial_rate_ai = self.service_rate_ai
        current_time = 0
        proc_communication_success = np.random.binomial(num_tasks, (1-processor_failure_prob),1)[0]  # Failure of processors
        proc_communication_failure = num_tasks - proc_communication_success
        cost += (proc_communication_failure*(processor_failure_cost - communication_cost))
        
        for i in range(num_tasks):   # Simulation of tasks with tasks queue which has 'num_processors' processors
            cost += (4*communication_cost)
            minimum = np.min(task_queue)
            current_time += minimum
            index = np.argmin(task_queue)
            if (index < self.num_processors_hm):
                tasks_performed[index] += 1
            else:
                tasks_performed[-1] += 1
            if (index < self.num_processors_hm):
                self.service_rate_hm[index] = initial_rates_hm[index] + (self.max_service_rate-initial_rates_hm[index])/(1 + np.exp(-0.025*(tasks_performed[index]-1000)))
            else:
                self.service_rate_ai = initial_rate_ai + (2*self.max_service_rate-initial_rate_ai)/(1+ np.exp(-0.1*(tasks_performed[-1]-1000)))
            task_queue = np.delete(task_queue,index)
            task_queue = task_queue - minimum
            num_processors = self.num_processors_ai+self.num_processors_hm
            if i+num_processors < num_tasks:
                service_time=0
                if index < self.num_processors_hm:
                    service_time = np.random.exponential(1/self.service_rate_hm[index], 1)
                else:
                    service_time = np.random.exponential(1/self.service_rate_ai, 1)
                    
                if arrival_times[i+num_processors] > current_time:
                    task_queue = np.insert(task_queue,index,arrival_times[i+num_processors]-current_time+service_time)
                else:
                    task_queue = np.insert(task_queue,index,service_time)
                    wait_times[i+num_processors] = current_time - arrival_times[i+num_processors]
            departure_times[i] = current_time
        
        return departure_times,cost

# Simulation parameters
arrival_rate = 3.0  # Average arrival rate of tasks per time unit
service_rate1_hm = [0.8, 0.5, 0.3, 0.55, 0.8]  # Average service rate per time unit
service_rate2_hm = [0.4, 0.7, 0.6, 0.45, 0.7]  # Average service rate per time unit
service_rate3_hm = [0.2, 0.3, 0.8, 0.46, 0.6]  # Average service rate per time unit
service_rate1_ai = 0.21  # Average service rate per time unit
service_rate2_ai = 0.3  # Average service rate per time unit
service_rate3_ai = 0.3  # Average service rate per time unit
max_service_rate1 = 3.0   # Max achievable service rate
max_service_rate2 = 2.0   # Max achievable service rate
max_service_rate3 = 2.5   # Max achievable service rate
num_tasks = 100000  # Number of tasks to simulate
num_processors_hm = 1  # Number of human processors
num_processors_ai = 4  # Number of AI processors

# Different kinds of costs
communication_cost = 7  # Communication costs between any two layers of the hierarchy
processor_failure_cost = 20 # Cost of failing of processor
functionalmanager_failure_cost = 1000 # Cost of failing of functional manager
executiveoffice_failure_cost = 1000 # Cost of failing of executive office
processor_failure_prob = 0.05 # Probability of failing of processor
functionalmanager_failure_prob = 0.002 # Probabilty of failing of functional manager
executiveoffice_failure_prob = 0.0001 # Probabilty of failing of executive office

# Create an Executive Office and Functional Manager
executiveoffice = {
    "TataMotors": ExecutiveOffice("TataMotors", arrival_rate)
}

bodies_manager = FunctionalManager("Bodies",max_service_rate1, service_rate1_hm, service_rate1_ai, num_processors_hm, num_processors_ai)
engines_manager = FunctionalManager("Engines",max_service_rate2, service_rate2_hm, service_rate2_ai, num_processors_hm, num_processors_ai)
tyres_manager = FunctionalManager("Tyres",max_service_rate3, service_rate3_hm, service_rate3_ai, num_processors_hm, num_processors_ai)

executiveoffice["TataMotors"].add_functional_manager(bodies_manager)
executiveoffice["TataMotors"].add_functional_manager(engines_manager)
executiveoffice["TataMotors"].add_functional_manager(tyres_manager)

temp = executiveoffice["TataMotors"].run_simulation(num_tasks)
processing_times = temp[0]
cost = temp[1]
avg_processing_time = np.mean(processing_times)
print(avg_processing_time)
print(cost)
