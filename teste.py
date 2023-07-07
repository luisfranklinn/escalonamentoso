import time



###
#  coisas necessárias para esse EDF 
#  array de cada thread vai possui[periodo, custo, deadline relativa, proximo_periodo, quanto de custo ainda falta, deadline_absoluto]
#  Funcionamento: o "escalonador" ira escolher no inicio de cada tempo, a thread com a deadline mais proxima e
#  tentar executar ela até seu fim ou até o inicio do periodo de outra thread na qual a deadline esteja proxima, 
#  caso a thread termine todo seu custo, a deadline absoluta aumenta a quantidade da relativa e aguarda o inicio do proximo periodo para poder reiniciar o custo.
#  caso nenhum periodo tenha começado, o processador ficara INATIVO  ###

def EDF(threads:list[dict]):
    img = ['','','']
    mmc = MMC(threads) #reinicio de ciclos
    intax = 0.0
    print(f'tempo de reinicio de ciclo: {mmc}')

    tempo_atual = 0
    while(tempo_atual!= mmc):
        print(f'tempo atual:{tempo_atual}')
        thread = encontrar_thread(threads)
        if(thread!=None):
            if(thread['deadline_absoluta']<tempo_atual):
                print(f'Tarefa{thread["nome"]} passou da deadline')
                break
            else:
                executar(thread)
                if(thread["nome"] == 1):
                    img[0]+=("◼ ")
                    img[1]+=("◻ ")
                    img[2]+=("◻ ")

                elif(thread["nome"] == 2):
                    img[0]+=("◻ ")
                    img[1]+=("◼ ")
                    img[2]+=("◻ ")
                else:
                    img[0]+=("◻ ")
                    img[1]+=("◻ ")
                    img[2]+=("◼ ")
            
        else:
            print('Nenhuma Tarefa executando, processador inativo')
            img[0]+=("◻ ")
            img[1]+=("◻ ")
            img[2]+=("◻ ")
            intax+=1
            #time.sleep(0.25)

        tempo_atual +=1


        #checa se é inicio de algum periodo
        atualizar_custos(threads,tempo_atual)

   

    print(f'Taxa de utilização para um ciclo: {(1-(intax/mmc))*100}%')

    f = open("img.txt",'w',encoding='UTF-8')
    for imgs in img: 
       f.write(imgs+'\n')



def MMC(threads:list):
    valores = []
    for thread in threads:
        valores.append(thread['periodo'])


    maxin = max(valores)
    mmc = maxin
    print(valores)

    while( True ):
        if(mmc%valores[0]==0 and mmc%valores[1]==0 and mmc%valores[2]==0):
            break
        mmc+=maxin
        print(mmc)
        #time.sleep(0.25)

    return mmc
    

def encontrar_thread(threads:list[dict]):
    thread_encontrada = None
    for thread in threads:
        if(thread['custo_restante'] !=0 ):
            if(thread_encontrada == None or thread['deadline_absoluta'] < thread_encontrada['deadline_absoluta'] or (thread['deadline_absoluta'] == thread_encontrada['deadline_absoluta'] and thread['custo_restante']<thread['custo'])):    
                 thread_encontrada = thread


    return thread_encontrada

def atualizar_custos(threads:list[dict],tempo_atual:int):
    for thread in threads:
        if(thread['prox_periodo'] == tempo_atual and thread['custo_restante']==0): 
            thread['custo_restante'] = thread['custo']
            thread['prox_periodo'] += thread['periodo'] 

def executar(thread:dict):
    


    thread['custo_restante'] -= 1
    print(f'executando tarefa {thread["nome"]} custo restante : {thread["custo_restante"]} / {thread["custo"]}')

    if(thread['custo_restante'] == 0):
        thread['deadline_absoluta'] += thread['deadline_relativa']

    #time.sleep(0.25)


""" ----------------------------------------MAIN-----------------------------------------------------"""



a = open(r'C:\Users\lavf0\OneDrive\Área de Trabalho\escalonamentoso\testes\sistema5.txt','r')
modes = a.readline().strip('\n').split('\t')
threads = []
i = 1 
for line in a:
    threads.append([i]+line.strip('\n').split('\t'))
    i+=1
    
print(threads,modes)

in_dic = []
for thread in threads:
    label = {
        'nome':int(thread[0]),
        'periodo':int(thread[1]),
        'custo':int(thread[2]),
        'deadline_relativa':int(thread[3]),
        'prox_periodo':int(thread[1]),
        'custo_restante':int(thread[2]),
        'deadline_absoluta':int(thread[3])
    }
    in_dic.append(label)


taxa = 0.0
escalona = True
print(in_dic)
for tarefa in in_dic:
    taxa += (tarefa['custo']/tarefa['periodo'])

print(f'a taxa de utilização: {taxa}')
if(taxa<=1):
    print('Sistema é escalonavel')
else:
    print('Sistema não é escalonavel')

input()

EDF(in_dic)
a.close()