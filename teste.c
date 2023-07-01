#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int period;
    int execution_time;
    int deadline;
} Task;

void EDF(Task *tasks, int num_tasks) {
    int current_time = 0;
    int i;

    while (num_tasks > 0) {
        // Encontre a tarefa com o prazo mais curto
        int next_task_index = -1;
        int min_deadline = INT_MAX;

        for (i = 0; i < num_tasks; i++) {
            if (tasks[i].deadline < min_deadline) {
                next_task_index = i;
                min_deadline = tasks[i].deadline;
            }
        }

        // Verifique se a próxima tarefa está pronta para ser executada
        if (tasks[next_task_index].period > current_time) {
            current_time = tasks[next_task_index].period;
        }

        // Execute a tarefa até o seu prazo de conclusão
        int execute_time = (tasks[next_task_index].execution_time < (tasks[next_task_index].deadline - current_time))
            ? tasks[next_task_index].execution_time
            : (tasks[next_task_index].deadline - current_time);

        current_time += execute_time;
        tasks[next_task_index].execution_time -= execute_time;

        // Verifique se a tarefa foi concluída ou não
        if (tasks[next_task_index].execution_time <= 0) {
            tasks[next_task_index] = tasks[num_tasks - 1];
            num_tasks--;
        }
    }
}

int main() {
    FILE *file = fopen("sistema1.txt", "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo.\n");
        return 1;
    }

    int num_tasks;
    fscanf(file, "%d", &num_tasks);

    Task *tasks = (Task *) malloc(num_tasks * sizeof(Task));
    if (tasks == NULL) {
        printf("Erro ao alocar memória.\n");
        fclose(file);
        return 1;
    }

    int i;
    for (i = 0; i < num_tasks; i++) {
        fscanf(file, "%d %d %d", &tasks[i].period, &tasks[i].execution_time, &tasks[i].deadline);
    }

    fclose(file);

    EDF(tasks, num_tasks);

    printf("Tarefas concluídas:\n");
    for (i = 0; i < num_tasks; i++) {
        printf("Tarefa %d: Periodo = %d, Tempo de execucao = %d, Deadline = %d\n",
               i+1, tasks[i].period, tasks[i].execution_time, tasks[i].deadline);
    }

    free(tasks);

    return 0;
}
