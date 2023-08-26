import numpy as np

# Division Class
class Division:
    # Division has different kinds of products under it
    # Which is maintained by product manager
    # System has a common arrival rate as whole
    def __init__(self, name, arrival_rate):
        self.name = name
        self.productmanagers = []
        self.arrival_rate = arrival_rate

    def add_productmanager(self, productmanager):
        self.productmanagers.append(productmanager)
        
    # Top level simulaiton function    
    def run_simulation(self, num_tasks):
        cost = 0   # Cost of tasks for the simulation
        num_PMs = len(self.productmanagers)   # Number of Products i.e., nnumber of product managers
        Results = []
        for i in range(num_PMs):   # Each product manager is getting tasks according to poisson process
            interarrival_times = np.random.exponential(1/self.arrival_rate, num_tasks)
            arrival_times = np.cumsum(interarrival_times)
            communication_success = np.random.binomial(num_tasks, (1-productmanager_failure_prob), 1)[0]   # Failure of product manager to assign tasks to processors
            communication_failure = num_tasks - communication_success
            cost += (communication_failure*(productmanager_failure_cost - 2*communication_cost))   # Cost of failing of product manager
            temp = self.productmanagers[i].pm_run_simulation(arrival_times, num_tasks, cost)   # Second level simulation function
            cost = temp[2]   # Updating the costs (which adds communication costs and costs pf failure of processors)
            Results.append(temp[1])
        
        return Results,cost

# Product Manager Class
class ProductManager:
    # Each product manager has some number of processors
    # Each processor has different service rate according to its function
    def __init__(self, name, num_processors, service_rates):
        self.name = name
        self.num_processors = num_processors
        self.service_rates = service_rates
    
    # Second level simulation function which assign tasks to all the processors according to their functionalities
    def pm_run_simulation(self, arrival_times, num_tasks, cost):
        service_times = []
        departure_times = np.zeros((num_processors,num_tasks))
        wait_times = np.zeros((num_processors,num_tasks))
        for i in range(num_processors):   # Creating a 2D list of service times for different processors under the given product manager (service time will follow exponential distribution)
            service_times.append(np.random.exponential(1/self.service_rates[i], num_tasks))
        
        for i in range(num_processors):   # Running the simulation and updating the departure times and wait times
            departure_times[i][0] = service_times[i][0]
            for j in range(1,num_tasks):
                departure_times[i][j] = max(arrival_times[j], departure_times[i-1][j]) + service_times[i][j]
                wait_times[i][j] = max(0, departure_times[i-1][j] - arrival_times[j])
        
        processing_times = np.zeros(num_tasks)
        task_success = np.random.binomial(num_tasks, (1-processor_failure_prob), 1)[0]   # Failure of processors
        task_failure = num_tasks - task_success
        cost += (task_failure*processor_failure_cost)   # Adding cost of failing of processors
        for i in range(num_tasks):
            processing_times[i] = np.max(departure_times[:,i]) - arrival_times[i]   # Processing time os just arrival time subtracted from the max of the departure time of a procduct from processors
            cost += (2*communication_cost)   # Adding communication cost
        
        avg_wait_times = np.zeros(num_processors)
        for i in range(num_processors):
            avg_wait_times[i] = np.mean(wait_times[i])
        
        return avg_wait_times,processing_times,cost


# Simulation parameters 
arrival_rate = 7.0  # Average arrival rate of tasks per time unit
service_rates1 = [0.7, 0.5, 0.9]  # Average service rate per time unit
service_rates2 = [0.5, 1.5, 0.3]  # Average service rate per time unit
service_rates3 = [1.1, 0.8, 0.6]  # Average service rate per time unit
num_tasks = 100000  # Number of tasks to simulate
num_processors = 3  # Number of processors

# Different kinds of costs
communication_cost = 5 # Communocation Cost between any two layers of hierarchy
processor_failure_cost = 20 # Cost of failing of processors
productmanager_failure_cost = 1000 # Cost of failing of product manager
processor_failure_prob = 0.05 # Probability of failing of processors
productmanager_failure_prob = 0.002 # Probabilty of failing of product manager

# Create Divisions and ProductManagers
divisions = {
    "TataMotors": Division("TataMotors", arrival_rate)
}

rangerover_manager = ProductManager("RangeRover Manager", num_processors, service_rates1)
jaguar_manager = ProductManager("Jaguar Manager", num_processors, service_rates2)
nexon_manager = ProductManager("Nexon Manager", num_processors, service_rates3)

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