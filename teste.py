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
    periods = []
    computation_times = []
    deadlines = []
    tasks = []
    with open(filename, 'r') as file:
        lista = file.readlines()
   
    for i in range(1,len(lista)):
        linha = lista[i].split()
        periods.append(linha[0])
        computation_times.append(linha[1])
        deadlines.append(linha[2])
        task = Task(linha[0], linha[1], linha[2])
        tasks.append(task)
    
    print(periods)
    print(computation_times)
    print(deadlines)
"""
def read_tasks(filename):
    tasks = []
    for i in range(len(lista)):
        linha = lista[i].split()
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines = lines[1:].strip()
        print(lines)
        
        for line in lines:
            #print(line[0])
            #if line.strip() != 'P C D':  # Adicione esta verificação para ignorar a linha de cabeçalho
            period, computation_time, deadline = map(int, line.split())
            task = Task(period, computation_time, deadline)
            tasks.append(task)
    return tasks
"""

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
    filename = r'C:\Users\lavf0\OneDrive\Área de Trabalho\escalonamentoso\testes\sistema1.txt'  # Substitua pelo nome do arquivo com as tarefas
    tasks = read_tasks(filename)
    tasks.sort(key=lambda x: x.deadline)
    if simulate(tasks):
        print("O sistema é escalonável!")
    else:
        print("O sistema não é escalonável!")


if __name__ == '__main__':
    main()
