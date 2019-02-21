import json
import copy
from robot import Robot
from task import Task
from micro_task import MuTask

class TaskProblemParser:
    _required_keys = ['robots','tasks','micro tasks']
    _robot_required_keys = ['pos', 'type']
    _mu_task_required_keys = ['pos', 'type', 'previous']
    _task_required_keys = ['deadline', 'micro tasks', 'priority']
    @staticmethod
    def _check_required_keys(dict_to_check, required_keys):
        return all([ key in dict_to_check for key in required_keys ])
    @staticmethod
    def save_problem(file_name, robot_vector, task_vector, mu_task_vector):
        problem_dict = {}
        problem_dict['robots'] = {}
        problem_dict['tasks'] = {}
        problem_dict['micro tasks'] = {}
        for robot in robot_vector:
            problem_dict['robots'][robot.name] = { "type":robot.type, "pos": robot.position }
        for task in task_vector:
            problem_dict['tasks'][task.name] = { "priority":task.priority, "deadline":task.deadline, "micro tasks":[mu_task.name for mu_task in task.mu_tasks] }
        for mu_task in mu_task_vector:
            if mu_task.previous:
                problem_dict['micro tasks'][mu_task.name] = { "pos":mu_task.position, "type":mu_task.type, "previous": [previous.name for previous in mu_task.previous] }
            else:
                problem_dict['micro tasks'][mu_task.name] = { "pos":mu_task.position, "type":mu_task.type, "previous": [] }
        try:
            TaskProblemParser.evaluate_problem_dict(problem_dict)
            problem_json = json.dumps(problem_dict, indent=4, sort_keys=True)
            with open(file_name, 'w') as f:
                f.write(problem_json)
        except:
            pass
    @staticmethod
    def _get_all_previous(root, current, mu_task_dict):
        if current[-1] != root:
            previous_tasks = mu_task_dict[current[-1]]['previous']
            if previous_tasks != []:
                for task in previous_tasks:
                    current.append(task)
                    TaskProblemParser._get_all_previous(root, current, mu_task_dict)

    @staticmethod
    def evaluate_problem_dict(problem_dict):
        has_all_required_keys = TaskProblemParser._check_required_keys(problem_dict, TaskProblemParser._required_keys)
        if not has_all_required_keys:
            return False
        for robot in problem_dict['robots']:
            has_all_required_keys = TaskProblemParser._check_required_keys(problem_dict['robots'][robot], TaskProblemParser._robot_required_keys)
            has_extra_keys = any([ key not in TaskProblemParser._robot_required_keys for key in problem_dict['robots'][robot]])
            if not has_all_required_keys:
                raise RuntimeError('Robot '+robot+' has missing arguments')
            if has_extra_keys:
                raise RuntimeError('Robot '+robot+' has extra arguments')
            problem_dict['robots'][robot]['type'] = str(problem_dict['robots'][robot]['type'])
            if len(problem_dict['robots'][robot]['pos']) != 2:
                raise RuntimeError('Robot '+robot+' position should have two elements')
            problem_dict['robots'][robot]['pos'] = float(problem_dict['robots'][robot]['pos'][0]), float(problem_dict['robots'][robot]['pos'][1])
        previous_list = []
        for mu_task in problem_dict['micro tasks']:
            has_all_required_keys = TaskProblemParser._check_required_keys(problem_dict['micro tasks'][mu_task], TaskProblemParser._mu_task_required_keys)
            has_extra_keys = any([ key not in TaskProblemParser._mu_task_required_keys for key in problem_dict['micro tasks'][mu_task]])
            if not has_all_required_keys:
                raise RuntimeError('Micro task '+mu_task+' has missing arguments')
            if has_extra_keys:
                raise RuntimeError('Micro task '+mu_task+' has extra arguments')
            problem_dict['micro tasks'][mu_task]['type'] = str(problem_dict['micro tasks'][mu_task]['type'])
            if len(problem_dict['micro tasks'][mu_task]['pos']) != 2:
                raise RuntimeError('Micro task '+mu_task+' position should have two elements')
            problem_dict['micro tasks'][mu_task]['pos'] = float(problem_dict['micro tasks'][mu_task]['pos'][0]), float(problem_dict['micro tasks'][mu_task]['pos'][1])
            previous = problem_dict['micro tasks'][mu_task]['previous']
            for prev in previous:
                if prev not in problem_dict['micro tasks']:
                    raise RuntimeError('Micro task '+mu_task+' previous task '+prev+' is not in micro task list')
                if previous.count(prev) != 1:
                    raise RuntimeError('Micro task '+mu_task+' previous task '+prev+' appears more than once')
                if prev == mu_task:
                    raise RuntimeError('Micro task '+mu_task+' previous task '+prev+' is self')
                if prev in previous_list:
                    raise RuntimeError('Micro task '+mu_task+' previous task '+prev+' is already previous to another')
                previous_list.append(prev)
        for mu_task in problem_dict['micro tasks']:
            previous = problem_dict['micro tasks'][mu_task]['previous']
            for prev in previous:
                all_previous = [prev]
                TaskProblemParser._get_all_previous(mu_task , all_previous, problem_dict['micro tasks'])
                if mu_task in all_previous:
                    raise RuntimeError('Micro task '+mu_task+' previous task '+prev+' has itself in sucession list')
        micro_tasks_used = []
        for task in problem_dict['tasks']:
            has_all_required_keys = TaskProblemParser._check_required_keys(problem_dict['tasks'][task], TaskProblemParser._task_required_keys)
            has_extra_keys = any([ key not in TaskProblemParser._task_required_keys for key in problem_dict['tasks'][task]])
            if not has_all_required_keys:
                raise RuntimeError('Task '+task+' has missing arguments')
            if has_extra_keys:
                raise RuntimeError('Task '+task+' has extra arguments')
            problem_dict['tasks'][task]['deadline'] = float(problem_dict['tasks'][task]['deadline'])
            problem_dict['tasks'][task]['priority'] = float(problem_dict['tasks'][task]['priority'])
            for mu_task in problem_dict['tasks'][task]['micro tasks']:
                if mu_task in micro_tasks_used:
                    raise RuntimeError('Task '+task+' micro task '+mu_task+' already used by other task')
                if mu_task not in problem_dict['micro tasks']:
                    raise RuntimeError('Task '+task+' micro task '+mu_task+' was not declared in micro task list')
                micro_tasks_used.append(mu_task)

    @staticmethod
    def _dict_to_vectors(problem_dict):
        TaskProblemParser.evaluate_problem_dict(problem_dict)
        robots = []
        mu_tasks = []
        tasks = []
        for robot_name in problem_dict['robots']:
            robots.append(Robot(robot_name, problem_dict['robots'][robot_name]['type'], problem_dict['robots'][robot_name]['pos']))
        for mu_task_name in problem_dict['micro tasks']:
            mu_tasks.append(MuTask(mu_task_name, problem_dict['micro tasks'][mu_task_name]['type'], problem_dict['micro tasks'][mu_task_name]['pos']))
        for mu_task in mu_tasks:
            if problem_dict['micro tasks'][mu_task.name]['previous'] is not []:
                mu_task.previous = []
                for previous in problem_dict['micro tasks'][mu_task.name]['previous']:
                    previous_task = list(filter(lambda x: x.name == previous, mu_tasks))
                    mu_task.previous.append(previous_task[0])
        for task_name in problem_dict['tasks']:
            micro_tasks_names = problem_dict['tasks'][task_name]['micro tasks']
            task_mu_tasks = list(filter(lambda x: x.name in micro_tasks_names, mu_tasks))
            tasks.append(Task(task_name,task_mu_tasks, problem_dict['tasks'][task_name]['priority'],problem_dict['tasks'][task_name]['deadline']))
        return robots, mu_tasks, tasks

    @staticmethod
    def load(file_name):
        with open(file_name, 'r') as f:
            json_str = f.read()
            json_dict = json.loads(json_str)
            return TaskProblemParser._dict_to_vectors(json_dict)
        

