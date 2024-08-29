import numpy as np
from mealpy.optimizer import Optimizer
from mealpy.utils.agent import Agent

from typing import List, Union, Tuple, Dict
from mealpy.utils.agent import Agent
from mealpy.utils.problem import Problem
from math import gamma
from mealpy.utils.history import History
from mealpy.utils.target import Target
from mealpy.utils.termination import Termination
from mealpy.utils.logger import Logger
from mealpy.utils.validator import Validator
import concurrent.futures as parallel
from functools import partial
import os
import time
import math
import random
from utils.util import generateRandomVector
class PSO_CP(Optimizer):
    """
    The original version of: PSO with composite particles (PSO-CP),

    Hyper-parameters should fine-tune in approximate range to get faster convergence toward the global optimum:
        + c1 (float): [1, 3], local coefficient, default = 2.05
        + c2 (float): [1, 3], global coefficient, default = 2.05
        + w (float): (0., 1.0), Weight min of bird, default = 0.4

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy import FloatVar, PSO
    >>>
    >>> def objective_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict = {
    >>>     "bounds": FloatVar(lb=(-10.,) * 30, ub=(10.,) * 30, name="delta"),
    >>>     "obj_func": objective_function,
    >>>     "minmax": "min",
    >>> }
    >>>
    >>> model = PSO.OriginalPSO(epoch=1000, pop_size=50, c1=2.05, c2=20.5, w=0.4)
    >>> g_best = model.solve(problem_dict)
    >>> print(f"Solution: {g_best.solution}, Fitness: {g_best.target.fitness}")
    >>> print(f"Solution: {model.g_best.solution}, Fitness: {model.g_best.target.fitness}")

    References
    ~~~~~~~~~~
    Liu, L., Yang, S., & Wang, D. (2010). Particle swarm optimization with composite particles in dynamic environments. 
    IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics), 40(6), 1634-1648.
    """

    def __init__(self, epoch: int = 200, pop_size: int = 100, c1: float = 2.05, c2: float = 2.05, w: float = 0.4, **kwargs: object) -> None:
        """
        Args:
            epoch: maximum number of iterations, default = 10000
            pop_size: number of population size, default = 100
            c1: [0-2] local coefficient
            c2: [0-2] global coefficient
            w_min: Weight min of bird, default = 0.4
        """
        super().__init__(**kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [5, 10000])
        self.c1 = self.validator.check_float("c1", c1, (0, 5.0))
        self.c2 = self.validator.check_float("c2", c2, (0, 5.0))
        self.w = self.validator.check_float("w", w, (0, 1.0))
        self.set_parameters(["epoch", "pop_size", "c1", "c2", "w"])
        self.sort_flag = False
        self.is_parallelizable = False
    
    # Generate VAR vector 
    def generateVAR_Vector(self, agent):
        var = []  
        max = np.amax(agent.velocity)
        for v in agent.velocity:
            var.append(self.generator.uniform(0, math.exp(-abs(v/max))))
        return  var
    
    def initialize_variables(self):
        self.v_max = 0.5 * (self.problem.ub - self.problem.lb)
        self.v_min = -self.v_max

    def generate_empty_agent(self, solution: np.ndarray = None) -> Agent:
        if solution is None:
            solution = self.problem.generate_solution(encoded=True)
        velocity = self.generator.uniform(self.v_min, self.v_max)
        local_pos = solution.copy()
        return Agent(solution=solution, velocity=velocity, local_solution=local_pos)

    def generate_agent(self, solution: np.ndarray = None) -> Agent:
        agent = self.generate_empty_agent(solution)
        agent.target = self.get_target(agent.solution)
        agent.local_target = agent.target.copy()
        return agent

    def amend_solution(self, solution: np.ndarray) -> np.ndarray:
        condition = np.logical_and(self.problem.lb <= solution, solution <= self.problem.ub)
        pos_rand = self.generator.uniform(self.problem.lb, self.problem.ub)
        return np.where(condition, solution, pos_rand)
    
    def findAgentByID(self, pop: List[Agent], id) -> Agent:
        
        for a in pop:
            if a.id == id:
                return a
            
    def computeComposite_Particles(self, pop: List[Agent]) -> List[Agent]:
        
        composite_Particles = []
        # pop_temp contains sorted population
        Nc = math.ceil((self.pop_size -1)/3)
        pop_temp, best, worst = self.get_special_agents(self.pop, n_best=1, n_worst=Nc, minmax=self.problem.minmax)
        
        for i in range(Nc):
            x_worst = worst[i]
            composite_Particles.append(x_worst)
            pop_temp.pop() # Remove the worset solution
            #Calculate Euclidien distance
            distances = {}
            for ag in pop_temp:
               distances.update ({"id":ag.id, "distance":np.linalg.norm(ag.solution - x_worst.solution)})
            temps = sorted(distances.items(), key=lambda x:x[1])
            
            #find Agent by Id
            comp_i =[] 
            Agent1 = self.findAgentByID(pop_temp, temps[0])
            Agent2 = self.findAgentByID(pop_temp, temps[1])  
            comp_i.append(Agent1)
            comp_i.append(Agent2)
                    
            composite_Particles.append({"id":x_worst.id, "elementary_Particles":comp_i})
            
        return composite_Particles
           
    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        R_Step = 6
        composites =self.computeComposite_Particles(self.pop)
        for c in composites:
            #var operation
            worst= self.findAgentByID(c["id"])
            Point_A= c["elementary_Particles"][0]
            Point_B= c["elementary_Particles"][1]
            M = generateRandomVector(Point_A.solution, Point_B.solution)
            Reflection_Point = M - R_Step*self.generateVAR_Vector(worst, self.pop)*(worst.solution - M)
            eval_Reflection = self.get_target(Reflection_Point)
            if eval_Reflection.target.fitness > worst.target.fitness:
                worst.update(local_solution=Reflection_Point.copy(), local_target=eval_Reflection.copy())
            
            pioneer_particle = Point_B.copy() if Point_A.target.fitness < Point_B.target.fitness else Point_A.copy()
            self.pop.append(pioneer_particle)
            c.update({"pioneer":pioneer_particle})
        # Update weight after each move count  (weight down)
        for idx in range(0, self.pop_size):
            cognitive = self.c1 * self.generator.random(self.problem.n_dims) * (self.pop[idx].local_solution - self.pop[idx].solution)
            social = self.c2 * self.generator.random(self.problem.n_dims) * (self.g_best.solution - self.pop[idx].solution)
            self.pop[idx].velocity = self.w * self.pop[idx].velocity + cognitive + social
            pos_new = self.pop[idx].solution + self.pop[idx].velocity
            pos_new = self.correct_solution(pos_new)
            target = self.get_target(pos_new)
            if self.compare_target(target, self.pop[idx].target, self.problem.minmax):
                self.pop[idx].update(solution=pos_new.copy(), target=target.copy())
            if self.compare_target(target, self.pop[idx].local_target, self.problem.minmax):
                self.pop[idx].update(local_solution=pos_new.copy(), local_target=target.copy())
        
        for c in composites:
            pionerInPop = self.findAgentByID(self.pop)
            dist = np.linalg.norm(pionerInPop.solution - c["pioneer"].solution)
            # Update Particles: 1 and 2
            for i in range(0, 2):
                pos_new1 = self.correct_solution(c["elementary_Particles"][i].solution + dist)
                target1 = self.get_target(pos_new1)
                c["elementary_Particles"][i].update(local_solution=pos_new1.copy(), local_target=target1.copy())           
    
    def solve(self, problem: Union[Dict, Problem] = None, mode: str = 'single', n_workers: int = None,
              termination: Union[Dict, Termination] = None, starting_solutions: Union[List, np.ndarray, Tuple] = None,
              seed: int = None) -> Agent:
        """
        Args:
            problem: an instance of Problem class or a dictionary
            mode: Parallel: 'process', 'thread'; Sequential: 'swarm', 'single'.

                * 'process': The parallel mode with multiple cores run the tasks
                * 'thread': The parallel mode with multiple threads run the tasks
                * 'swarm': The sequential mode that no effect on updating phase of other agents
                * 'single': The sequential mode that effect on updating phase of other agents, this is default mode

            n_workers: The number of workers (cores or threads) to do the tasks (effect only on parallel mode)
            termination: The termination dictionary or an instance of Termination class
            starting_solutions: List or 2D matrix (numpy array) of starting positions with length equal pop_size parameter
            seed: seed for random number generation needed to be *explicitly* set to int value

        Returns:
            g_best: g_best, the best found agent, that hold the best solution and the best target. Access by: .g_best.solution, .g_best.target
        """
        self.check_problem(problem, seed)
        self.check_mode_and_workers(mode, n_workers)
        self.check_termination("start", termination, None)
        self.initialize_variables()

        self.before_initialization(starting_solutions)
        self.initialization()
        self.after_initialization()

        self.before_main_loop()
        # compute  composite particles List
              
        for epoch in range(1, self.epoch + 1):
            time_epoch = time.perf_counter()

            ## Evolve method will be called in child class
            self.evolve(epoch)

            # Update global best solution, the population is sorted or not depended on algorithm's strategy
            pop_temp, self.g_best = self.update_global_best_agent(self.pop)
            if self.sort_flag: self.pop = pop_temp

            time_epoch = time.perf_counter() - time_epoch
            self.track_optimize_step(self.pop, epoch, time_epoch)
            if self.check_termination("end", None, epoch):
                break
        self.track_optimize_process()
        return self.g_best