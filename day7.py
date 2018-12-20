import attr
import collections
from utils import read_input


Instruction = collections.namedtuple("Instruction", ["prereq", "action"])


test_input = [Instruction('C', 'A'),
              Instruction('C', 'F'),
              Instruction('A', 'B'),
              Instruction('A', 'D'),
              Instruction('B', 'E'),
              Instruction('D', 'E'),
              Instruction('F', 'E')]

def parse_input():
    for line in read_input(7):
        splits = line.split()
        prereq = splits[1]
        action = splits[7]
        yield Instruction(prereq, action)

@attr.s()
class Task:
    action = attr.ib()
    is_done = attr.ib(default=False)
    prereqs = attr.ib(factory=list)

    def __key__(self, other):
        return self.action 

def is_ready(task):
    return all(prereq.is_done for prereq in task.prereqs) and not task.is_done

def find_actions(instructions):
    """ returns all actions based on instructions """
    prereqs = set(instr.prereq for instr in instructions)
    actions = set(instr.action for instr in instructions)
    return prereqs.union(actions)


def create_tasks(instructions):
    tasks = {action: Task(action) for action in find_actions(instructions)}
    for instr in instructions:
        tasks[instr.action].prereqs.append(tasks[instr.prereq])

    return tasks

def is_solved(tasks):
    """ checks whether solution has been found """
    return all(task.is_done for task in tasks.values())

def find_next_task(tasks):
    """ return the task that should be done next """
    ready_tasks = [task for task in tasks.values()
                   if is_ready(task)]
    return min(ready_tasks)
        
def solve_tasks(tasks):
    """ find ordering of tasks that satisfies prereqs """
    def helper(tasks):
        while not is_solved(tasks):
            next_task = find_next_task(tasks)
            next_task.is_done = True
            # return next action
            yield next_task.action

    return list(helper(tasks))

def test_solution(solution, instructions):
    ordering = {action: order for order, action in enumerate(solution)}

    # ensure that each prereq is finished before task is run
    for instr in instructions:
        assert ordering[instr.prereq] < ordering[instr.action]
        

def solve_part_1():
    instructions = list(parse_input())
    tasks = create_tasks(instructions)
    solution = solve_tasks(tasks)
    test_solution(solution, instructions)
    return ''.join(solution)
        
    