class TaskDomainParser:
    _required_keys = ['task_types', 'robot_types', 'effort_function', 'reward_function']

    @staticmethod
    def _evaluate_effort_function(effort_function, robot_types, task_types):
        copy_effort_function = copy.deepcopy(effort_function)
        for robot_type in robot_types:
            if robot_type not in effort_function:
                raise RuntimeError('Missing '+robot_type+' declaration on the effort function')
            copy_effort_function_value = copy.deepcopy(effort_function[robot_type])
            for task_type in task_types:
                if task_type not in effort_function[robot_type]:
                    raise RuntimeError('Missing "'+task_type+'" for "'+robot_type+'" on the effort function')
                effort_function[robot_type][task_type] = float(effort_function[robot_type][task_type])
                copy_effort_function_value.pop(task_type)
            if len(copy_effort_function_value) is not 0:
                raise RuntimeError('To many tasks for robot "'+robot_type+'" in effort function. Invalid tasks: '+str(copy_effort_function_value))
            copy_effort_function.pop(robot_type)
        if len(copy_effort_function) is not 0:
            raise RuntimeError('To many robots in effort function. Invalid robots: '+str(copy_effort_function))

    @staticmethod
    def _evaluate_reward_function(reward_function, task_types):
        copy_reward_function = copy.deepcopy(reward_function)
        for task_type in task_types:
            if task_type not in reward_function:
                raise RuntimeError('Missing "'+task_type+'" on the reward function')
            reward_function[task_type] = float(reward_function[task_type])
            copy_reward_function.pop(task_type)
        if len(copy_reward_function) is not 0:
            raise RuntimeError('To many tasks in the reward function. Invalid tasks: '+str(copy_reward_function))
            
    @staticmethod
    def parse(filename= '', json_str='', json_dict={}):
        if filename is not '':
            with open(filename, 'r') as f:
                json_str = f.read()
            json_dict = json.loads(json_str)
        elif json_str is not '':
            json_dict = json.loads(json_str)
        elif len(json_dict) is not 0:
            json_dict = json_dict
        lowered_keys = [ key.lower() for key in json_dict ]
        contains_all_required_keys = all([(required_key in lowered_keys) for required_key in TaskDomainParser._required_keys])
        if not contains_all_required_keys:
            return None
        TaskDomainParser._evaluate_effort_function(json_dict['effort_function'], json_dict['robot_types'], json_dict['task_types'])
        TaskDomainParser._evaluate_reward_function(json_dict['reward_function'], json_dict['task_types'])
        return json_dict

if __name__ == "__main__":
    TaskDomainParser.parse('tasks_definitions.json')
    TaskProblemParser.load('teste.json')
    
