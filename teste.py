import time

import matplotlib.pyplot as plt


def EDF(threads):
    img = []
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
                img.append(thread['nome'])
        else:
            print('Nenhuma tarefa executando, processador inativo')
            img.append(0)
            intax += 1

        tempo_atual += 1
        atualizar_custos(threads, tempo_atual)

    print(f'Taxa de utilização para um ciclo: {(1 - (intax / mmc)) * 100}%')

    plt.plot(img)
    plt.xlabel('Tempo')
    plt.ylabel('Tarefa')
    plt.title('Escalonamento EDF')
    plt.show()

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


filename = r'C:\Users\lavf0\OneDrive\Área de Trabalho\escalonamentoso\testes\sistema1.txt'

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

input()

EDF(in_dic)
