import time

import matplotlib.pyplot as plt


def EDF(threads):
    img = [[], [], []]
    mmc = MMC(threads)
    intax = 0.0
    print(f'Tempo de reinício de ciclo: {mmc}')

    tempo_atual = 0
    while tempo_atual != mmc:
        print(f'Tempo atual: {tempo_atual}')
        thread = encontrar_thread(threads)
        if thread is not None:
            if thread['deadline_absoluta'] < tempo_atual:
                print(f'Tarefa {thread["nome"]} passou da deadline')
                break
            else:
                executar(thread)
                if thread['nome'] == 1:
                    img[0].append(thread['nome'])
                    img[1].append(None)
                    img[2].append(None)
                elif thread['nome'] == 2:
                    img[0].append(None)
                    img[1].append(thread['nome'])
                    img[2].append(None)
                elif thread['nome'] == 3:
                    img[0].append(None)
                    img[1].append(None)
                    img[2].append(thread['nome'])
        else:
            print('Nenhuma tarefa executando, processador inativo')
            img[0].append(None)
            img[1].append(None)
            img[2].append(None)
            intax += 1

        tempo_atual += 1
        atualizar_custos(threads, tempo_atual)

    taxa_utilizacao = (1 - (intax / mmc)) * 100
    print(f'Taxa de utilização para um ciclo: {taxa_utilizacao}%')

    plot_grafico(img, taxa_utilizacao)


def MMC(threads):
    valores = [thread['periodo'] for thread in threads]
    maxin = max(valores)
    mmc = maxin

    while True:
        if all(mmc % valor == 0 for valor in valores):
            break
        mmc += maxin

    return mmc


def encontrar_thread(threads):
    thread_encontrada = None
    for thread in threads:
        if thread['custo_restante'] != 0:
            if (
                thread_encontrada is None
                or thread['deadline_absoluta'] < thread_encontrada['deadline_absoluta']
                or (
                    thread['deadline_absoluta'] == thread_encontrada['deadline_absoluta']
                    and thread['custo_restante'] < thread['custo']
                )
            ):
                thread_encontrada = thread

    return thread_encontrada


def atualizar_custos(threads, tempo_atual):
    for thread in threads:
        if thread['prox_periodo'] == tempo_atual and thread['custo_restante'] == 0:
            thread['custo_restante'] = thread['custo']
            thread['prox_periodo'] += thread['periodo']


def executar(thread):
    thread['custo_restante'] -= 1
    print(f'Executando tarefa {thread["nome"]}, custo restante: {thread["custo_restante"]} / {thread["custo"]}')

    if thread['custo_restante'] == 0:
        thread['deadline_absoluta'] += thread['deadline_relativa']

    time.sleep(0.25)


def plot_grafico(img, taxa_utilizacao):
    plt.figure(figsize=(10, 6))
    plt.yticks([1, 2, 3], ['T3', 'T2', 'T1'])
    plt.xlabel('Tempo')
    plt.title('Execução das Tarefas\nTaxa de Utilização: {:.2f}%'.format(taxa_utilizacao))

    colors = ['red', 'green', 'blue']
    labels = ['T1', 'T2', 'T3']

    for i in range(len(img[0])):
        for j in range(3):
            if img[j][i] is not None:
                plt.barh(3-j, 1, left=i, color=colors[j], edgecolor='black')
                plt.text(i + 0.5, 3-j, labels[j], color='white', ha='center', va='center')

    plt.ylim(0.5, 3.5)

    for i in range(1, len(img[0])):
        plt.axvline(x=i, color='black', linestyle='--', alpha=0.5)

    plt.show()


filename = r'C:\Users\lavf0\OneDrive\Área de Trabalho\escalonamentoso\testes\sistema6extra.txt'

with open(filename, 'r') as file:
    modes = file.readline().strip().split('\t')
    threads = []
    i = 1
    for line in file:
        threads.append([i] + line.strip().split('\t'))
        i += 1

print(threads, modes)

in_dic = []
for thread in threads:
    label = {
        'nome': int(thread[0]),
        'periodo': int(thread[1]),
        'custo': int(thread[2]),
        'deadline_relativa': int(thread[3]),
        'prox_periodo': int(thread[1]),
        'custo_restante': int(thread[2]),
        'deadline_absoluta': int(thread[3])
    }
    in_dic.append(label)

taxa = sum(tarefa['custo'] / tarefa['periodo'] for tarefa in in_dic)
print(f'A taxa de utilização: {taxa}')
if taxa <= 1:
    print('Sistema é escalonável')
else:
    print('Sistema não é escalonável')

EDF(in_dic)
