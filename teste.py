import heapq


class Task:
    def __init__(self, period, computation_time, deadline):
        self.period = period
        self.computation_time = computation_time
        self.deadline = deadline
        self.release_time = 0
        self.remaining_time = computation_time

    def __lt__(self, other):
        return self.deadline < other.deadline


def read_tasks(filename):
    tasks = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() != 'P C D':
                period, computation_time, deadline = map(int, line.split())
                task = Task(period, computation_time, deadline)
                tasks.append(task)
    return tasks


def calculate_hyperperiod(tasks):
    periods = [task.period for task in tasks]
    hyperperiod = periods[0]
    for period in periods[1:]:
        hyperperiod = lcm(hyperperiod, period)
    return hyperperiod


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def simulate(tasks):
    hyperperiod = calculate_hyperperiod(tasks)
    timeline = []
    for task in tasks:
        task.release_time = 0
        task.remaining_time = task.computation_time
        heapq.heappush(timeline, (task.release_time + task.period, task))

    current_time = 0
    while current_time < hyperperiod:
        if timeline:
            next_release_time, next_task = heapq.heappop(timeline)
            current_time = max(current_time, next_task.release_time)
            if current_time + next_task.remaining_time <= next_release_time:
                current_time += next_task.remaining_time
                next_task.release_time = current_time
                next_task.remaining_time = 0
                heapq.heappush(timeline, (current_time + next_task.period, next_task))
            else:
                print("O sistema não é escalonável!")
                return False
        else:
            current_time += 1

    return True


def main():
    filename = 'tasks.txt'  # Substitua pelo nome do arquivo com as tarefas
    tasks = read_tasks(filename)
    tasks.sort(key=lambda x: x.deadline)
    if simulate(tasks):
        print("O sistema é escalonável!")
    else:
        print("O sistema não é escalonável!")


if __name__ == '__main__':
    main()
