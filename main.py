from function import *
won=[]
table=[]
deck= card_shuffle(basedeck())
p=card_deal(deck)
p[0]=card_sort(p[0])
p[1]=card_sort(p[1])
p[2]=card_sort(p[2])
p[3]=card_sort(p[3])
fst =linearSearch(p,'03c')
p1 = fst[0]
table=['03c']
i=p1+1
if i>3:
    i=0
p[i] = list(set(p[i])-set(table))
surender=[]
tsurender=0
while len(won)<3:
    if tsurender>=3:
        i=linearSearch1d(surender,0)
        table=[0]
    surender=[0,0,0,0]
    tsurender=0
    while(tsurender < 3):
        if surender[i] != 1 or len(p[i])==0:
            print(f'\nplayer1: {len(p[0])} player2: {len(p[1])} player3: {len(p[2])} player4: {len(p[3])}')
            print(f'table:{table}')
            print(f'player{i+1}')
            print(card_sort(p[i]))
            sur = input("Surender[y/n]: ")
            if sur == 'y':
                surender[i]=1
                if i<3:
                    i+=1
                else:
                    i=0
                tsurender = sum(surender)
                continue
            elif sur == 'n':
                pass
            l=True
            s=0
            while l==True:
                select = [item for item in input("Enter \ the list items : ").split()]
                if len(select)== 0:
                    print('tryagain')
                    continue
                elif select[0][:2] == select[len(select)-2][:2] and select[0][:2] == select[len(select)-1][:2] and len(select)<=4 and compair(select,table):
                    l=False
                    continue
                else:
                    s+=1
                    if s>2:
                        sur = input("Surender[y/n]: ")
                        if sur == 'y':
                            surender[i]=1
                            l=False
                            if i<3:
                                i+=1
                            else:
                                i=0
                            tsurender = sum(surender)
                        elif sur == 'n':
                            pass
                    else:
                        print('try again')   
                    continue
            p[i] = list(set(p[i])-set(select))
            table = select
            if len(p[i])==0:
                won.append(i)   
        if i<3:
            i+=1
        else:
            i=0
print(won)
     