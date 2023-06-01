import numpy as np
class Ocero:
    def __init__(self):

        #-1は黒の石。1は白の石。0は何も置かれていない
        self.board = np.array( [[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0,-1, 1, 0, 0, 0],
                                [0, 0, 0, 1,-1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],], dtype=np.int8)

        
    def display(self):
        """現在の盤面を出力"""
        print(self.board)
    
    def getboard(self):
        """現在の盤面を取得"""
        return self.board 
    

    def set_black(self, pos:tuple):
        '''黒色の石を置いて、回転判定を行う。'''
        x, y = pos                                        #設置位置
        afterset = self.turnCheck(pos=(x, y), stone=-1)   #石をx, yに設置し、回転した後の盤面を取得
        if type(afterset) !=bool:
            afterset[y, x]=-1
            self.board = afterset.copy()

        else:
            return False
    
    def set_white(self, pos):
        '''白色の石を置いて回転'''
        x, y = pos
        afterset = self.turnCheck(pos=(x, y), stone=1)
        if type(afterset) != bool:
            afterset[y, x]=1
            self.board = afterset.copy()

        else:
            return False

    def isCanSet(self, stone):
        '''石を設置できる場所のタプルのリストを返す pos:設置場所のタプル stone=1or-1'''
        cansetpos = []
        for x in range(8):
            for y in range(8):
                if self.board[y, x] != 0:
                    continue
                elif self.turnCheck((x, y), stone, isbool=True) !=False:
                    cansetpos.append((x,y))
        return cansetpos

            
    def turnCheck(self, pos, stone, isbool=False):
        '''石を置いたとき回転するかを調べ、回転したときの値を返す。回転がなかったときはFalseを返す'''
        x, y = pos
        now_board = self.board.copy()
        isTurn = False
        turnpoint=[]
        #right, left, top, bottom, topleft, topright, bottomleft, bottomright
        for i in [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            vx, vy = i
            res = self.searchTurn(pos, vx, vy, stone, now_board)
            if type(res) != bool:
                for i in res:
                    turnpoint.append(i)
                isTurn = True
        if isbool:
            return isTurn
        
        for i in turnpoint:
            x, y = i
            now_board[y, x] = stone
        return now_board if isTurn else False
    
    def searchTurn(self, point, vx, vy, stone, board):
        '''vx, vy:探査の方向'''
        #turnCheckの補助 
        sx, sy = point
        turnpoint =[] #回転のタプルのリスト
        if not(0 <= sy+vy <= 7 and 0 <= sx+vx <= 7):
            return False
        
        if board[sy+vy, sx+vx] != stone*-1:
            return False
        y=sy+vy
        x=sx+vx

        while True:
            y+=vy
            x+=vx
            if not(0 <= y <= 7 and 0 <= x <= 7):
                return False
            
            if board[y, x]==0:
                return False



            if board[y, x] == stone:
                sx+=vx
                sy+=vy
                while True:
                    turnpoint.append((sx, sy))
                    sx += vx
                    sy += vy
                    if sx == x and sy == y:
                        return turnpoint
            
            
                        
                    

        
        
if __name__ == '__main__':
    #デバッグ用に作成した。設置不能な位置に石を設置するとおかしくなる。
    game = Ocero()
    game.display()

    while True:
        print(game.isCanSet(1))
        inp = input('白の場所をスペース区切りで入力(x y):')
        x, y = inp.split(' ')

        game.set_white(pos=(int(x), int(y)))
        game.display()

        print(game.isCanSet(-1))
        inp = input('黒の場所をスペース区切りで入力(x y):')
        x, y = inp.split(' ')
        game.set_black(pos=(int(x), int(y)))
        game.display()



        
