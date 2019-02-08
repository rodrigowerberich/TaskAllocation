import json
import copy

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
                raise RuntimeError('To many tasks for robot'+robot_type+' in effort function. Invalid tasks: '+str(copy_effort_function_value))
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
    print(TaskDomainParser.parse('tasks_definitions.json'))    
    
