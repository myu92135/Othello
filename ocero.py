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
        afterset = self.turnCheck(pos=(x, y), stone=-1)   #石をx, yに設置したときに回転した後の盤面を取得
        afterset[y, x]=-1                                 #posに石を設置する
        self.board = afterset.copy()                      #盤面を新しいものに更新する
    
    def set_white(self, pos):
        '''白色の石を置いて回転'''
        x, y = pos                                        #設置位置
        afterset = self.turnCheck(pos=(x, y), stone=1)    #石をx, yに設置したときに回転した後の盤面を取得
        afterset[y, x]=1                                  #posに石を設置する
        self.board = afterset.copy()                      #盤面を新しいものに更新する

    def isCanSet(self, stone):
        '''石を設置できる場所のタプルのリストを返す pos:設置場所のタプル stone:現在の石の種類、1/-1'''
        cansetpos = []                                                      #設置が可能な位置のタプルを入れるリスト
        for x in range(8):                                                  #マスの個数だけ繰り返す
            for y in range(8):
                if self.board[y, x] != 0:                                   #判定しようとしたマスに既に石が置かれていた場合
                    continue                                                #次のループに移動する

                elif self.turnCheck((x, y), stone, isbool=True) !=False:    #x, yに石を置いたとき石の回転が発生するか調べる
                    cansetpos.append((x,y))                                 #発生したら設置が可能な位置に追加する
        return cansetpos   #設置が可能な位置のリストを返す

            
    def turnCheck(self, pos:tuple, stone:int, isbool=False):
        '''石を置いたとき回転するかを調べ、回転したときの盤面を返す。isboolがTrueだったら石が回転するかどうかのみを調べてboolを返す。
           pos:石を置く位置のタプル(x, y)
           stone:現在位の石の色(1/-1)'''
        x, y = pos
        now_board = self.board.copy() #現在の盤面のコピーを取得
        isTurn = False                #回転するか否か
        turnpoint=[]                  #石が回転する座標のリスト

        #石を置く場所から8方向に対してそれぞれ回転するかどうかを調べる
        #right, left, top, bottom, topleft, topright, bottomleft, bottomright
        for i in [(1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]: 
            vx, vy = i  

            try: #iの方向に回転が発生する場合
                res = self.searchTurn(pos, vx, vy, stone, now_board) #vx vyずつ値を増やしながらそちらの方向に回転するかを調べる(しない場合例外発生)

                if isbool: #boolを返してほしいとき
                        return True #回転が発生することを知らせる
                for i in res:            #回転する位置を回す
                    turnpoint.append(i)  #回転位置をturnpointに追加する
                    
                    
            except Exception:#回転が発生しない場合
                continue     #次の方向を調べる

        if isbool:           #boolを返してほしいとき
             return False   #回転しなかったことを返す
        
        for i in turnpoint:         #全ての回転する位置に石を置きなおす
            x, y = i
            now_board[y, x] = stone #回転位置x, yに新しい石をセット
        return now_board            #回転した後の盤面を返す
    
    #turnCheckの補助として使う
    def searchTurn(self, point, vx, vy, stone, board):
        '''指定された位置(point)からvx, vy方向にマスを移動しながら石が回転するかどうかを調べる。
           回転した場合回転する位置のタプルのリストを返す。
           回転しなかったら例外を発生させる。
           point:探索の初期位置
           vx, vy:探索の方向
           stone:現在の石の色
           board:調べる盤面'''
        
        sx, sy = point  #sx, syに初期値を設定
        turnpoint =[]   #回転のタプルのリスト
        if not(0 <= sy+vy <= 7 and 0 <= sx+vx <= 7): #次の位置が盤面の範囲外になるなら例外を発生(探索終了)
            raise Exception
        
        if board[sy+vy, sx+vx] != stone*-1:          #次の位置にあるのが相手側の石ではなかったら例外を発生(探索終了)
            raise Exception
        
        y=sy+vy #初期値の次のx座標を設定
        x=sx+vx #初期値の次のy座標を設定

        while True: #調べる位置をvx, vy方向にずらしながら探索を繰り返す。

            #探索位置をvx, vyだけ更新
            y+=vy 
            x+=vx

            if not(0 <= y <= 7 and 0 <= x <= 7): #探索位置が盤面の範囲外だったら例外を発生(探索終了)
                raise Exception
            
            elif board[y, x]==0:                   #x, yに何も置かれていなかったら例外を発生(探索終了)
                raise Exception
            

            if board[y, x] == stone:               #探索位置にある石が自分の石と同じだったら
                # 初期位置から現在の探索地点までの座標をturnpointに追加する
                while True:
                    turnpoint.append((sx, sy))  
                    sx += vx
                    sy += vy
                    if sx == x and sy == y: #sx, xyが現在の探索地点と一致したら終了する
                        return turnpoint