#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct
{
    int period;
    int computation_time;
    int deadline;
} task_t;

int gcd(int a, int b)
{
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

int lcm(int a, int b)
{
    return (a * b) / gcd(a, b);
}

bool edf(task_t tasks[], int num_tasks)
{
    int hyperperiod = tasks[0].period;
    for (int i = 1; i < num_tasks; i++)
        hyperperiod = lcm(hyperperiod, tasks[i].period);

    double utilization = 0.0;
    for (int i = 0; i < num_tasks; i++)
        utilization += (double)tasks[i].computation_time / tasks[i].period;

    printf("Taxa de utilizacao igual a %.6f\n", utilization);

    if (utilization > 1)
    {
        printf("O sistema nao eh escalonavel.\n");
        return false;
    }
    else
    {
        printf("O sistema eh escalonavel.\n");
    }

    char timeline[num_tasks][hyperperiod];

    for (int i = 0; i < num_tasks; i++)
    {
        for (int j = 0; j < hyperperiod; j++)
        {
            timeline[i][j] = '-';
        }
    }

    for (int time = 0; time < hyperperiod; time++)
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
            for (int k = 0; k < tasks[selected_task].computation_time; k++)
            {
                timeline[selected_task][time + k] = 'o';
            }
            time += tasks[selected_task].computation_time - 1;
        }
    }

    for (int i = 0; i < num_tasks; i++)
    {
        for (int j = 0; j < hyperperiod; j++)
        {
            printf("%c ", timeline[i][j]);
        }
        printf("\n");
    }

    return true;
}

int main()
{
    FILE *fp;
    fp = fopen("C:/Users/honyc/OneDrive/Documentos/cod/sistema1.txt", "r");
    if (fp == NULL)
    {
        printf("Erro ao abrir o arquivo.\n");
        exit(1);
    }

    task_t tasks[100];
    int n = 0;

    while (fscanf(fp, "%d %d %d", &tasks[n].period, &tasks[n].computation_time, &tasks[n].deadline) != EOF)
    {
        n++;
    }

    fclose(fp);

    edf(tasks, n);

    return 0;
}
