#include <stdio.h>
#include <stdlib.h>

#define MAX_TASKS 10

typedef struct
{
    int period;
    int computation_time;
    int deadline;
} task_t;

int read_tasks(task_t tasks[])
{
    FILE *file;
    file = fopen("C:/Users/Davi & Larissa/Documents/TRABALHO SO/escalonamentoso/sistema1.txt", "r");

    if (file == NULL)
    {
        printf("Erro ao abrir o arquivo.\n");
        exit(1);
    }
    char discard[100];
    fgets(discard, sizeof(discard), file);

    int num_tasks = 0;
    while (fscanf(file, "%d %d %d", &tasks[num_tasks].period, &tasks[num_tasks].computation_time, &tasks[num_tasks].deadline) == 3)
    {
        num_tasks++;
        if (num_tasks >= MAX_TASKS)
        {
            printf("Erro: número máximo de tarefas excedido.\n");
            exit(1);
        }
    }

    fclose(file);
    return num_tasks;
}

int gcd(int a, int b)
{
    if (b == 0)
        return a;
    else
        return gcd(b, a % b);
}

int lcm(int a, int b)
{
    return (a * b) / gcd(a, b);
}

int edf(task_t tasks[], int num_tasks)
{
    int hyperperiod = tasks[0].period;
    for (int i = 1; i < num_tasks; i++)
        hyperperiod = lcm(hyperperiod, tasks[i].period);

    int time = 0;
    while (time < hyperperiod)
    {
        int earliest_deadline = hyperperiod;
        int selected_task = -1;
        for (int i = 0; i < num_tasks; i++)
        {
            if (time % tasks[i].period == 0 && tasks[i].deadline < earliest_deadline)
            {
                earliest_deadline = tasks[i].deadline;
                selected_task = i;
            }
        }

        if (selected_task != -1)
        {
            time += tasks[selected_task].computation_time;
        }
        else
        {
            time++;
        }
    }
    printf("\n");

    double utilization = 0.0;
    for (int i = 0; i < num_tasks; i++)
        utilization += (double)tasks[i].computation_time / tasks[i].period;

    printf("Taxa de utilizacao igual a %.6f\n", utilization);

    for (int i = 0; i < num_tasks; i++)
    {
        for (int j = 0; j < hyperperiod; j++)
        {
            if (j % tasks[i].period == 0)
                printf("o ");
            else
                printf("- ");
        }
        printf("\n");
    }

    return utilization <= 1.0;
}

int main()
{
    task_t tasks[MAX_TASKS];
    int num_tasks = read_tasks(tasks);

    int is_schedulable = edf(tasks, num_tasks);

    if (is_schedulable)
        printf("O sistema e escalonavel.\n");
    else
        printf("O sistema nao e escalonavel.\n");

    return 0;
}
