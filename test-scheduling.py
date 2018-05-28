''' Runs greedy algorithm to schedule tasks on machines
'''
import ast

def main():
    ''' Main method '''

    input_filename = input('Enter the name of the instance file (with extension): ')
    input_file = open(input_filename)

    tasks, machines_list, resource_list = parse_input(input_file)

    # machines_list = ['m'+str(i) for i in range(1, 4)]
    # resource_list = ['r1']

    # Run the algorithm
    results = sorted([
        run_schedule(tasks, machines_list, resource_list, 'SHORTEST_FIRST'),
        run_schedule(tasks, machines_list, resource_list, 'LONGEST_FIRST'),
        run_schedule(tasks, machines_list, resource_list, 'REQUIREMENTS_FIRST')
        ])

    best_makespan = results[0][0]
    best_schedule = results[0][1]

    output_file = open('res-' + input_filename, 'w')
    for item in best_schedule:
        output_file.write(item + '\n')
    output_file.close()
    print("Best makespan:", best_makespan)
    # print("Best schedule:", best_schedule)

def parse_input(file):
    ''' Parses input file.

    Arguments:
    file -- input file
    '''
    tasks = {}
    machines_list = []
    resource_list = []

    for line in file:

        if line.startswith('test( '):
            line_list = [x for x in line.split(', ')]

            test_name = ast.literal_eval(line_list[0].lstrip('test( '))
            test_duration = int(line_list[1])
            test_machines = ast.literal_eval(line_list[2])
            test_resources = ast.literal_eval(line_list[3].rstrip(').\n'))

            tasks.update({test_name: {'duration': test_duration,
                                      'machines': test_machines,
                                      'resources': test_resources}})

        elif line.startswith('embedded_board( '):
            parsed = ast.literal_eval(line.strip('embedded_board( ).\n'))
            machines_list.append(parsed)

        elif line.startswith('resource( '):
            parsed = ast.literal_eval(line.strip('resource( , 1).\n'))
            resource_list.append(parsed)
    return tasks, machines_list, resource_list

def uses_global_resource(tasks, task):
    ''' Checks whether given task uses any global
    resources

    Arguments:
    tasks -- dictionary containing specifications for all tasks
    task -- task in question
    '''
    return bool(tasks[task]['resources'])

def all_global_resources_available(global_res_next_available, tasks, task, time):
    ''' Checks whether all global resources that the given
    task uses are available

    Arguments:
    global_res_next_available -- list containing times when each global resource is next available
    tasks -- dictionary containing specifications for all tasks
    task -- task in question
    time -- point in time for which a check is wanted
    '''
    for res in tasks[task]['resources']:
        if global_res_next_available[res] > time:
            return False
    return True

def reserve_global_resources(global_res_next_available, current_time, tasks, task):
    ''' Reserves all global resources that the task in question requires

    Arguments:
    global_res_next_available -- list containing times when each global resource is next available
    current_time -- current point in time during execution of the algorithm
    tasks -- dictionary containing specifications for all tasks
    task -- task in question
    '''
    for res in tasks[task]['resources']:
        global_res_next_available[res] = current_time + tasks[task]['duration']
        # print('Global resource', res, 'next available at', global_res_next_available[res])

def sort_tasks(tasks, tasks_sort_method):
    ''' Sorts tasks according to selected sort method

    Arguments:
    tasks -- dictionary containing specifications for all tasks
    tasks_sort_method -- sort method
    '''

    tasks_durations = {key : tasks[key]['duration'] for key in tasks}

    if tasks_sort_method == 'SHORTEST_FIRST':
        return sorted(tasks_durations, key=tasks_durations.__getitem__)

    elif tasks_sort_method == 'LONGEST_FIRST':
        return sorted(tasks_durations, key=tasks_durations.__getitem__, reverse=True)

    elif tasks_sort_method == 'REQUIREMENTS_FIRST':
        task_names = [task for task in tasks]
        tasks_sorted = []
        for tsk in tasks:
            if tasks[tsk]["resources"]:
                tasks_sorted.append(tsk)
                task_names.remove(tsk)
        tasks_sorted.extend(task_names)
        return tasks_sorted

def run_schedule(tasks, machines_list, resource_list, tasks_sort_method):
    ''' Main "worker" function, runs the algorithm itself

    Arguments:
    tasks -- dictionary containing specifications for all tasks
    machines_list -- list of all machines
    resource_list -- list of all global resources
    tasks_sort_method -- method of sorting unscheduled tasks
    '''

    machine_next_available = {machine : 0 for machine in machines_list}
    global_res_next_available = {resource : 0 for resource in resource_list}
    current_time = 0
    results = []
    max_time = 0

    tasks_sorted = sort_tasks(tasks, tasks_sort_method)

    # While there are still (unscheduled) tasks
    while tasks_sorted:

        assigned_tasks = []

        # print('New iteration...')

        for current_task in tasks_sorted:
            # print('Current task: ' + current_task)

            # If the task has no specified machines, it means the task can be executed
            # on any machine, so add all of them to the list of possible machines
            if not tasks[current_task]['machines']:
                for machine in machines_list:
                    tasks[current_task]['machines'].append(machine)

            # If the task either doesn't use global resources at all or they are all available
            if (not(uses_global_resource(tasks, current_task)) or
                    all_global_resources_available(global_res_next_available,
                                                   tasks, current_task, current_time)):

                # For each machine the task can be executed on...
                for possible_machine in tasks[current_task]['machines']:

                    # If this particular candidate machine has become available at or
                    # before current point in time (in short, if it is available),
                    # then the task can be assigned to it, starting at the current time
                    if machine_next_available[possible_machine] <= current_time:

                        assigned_tasks.append(current_task)

                        # Remember maximum makespan
                        if current_time + tasks[current_task]['duration'] > max_time:
                            max_time = current_time + tasks[current_task]['duration']

                        # print('Scheduled: ', current_task, current_time, possible_machine)
                        results.append("'%s',%d,'%s'." %
                                       (current_task, current_time, possible_machine))

                        # Machine that the task was just now scheduled on will be reserved for
                        # the duration of the task
                        machine_next_available[possible_machine] = (current_time +
                                                                    tasks[current_task]['duration'])

                        # Additionally, if the task uses some global resources, reserve them too
                        if uses_global_resource(tasks, current_task):
                            reserve_global_resources(global_res_next_available,
                                                     current_time, tasks, current_task)

                        break
        current_time += 1

        # Remove all tasks that were assigned in this current iteration from the list of tasks
        for task in assigned_tasks:
            tasks_sorted.remove(task)
        # print(tasks_sorted)

    # print('Konacno: ', results)
    print('Makespan (', tasks_sort_method, ')', max_time)

    return max_time, results

if __name__ == '__main__':
    main()
