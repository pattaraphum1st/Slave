import math,random
import numpy as np
def card_convert(card):
    ncard=[]
    for i in range(len(card)):
        new = 0
        if card[i][:2] == '0j':
            new = new+11
        elif card[i][:2] == '0q':
            new = new+12
        elif card[i][:2] == '0k':
            new = new+13
        elif card[i][:2] == '0a':
            new = new+14
        elif card[i][:2] == '02':
            new = new+15
        else:
            new = new+float(card[i][:2])
        if card[i][-1:] == 'c':
            new = new+0.1
        elif card[i][-1:] == 'd':
            new = new+0.2
        elif card[i][-1:] == 'h':
            new = new+0.3
        elif card[i][-1:] == 's':
            new = new+0.4
        ncard.append(new)
    return ncard

def card_rconvert(card):
    ncard = []
    for i in range(len(card)):
        if int(card[i]) == 10:
            new='10'
        else:
            new='0'
        if int(card[i]) == 11:
            new = new+'j'
        elif int(card[i]) == 12:
            new = new+'q'
        elif int(card[i]) == 13:
            new = new+'k'
        elif int(card[i]) == 14:
            new = new+'a'
        elif int(card[i]) == 15:
            new = new+'2'
        elif int(card[i]) == 10:
            pass
        else:
            new = new + str(int(card[i]))
        if round(card[i]-math.floor(card[i]),1) == 0.1:
            new = new+'c'
        elif round(card[i]-math.floor(card[i]),1) == 0.2:
            new = new+'d'
        elif round(card[i]-math.floor(card[i]),1) == 0.3:
            new = new+'h'
        elif round(card[i]-math.floor(card[i]),1) == 0.4:
            new = new+'s'
        ncard.append(new)
    return ncard

def card_sum(arr):
    sum = 1
    for i in arr:
        sum = i*sum*3
    return sum

def sum(arr):
    sum = 0
    for i in arr:
        sum = sum + i
    return(sum)

def compair(select,table):
    if len(select)%2 != len(table)%2:
        return False
    vselect = card_convert(select)
    vtable = card_convert(table)
    tvselect = card_sum(vselect)
    tvtable = card_sum(vtable)
    if tvselect > tvtable:
        return True
    else:
        return False
    
def quick_sort(arr):
  if len(arr) < 2:
    return arr
  else:
    pivot = arr[0]
    less = [i for i in arr[1:] if i <= pivot]
    greater = [i for i in arr[1:] if i > pivot]
    return quick_sort(less) + [pivot] + quick_sort(greater)

def card_sort(card):
    vcard=card_convert(card)
    svcard=quick_sort(vcard)
    card=card_rconvert(svcard)
    return card

def card_shuffle(card):
    newcard = card
    random.shuffle(newcard)
    return newcard

def linearSearch(arr, target):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if (arr[i][j] == target):
                return [i, j]
    return [-1, -1]

def linearSearch1d(arr, target):
    for i in range(len(arr)):
        if (arr[i] == target):
            return i
    return -1

def card_deal(deck):
    for i in range(math.floor(len(deck)/4)):
        p[0].append(deck[0])
        deck.pop(0)
        p[1].append(deck[0])
        deck.pop(0)
        p[2].append(deck[0])
        deck.pop(0)
        p[3].append(deck[0])
        deck.pop(0)
    return p

def basedeck():
    basedeck=['03c','03d','03h','03s','04c','04d','04h','04s','05c','05d','05h','05s','06c','06d','06h','06s'
      ,'07c','07d','07h','07s','08c','08d','08h','08s','09c','09d','09h','09s','10c','10d','10h','10s'
      ,'0jc','0jd','0jh','0js','0qc','0qd','0qh','0qs','0kc','0kd','0kh','0ks','0ac','0ad','0ah','0as'
      ,'02c','02d','02h','02s']
    return basedeck

p=[[],[],[],[]]











