import numpy as np

class Division:
    def __init__(self, name, arrival_rate):
        self.name = name
        self.productmanagers = []
        self.arrival_rate = arrival_rate

    def add_productmanager(self, productmanager):
        self.productmanagers.append(productmanager)
        
    def run_simulation(self, num_tasks):
        cost = 0
        num_PMs = len(self.productmanagers)
        Results = []
        for i in range(num_PMs):
            interarrival_times = np.random.exponential(1/self.arrival_rate, num_tasks)
            arrival_times = np.cumsum(interarrival_times)
            communication_success = np.random.binomial(num_tasks, (1-productmanager_failure_prob), 1)[0]
            communication_failure = num_tasks - communication_success
            cost += (communication_failure*(productmanager_failure_cost - 2*communication_cost))
            temp = self.productmanagers[i].pm_run_simulation(arrival_times, num_tasks, cost)
            cost = temp[2]
            Results.append(temp[1])
        
        return Results,cost


class ProductManager:
    def __init__(self, name, num_processors, service_rates):
        self.name = name
        self.num_processors = num_processors
        self.service_rates = service_rates
    
    def pm_run_simulation(self, arrival_times, num_tasks, cost):
        service_times = []
        departure_times = np.zeros((num_processors,num_tasks))
        wait_times = np.zeros((num_processors,num_tasks))
        for i in range(num_processors):
            service_times.append(np.random.exponential(1/self.service_rates[i], num_tasks))
        
        for i in range(num_processors):
            departure_times[i][0] = service_times[i][0]
            for j in range(1,num_tasks):
                departure_times[i][j] = max(arrival_times[j], departure_times[i-1][j]) + service_times[i][j]
                wait_times[i][j] = max(0, departure_times[i-1][j] - arrival_times[j])
        
        processing_times = np.zeros(num_tasks)
        task_success = np.random.binomial(num_tasks, (1-processor_failure_prob), 1)[0]
        task_failure = num_tasks - task_success
        cost += (task_failure*processor_failure_cost)
        for i in range(num_tasks):
            processing_times[i] = np.max(departure_times[:,i]) - arrival_times[i]
            cost += (2*communication_cost)
        
        avg_wait_times = np.zeros(num_processors)
        for i in range(num_processors):
            avg_wait_times[i] = np.mean(wait_times[i])
        
        return avg_wait_times,processing_times,cost


# Simulation parameters
arrival_rate = 7.0  # Average arrival rate of tasks per time unit
service_rates = [0.7, 0.5, 0.9]  # Average service rate per time unit
num_tasks = 100000  # Number of tasks to simulate
num_processors = 3  # Number of processors

# Different kinds of costs
communication_cost = 5
processor_failure_cost = 20
productmanager_failure_cost = 1000
processor_failure_prob = 0.05
productmanager_failure_prob = 0.002

# Create Divisions and ProductManagers
divisions = {
    "TataMotors": Division("TataMotors", arrival_rate)
}

rangerover_manager = ProductManager("RangeRover Manager", num_processors, service_rates)
jaguar_manager = ProductManager("Jaguar Manager", num_processors, service_rates)
nexon_manager = ProductManager("Nexon Manager", num_processors, service_rates)

divisions["TataMotors"].add_productmanager(rangerover_manager)
divisions["TataMotors"].add_productmanager(jaguar_manager)
divisions["TataMotors"].add_productmanager(nexon_manager)

temp = divisions["TataMotors"].run_simulation(num_tasks)
Results = temp[0]
cost = temp[1]
processing_times = []
for i in range(len(Results)):
    processing_times.append(np.mean(Results[i]))
    
print(processing_times)
print(cost)
