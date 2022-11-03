import numpy as np
"""自分の石を1、敵の石を-1として表現している"""
def load_file_mc(path, nowStone):
    with open(path, mode='r', encoding="utf_8") as file:
        #保存してある辞書の呼び出し
        dic = {}
        for f in file:
            k1, v1 = f.split('&')
            k1 =list(map(int, k1.split(',')))
            spv1= [i for i in v1.split(',')]
            d = {}
            for v in spv1:
                k2, v2 = v.split('$')
                
                

                k2 = tuple(map(int, k2.replace('(', '').replace(')', '').replace(' ', '').strip().split('a')))

                v2 = float(v2.strip())

                d[k2] = v2
            dic[tuple(k1)] = d
            
    return dic

def write_file_mc(path, log, nowStone, wincolor):
    r = 0.7 #割引率
    a = 0.1 #学習率

    dic = load_file_mc(path, 1)
    if wincolor == 'black':
        wincolor = -1
    else:
        wincolor = 1

    if wincolor == nowStone:
        score = 1
    elif wincolor == 'draw':
        score = 0
    
    else:
        score = -1

    for turn, j in enumerate(log[::-1]):
        state, pos = j
        state = tuple(state.reshape((1, 64)).tolist()[0])

        try:
            dic[state][pos] = float(dic[state][pos]) * (1-a) + score*a*r**turn
        except KeyError:
            try:
                dic[state][pos] = 0.0
                dic[state][pos] = float(dic[state][pos]) * (1-a) + score*a*r**turn
            except KeyError:
                dic[state] = {pos:0.0}
                dic[state][pos] = float(dic[state][pos]) * (1-a) + score*a*r**turn

    write_text=''
    with open(path, mode='w', encoding='utf-8', newline='\n') as f:
        for k1 in dic:
            write_text=''
            write_text += str(k1).replace('(','').replace(')','')+'&'

            for p in dic[k1]:
                write_text+=str(p).replace(',', 'a')+'$'
                write_text+=str(dic[k1][p])+','

            write_text = write_text[:-1] + '\n'
            f.write(write_text)
        


        
    
if __name__ == '__main__':
    print(load_file_mc('data/mc/sample.txt', 2))
    log = [np.array([[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1],[0, 0, 0, 0, 1, 1, 1, 1]]), (1, 5)],[np.array([[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1],[0, 0, 0, 0, 0, 0, 0, 1]]), (200, 6)]
    write_file_mc('data/mc/sample.txt', log, 1, 'black')