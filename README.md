<!--StartFragment-->


## <!--StartFragment--> Modeling-Coordination-in-Organization-and-Markets <!--StartFragment-->

  ### Product Hierarchy Brief

  - For product hierarchy we have considered an overall arrival rate for the system as whole.

  - For the service rate we have considered that different processors under product manager will have different service rates. Also processors working on building same thing but under different product manager can also have different service rates.

  - Tata’s rangerover product manger will have different processors making engines,tyres, car bodies  with service rate µ1, µ2, µ3 …  while Jaguar's product manager will have processors making  engines,tyres, car bodies with µ1, µ2, µ3 … so on would be different.

  - System would receive order for a product according to Poisson Process and we have considered one order at a time (but can be easily modified to n orders from one buyer).

  - Also we have given orders to different product manager independently (We can also do it where order comes and Executive deligates it to appropriate Product manager)

  - Simulation Parameters 

    - Arrival rate

    - Service rates

    - Num  of tasks

    - Num of processors under product manager

  - Cost Analysis Parameters

    - Communication Cost

    - Processors failure cost

    - Product manager failure cost

    - Processor failure probability

    - Product manager failure probability

  - Results from Simulation

    - Cost

    - Processing times for every order placed

    - Avg. Processing time

  ### Functional Hierarchy Brief

  - For functional hierarchy we have considered an overall arrival rate for the system.

  - For the service rate we have made two different types of processors under every functional manager which are Human and AI. We can give any number of processors under a certain functional manager in any proposition of Human and AI. Also service rates for all AI processors will be the same. And learning of one processor will update the service rate of all AI processors. While for humans service rates will be different. And according to the number of tasks they perform their learning will increase.

  - System would receive orders for a product according to the Poisson Process and we have considered one order at a time (but can be easily modified to n orders from one buyer).

  - Also on receiving orders the executive office delegates tasks to functional manager and functional manager to the first available processor. Every functional manager has a number of processors.

  - Simulation Parameters 

    - Arrival rate

    - Service rates (different for diff. func. manager also diff. For AI & Humans)

    - Num  of tasks

    - Num of processors under functional managers

  - Cost Analysis Parameters

    - Communication Cost

    - Processors failure cost

    - Functional manager failure cost

    - Executive office failure cost

    - Processor failure probability

    - Functional manager failure probability

    - Executive office failure probability

  - Results from Simulation

    - Cost

    - Processing times for every order placed

    - Avg. Processing time

  ### _ANALYSIS POST ADDITION of Multi-Facilitating Processors:_

  i) **Processors with constant learning rates:**

  - It was observed that since task efficiency was directly proportional to the number of tasks performed by a processor and the slope of the learning curve. In a long term analysis VIA SIMULATIONS ABOVE, optimal processor ratio was obtained to be a complete set of HUMAN processors or a complete set of AI processors depending upon which of them had a higher learning rate which  is also in agreement with the intuitive answer.

  - The results are independent of the type of Hierarchy used, i.e. Product or Functional.

  ii) **Processors with both AI and Human Preprocessors and no learning rates:**

  - In this scenario, we have processors of two different types: AI and Human. However, there are no learning rates provided, which implies that the processors don't have specific learning rates associated with them. In this case, we don't have explicit information to calculate the workforce ratio based on learning rates.

  * However, we can still analyse the workforce distribution based on other factors such as processing speed, task handling capacity, and availability.

  **iii) Product with AI processors with learning rate and Human with no learning rates:**

  - In this case we have Humans having higher service rate initially so if we are performing tasks for a short time scale ie., our goal is to optimise workforce ratio for a short time scale so Humans will overtake AI as they have higher service rate.

  - But if we are looking for an optimal workforce ratio for a long term run then AI would dominate humans as they have lower service rate initially but they have got a learning rate and hence will end up having higher service rate than humans.

  **iv) Product with Human only and learning Rate:**

  - As discussed above in this case we have AI having higher service rate initially so if we are performing tasks for a short time scale ie., our goal is to optimise workforce ratio for a short term scale so that AI will overtake Humans as they have higher service rate.

  - But if we are looking for an optimal workforce ratio for a long term run than Humans in this case would dominate AI as they have lower service rate initially but they have got a learning rate and hence will end up having higher service rate than AI.

  **v)  FINALLY, Product with both HUMAN and AI learning RATEs:**

  - This is much more complex case when both have learning rates. There are multiple cases for learning rates of both and service rate at starting. Firstly we can use different learning curves. But we have used SIGMOID function for the best result.

  - Now another thing is that we assume that the AIs will have lower service rate at start than the Humans but their learning will be much higher than the humans. Also we have set tasks barriers after which learning will start to rise significantly and also max learning rate.

  ### FUTURE EXTENSIONS:

  While our current paper delves comprehensively into fundamental aspects within the allocated time, several noteworthy avenues for future research remain unexplored. These potential extensions include delving deeper into the impact of external variables on our findings, conducting longitudinal studies to assess the sustainability of our proposed model, investigating other variations to hierarchies pertaining to the modern world to ensure broader applicability, and to enhance implementation efficiency. These uncharted domains promise valuable insights and could contribute significantly to the robustness and applicability of our work.

  1. **Identifying optimal workforce size given task requirements:**

  - Given an array of n unique tasks and the amount of each needed to be achieved. Optimise workforce size keeping in mind time constraints, various costs (communication costs, failure costs, other vulnerability costs) and other requirements ( can be non-linear)  to choose a hierarchy and workforce size for efficient operations.

  2. **Identifying optimal workforce ratio  (human : ai):** 

  - Given an array of n unique tasks and the amount of each needed to be achieved. Optimise workforce size keeping in mind time constraints, various costs (communication costs, failure costs, other vulnerability costs) and other requirements ( can be non-linear)  to choose a hierarchy and workforce ratio for efficient operations.

  3. **Modifying simulation to various observed  learning rates by Data Observation:**

  - While purely mathematical and deterministic  learning rate functions we assumed to simplify the simulation’s implementation these assumptions might not hold in the real world where learning rates are non-stationary stochastic and non-monotonic in nature and are also prone to psychological and environmental factors(at least for HUMAN processors). Objective can be to observe data and try to model Learning Rates by  fitting Regression Models/Neural Networks of various observables .

  4. **Introducing Collaborative learning:**

  - An interesting real world scenario that can give unique results is the case of coalition among various types of Processors ( human, ai). One such example might be usage of CHATGPT by humans to boost their efficiency and in turn chat gpt using human interaction to boost its efficiency. This kind of collaborative learning rate wherein preprocessors are dependent on each other may have far reaching applications.

  <!--EndFragment--><!--EndFragment--><!--EndFragment--><!--EndFragment--><!--EndFragment--><!--EndFragment--><!--EndFragment--><!--EndFragment-->

<!--EndFragment-->
