from ortools.sat.python import cp_model
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class WarehouseRobotCSP:
    def __init__(self, grid_size, num_robots, num_packages, charging_stations):
        """
        Initialize the warehouse robot CSP.
        
        Args:
            grid_size: Tuple (width, height) representing the grid size
            num_robots: Number of robots
            num_packages: Number of packages
            charging_stations: List of tuples (x, y) representing charging station positions
        """
        self.grid_width, self.grid_height = grid_size
        self.num_robots = num_robots
        self.num_packages = num_packages
        self.charging_stations = charging_stations
        
        # Initialize robot properties
        self.robot_positions = [(random.randint(0, self.grid_width-1), 
                                random.randint(0, self.grid_height-1)) 
                               for _ in range(num_robots)]
        
        self.robot_capacities = [random.randint(1, 3) for _ in range(num_robots)]
        self.robot_battery = [100 for _ in range(num_robots)]
        
        # Initialize package properties
        self.package_pickup = [(random.randint(0, self.grid_width-1), 
                               random.randint(0, self.grid_height-1)) 
                              for _ in range(num_packages)]
        
        self.package_delivery = [(random.randint(0, self.grid_width-1), 
                                 random.randint(0, self.grid_height-1)) 
                                for _ in range(num_packages)]
        
        self.package_weights = [random.randint(1, 2) for _ in range(num_packages)]
        
        # Maximum time steps for planning
        self.max_time_steps = 30
    
    def solve(self):
        """
        Solve the warehouse robot problem using CP-SAT.
        
        Returns:
            Dictionary with plan details if solution is found, None otherwise
        """
        model = cp_model.CpModel()
        
        # Create variables
        
        # Robot positions over time
        robot_x = {}
        robot_y = {}
        for r in range(self.num_robots):
            for t in range(self.max_time_steps + 1):
                robot_x[(r, t)] = model.new_int_var(0, self.grid_width - 1, f'robot_{r}_x_{t}')
                robot_y[(r, t)] = model.new_int_var(0, self.grid_height - 1, f'robot_{r}_y_{t}')
        
        # Package status variables
        # Which robot is carrying the package at time t (-1 means not being carried)
        package_carrier = {}
        for p in range(self.num_packages):
            for t in range(self.max_time_steps + 1):
                package_carrier[(p, t)] = model.new_int_var(-1, self.num_robots - 1, f'package_{p}_carrier_{t}')
        
        # Whether a package has been delivered by time t
        package_delivered = {}
        for p in range(self.num_packages):
            for t in range(self.max_time_steps + 1):
                package_delivered[(p, t)] = model.new_bool_var(f'package_{p}_delivered_{t}')
        
        # Robot battery level
        robot_battery = {}
        for r in range(self.num_robots):
            for t in range(self.max_time_steps + 1):
                robot_battery[(r, t)] = model.new_int_var(0, 100, f'robot_{r}_battery_{t}')
        
        # Add constraints
        
        # Initial conditions
        for r in range(self.num_robots):
            model.add(robot_x[(r, 0)] == self.robot_positions[r][0])
            model.add(robot_y[(r, 0)] == self.robot_positions[r][1])
            model.add(robot_battery[(r, 0)] == self.robot_battery[r])
        
        # Initially no package is picked up or delivered
        for p in range(self.num_packages):
            model.add(package_carrier[(p, 0)] == -1)
            model.add(package_delivered[(p, 0)] == 0)
        
        # Movement constraints
        for r in range(self.num_robots):
            for t in range(self.max_time_steps):
                # Robots can move in cardinal directions or stay put
                # dx, dy = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
                dx = model.new_int_var(-1, 1, f'dx_{r}_{t}')
                dy = model.new_int_var(-1, 1, f'dy_{r}_{t}')
                
                # Cannot move diagonally
                no_diagonal = model.new_bool_var(f'no_diag_{r}_{t}')
                dx_zero = model.new_bool_var(f'dx_zero_{r}_{t}')
                dy_zero = model.new_bool_var(f'dy_zero_{r}_{t}')
                
                model.add(dx == 0).only_enforce_if(dx_zero)
                model.add(dx != 0).only_enforce_if(dx_zero.not_())
                model.add(dy == 0).only_enforce_if(dy_zero)
                model.add(dy != 0).only_enforce_if(dy_zero.not_())
                
                # Either dx or dy must be zero (no diagonal movement)
                model.add(dx_zero + dy_zero >= 1)
                
                # Apply movement
                model.add(robot_x[(r, t+1)] == robot_x[(r, t)] + dx)
                model.add(robot_y[(r, t+1)] == robot_y[(r, t)] + dy)
                
                # Battery consumption: 5 units for moving, 1 unit for staying put
                is_moving = model.new_bool_var(f'is_moving_{r}_{t}')
                model.add(dx != 0).only_enforce_if(is_moving)
                model.add(dy != 0).only_enforce_if(is_moving)
                model.add(dx == 0).only_enforce_if(is_moving.not_())
                model.add(dy == 0).only_enforce_if(is_moving.not_())
                
                # Battery decreases by 5 if moving, by 1 if staying put
                battery_decrease = model.new_int_var(1, 5, f'battery_decrease_{r}_{t}')
                model.add(battery_decrease == 5).only_enforce_if(is_moving)
                model.add(battery_decrease == 1).only_enforce_if(is_moving.not_())
                
                # Check if at charging station
                at_charging_station = []
                for cs_x, cs_y in self.charging_stations:
                    cs_match = model.new_bool_var(f'at_cs_{r}_{t}_{cs_x}_{cs_y}')
                    model.add(robot_x[(r, t)] == cs_x).only_enforce_if(cs_match)
                    model.add(robot_y[(r, t)] == cs_y).only_enforce_if(cs_match)
                    at_charging_station.append(cs_match)
                
                is_charging = model.new_bool_var(f'is_charging_{r}_{t}')
                model.add(sum(at_charging_station) >= 1).only_enforce_if(is_charging)
                model.add(sum(at_charging_station) == 0).only_enforce_if(is_charging.not_())
                
                # Battery charging/discharging logic
                # If charging, increase by 10 (capped at 100)
                # If not charging, decrease by battery_decrease
                new_battery = model.new_int_var(0, 100, f'new_battery_{r}_{t}')
                model.add(new_battery == min(100, robot_battery[(r, t)] + 10)).only_enforce_if(is_charging)
                model.add(new_battery == max(0, robot_battery[(r, t)] - battery_decrease)).only_enforce_if(is_charging.not_())
                model.add(robot_battery[(r, t+1)] == new_battery)
        
        # Package pickup and delivery constraints
        for p in range(self.num_packages):
            package_px, package_py = self.package_pickup[p]
            delivery_px, delivery_py = self.package_delivery[p]
            
            for t in range(self.max_time_steps):
                # Package can be picked up if a robot is at the pickup location
                # and the package is not already picked up or delivered
                for r in range(self.num_robots):
                    pickup_possible = model.new_bool_var(f'pickup_possible_{p}_{r}_{t}')
                    
                    # Robot must be at pickup location
                    model.add(robot_x[(r, t)] == package_px).only_enforce_if(pickup_possible)
                    model.add(robot_y[(r, t)] == package_py).only_enforce_if(pickup_possible)
                    
                    # Package must not be picked up yet
                    model.add(package_carrier[(p, t)] == -1).only_enforce_if(pickup_possible)
                    
                    # Robot must have enough capacity
                    # (We'd need to track current load, simplified for this example)
                    
                    # If pickup is possible and executed, update carrier
                    model.add(package_carrier[(p, t+1)] == r).only_enforce_if(pickup_possible)
                
                # Package can be delivered if robot carrying it is at delivery location
                for r in range(self.num_robots):
                    delivery_possible = model.new_bool_var(f'delivery_possible_{p}_{r}_{t}')
                    
                    # Robot must be carrying the package
                    model.add(package_carrier[(p, t)] == r).only_enforce_if(delivery_possible)
                    
                    # Robot must be at delivery location
                    model.add(robot_x[(r, t)] == delivery_px).only_enforce_if(delivery_possible)
                    model.add(robot_y[(r, t)] == delivery_py).only_enforce_if(delivery_possible)
                    
                    # If delivery is possible and executed, update status
                    model.add(package_delivered[(p, t+1)] == 1).only_enforce_if(delivery_possible)
                    model.add(package_carrier[(p, t+1)] == -1).only_enforce_if(delivery_possible)
                
                # Package remains delivered once delivered
                model.add(package_delivered[(p, t+1)] >= package_delivered[(p, t)])
                
                # Package carrier stays the same if not picked up or delivered
                no_change = model.new_bool_var(f'no_change_{p}_{t}')
                model.add(package_delivered[(p, t+1)] == package_delivered[(p, t)]).only_enforce_if(no_change)
                model.add(package_carrier[(p, t+1)] == package_carrier[(p, t)]).only_enforce_if(no_change)
        
        # Package follows robot when being carried
        for p in range(self.num_packages):
            for t in range(self.max_time_steps):
                for r in range(self.num_robots):
                    being_carried = model.new_bool_var(f'carried_{p}_{r}_{t}')
                    model.add(package_carrier[(p, t)] == r).only_enforce_if(being_carried)
        
        # Constraint: robot must have sufficient battery (at least 10%)
        for r in range(self.num_robots):
            for t in range(self.max_time_steps):
                model.add(robot_battery[(r, t)] >= 10)
        
        # Objective: minimize time to deliver all packages
        all_delivered = {}
        for t in range(self.max_time_steps + 1):
            all_delivered[t] = model.new_bool_var(f'all_delivered_{t}')
            delivered_indicators = [package_delivered[(p, t)] for p in range(self.num_packages)]
            model.add(sum(delivered_indicators) == self.num_packages).only_enforce_if(all_delivered[t])
        
        # Find minimum time when all packages are delivered
        min_delivery_time = model.new_int_var(0, self.max_time_steps, 'min_delivery_time')
        for t in range(self.max_time_steps + 1):
            # If all packages are delivered at time t, min_delivery_time <= t
            leq_t = model.new_bool_var(f'min_delivery_time_leq_{t