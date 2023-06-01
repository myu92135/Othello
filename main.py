from PIL import Image, ImageTk
import tkinter as tk
from ocero import Ocero
import numpy as np
import random
class Game(tk.Frame):
    def __init__(self, player1='human', player2='randomai', master=tk.Tk()):
        """オセロゲームのクラス。
        player1, player2引数にプレイヤーの種類を指定する。デフォルトでは1がhuman, 2がrandomai
        【種類】human:人間, randomai:ランダムに置くAI"""

        super().__init__(master)
       
        self.pack()

        master.geometry('400x600')        #ウィンドウの作成

        self.img_dict = self.import_Images('./Images')#画像の読み込み
        
        self.init_board()                #ボードの初期化、描画

        self.update()                    #画面を更新する
        
        self.play_game(whitemode=player1, blackmode=player2)                 #ゲーム実行処理(ゲームが終わるまでループ)

        self.show_info(nowstone=0)       #ゲーム終了処理(勝敗の表示)

        

    def init_board(self):
        
        '''ゲームの初期設定'''
        self.canvas = tk.Canvas(self.master, width=400, height=600)   #canvasを作成
        self.canvas.place(x=0, y=0)                                   #canvasの左上を0, 0に置く
        self.pos_tags = [[(i,j) for i in range(8)] for j in range(8)] #盤面の座標名
        self.manager = Ocero()                                        #オセロの盤面を管理するモジュール(石の設置、回転判定、盤面の記憶など)

        #画像の貼り付け
        self.canvas.create_image(0, 0,anchor='nw',image=self.img_dict['black_player_bg'], tag='bp')   #黒のプレイヤー用の情報表示版画像を置く
        self.canvas.create_image(0, 500,anchor='nw', image=self.img_dict['white_player_bg'], tag='wp')#白のプレイヤー用の情報表示盤画像を置く
        self.canvas.create_image(0, 100, anchor='nw', image=self.img_dict['board'], tag='board')      #オセロ盤の画像を置く
        self.update()        #画面を更新

        self.update_board() #盤面の描画を最新にする
        
    def update_board(self):
        '''盤面の描画を最新にする。'''
        ###石を全部消してから描画している(重くなるのを防止するため)
        board = self.manager.getboard() #盤面を取得
        for i in self.pos_tags:         #盤面の全ての座標についてループを回す
            for j in i:
                x, y = j
                try:
                    self.canvas.delete(f'{j}')  #(x, y)座標のタグを持つ石を消す(なければスキップする)
                except:
                    pass
                if board[y, x] == -1:  #現在の座標が黒ならば
                    self.canvas.create_image(25+x*50, 125+y*50, anchor='center', image=self.img_dict['black_stone'], tag=f'{j}') #(x, y)というタグ名でx,yのマスに黒い石を描画
                elif board[y, x]==1:   #現在の座標が白ならば
                    self.canvas.create_image(25+x*50, 125+y*50, anchor='center', image=self.img_dict['white_stone'], tag=f'{j}') #(x, y)というタグ名でx,yのマスに白い石を描画
        self.update() #更新
        
        


    def play_game(self, first='white', whitemode='human', blackmode='randomai'): 
        '''ゲーム中の処理
           first:最初の石を指定。(white/black)
           whitemode:白い石の入力モード
           blackmode:黒い石の入力モード'''
        if first == 'black':   #最初が黒の番だったら
            nowTurnStone = -1  #現在の手番を黒にする
        else:                  #最初が白の番だったら
            nowTurnStone= 1    #現在の手番を白にする
        while True: #ゲーム処理のループ
            self.manager.display()       #盤面を出力する(デバック用)
            self.show_info(nowTurnStone) #現在の盤面をもとに画面を更新する
            nowPlayermode = whitemode if nowTurnStone ==1 else blackmode     #現在のプレイヤーの種類(入力モード)を保存


            if self.manager.isCanSet(nowTurnStone)==[]:    #置ける場所がなかったらもう一方の手番に変更する(パス)
                nowTurnStone*=-1                       
                continue
            
            inp = self.move(nowPlayermode, nowTurnStone)   #現在のプレイヤーの種類に応じて、石の設置位置をタプルで返す
            print(inp)  #入力を表示(デバッグ用)
            x, y = inp  #石の設置位置をアンパック
            
            

            if nowTurnStone == 1:                              #現在が白の手番だったら
                self.manager.set_white(pos=(int(x), int(y)))   #白の石を(x, y)に置いて回転する
            else:                                              #現在が黒の手番だったら
                self.manager.set_black(pos=(int(x), int(y)))   #黒の石を(x, y)に置いて回転する
            
            


            self.update_board()                                #最新の盤面を描画する

            #ゲーム終了判定
            if self.manager.isCanSet(1) ==[] and self.manager.isCanSet(-1)==[]:  #お互いのプレイヤーの置ける位置が無くなったとき
                w = np.count_nonzero(self.manager.board==1)                      #白の石の数を数える
                b = np.count_nonzero(self.manager.board==-1)                     #黒の石の数を数える
                self.wincolor = 'white' if w > b else 'black'                    #勝った色を判定
                if w == b:                                                       #もし石の数が一致していたら引き分け
                    self.wincolor ='draw'
                break                                                            #ループを抜ける

            nowTurnStone*=-1                       #現在の石の色を反対にする (ターン終了)
    

    
    
    def move(self, pmode:str, nowStone:int)->tuple:
        '''石を設置する位置をタプルで返す。
           pmode:プレイヤーの種類
           nowStone:現在の石の色'''
        ###設置する位置は(x, y)のタプルにして返すようにすること########################################

        self.nowCanset = self.manager.isCanSet(nowStone)  #現在石を置ける位置のタプルのリスト
        if pmode=='human':  #プレイヤーが人間だった時
            for x, y in self.nowCanset:
                self.canvas.create_rectangle(22+50*x,100+22+50*y, 28+50*x, 28+100+50*y, fill='yellow', tags='canpos') #現在置ける位置の目印を画面に表す
                self.update()                                                                                         #更新
            
            clickpos = self.playerInput() #プレイヤーの入力(設置可能な場所がクリックされるまで待つ)
            self.canvas.delete('canpos')  #現在置ける位置の目印を消す
            return clickpos               #設置する場所を返す
        
        if pmode=='randomai':              #現在設置できる位置からランダムに設置するAI
            return self.randomai(nowStone) #ランダムな位置返す
        


    
    def randomai(self, nowStone:int):
        '''設置できる位置をランダムに返す'''
        canset = self.manager.isCanSet(nowStone)     #設置可能位置
        return random.choice(canset)                 #設置可能な位置からランダムに選ぶ
    

    def playerInput(self):
        '''人間のクリック位置のマス目を返す'''
        global mousePos       #クリックされた時のマウス位置
        while True: #適切な位置がクリックされるまで繰り返す
            self.canvas.bind("<ButtonPress-1>", ret_clickpos)           # クリックされたときmousePosにクリックしたマスを保存する
            
            if mousePos != (-100, -100) and mousePos in self.nowCanset: # クリックしたマスが初期値ではなく、また設置可能な場所だったとき
                x, y =mousePos             # x, yにクリックしたマスを保存
                mousePos=(-100, -100)      # クリックマスの位置を初期値に戻す
                return (x, y)              # クリックしたマスを返す
            
            self.update()                  #更新
    
    def show_info(self, nowstone):
        '''各々が獲得した石の数、現在がどちらの手番かなどの情報を画面に表示する。
           nowStone:現在がどちらの石の手番か。[(白)1/-1(黒)]
           nowStoneが0のとき、勝敗を表示する'''
            
        #石の個数を数える
        white_count = np.count_nonzero(self.manager.getboard()==1)  #現在白が獲得している石の数
        black_count = np.count_nonzero(self.manager.getboard()==-1) #現在黒が獲得している石の数

        try:
            self.canvas.delete('white_count')  #古い白が獲得している石の数の表示を削除
            self.canvas.delete('black_count')  #古い黒が獲得している石の数の表示を削除
        except:
            pass

        self.canvas.create_text(180, 550, text=str(white_count), tags='white_count') #現在白が獲得している石の数を表示する
        self.canvas.create_text(180, 50, text=str(black_count), tags='black_count')  #現在黒が獲得している石の数を表示する

        
        #現在の手番を表示(終了後は勝った方に表示)
        text_turn = 'こちらのターン' if nowstone!=0 else 'WIN'
        try:
            self.canvas.delete('turn')  #古い現在の手番の表示を削除
        except:
            pass
        if nowstone == -1:                                               #現在の手番が黒だった時
            self.canvas.create_text(230, 50, text=text_turn, tags='turn')#黒の位置に「こちらのターン」と表示する
        elif nowstone == 1:                                              #現在の手番が白だった時
            self.canvas.create_text(230, 550, text=text_turn, tags='turn')#白の位置に「こちらのターン」と表示する
        
        if nowstone==0:                                                        #ゲームが終了していた時
            if self.wincolor=='black':                                         #勝った色が黒だった時
                self.canvas.create_text(230, 50, text=text_turn, tags='turn')  #黒の方にWINと表示
            elif self.wincolor =='white':                                      #勝った色が白だったとき
                self.canvas.create_text(230, 550, text=text_turn, tags='turn') #白の方にWINと表示
        
        self.update() #更新
            



    def import_Images(self, dir):
        '''オセロ用の画像を読み込む
           dir:画像を保存しているディレクトリ'''

        #画像の名前を保存
        files =['black_stone.png',      #黒い石の画像 
                'white_stone.png',      #白い石の嘉造
                'board.png',            #盤面の画像
                'bg.png',               #背景の画像
                'black_player_bg.png',  #黒のプレイヤーの情報表示盤の画像
                'white_player_bg.png'   #白のプレイヤーの情報表示盤の画像
                ]
        sizes = [(45, 45),           #それぞれの画像の大きさ(filesの並びに対応している)
                 (45, 45),
                 (400, 400),
                 (400, 600),
                 (400, 100),
                 (400, 100)]
        pic_dict={}                           #読み込んだPhotoImageを保存する用のdict
        for file, size in zip(files, sizes):  #ファイル名と画像サイズでループを回す
            path = dir + '/' + file           #画像までのパスを作成
            img = Image.open(path)            #パスの画像を取得
            img = img.resize(size)            #画像をそれぞれ指定されている大きさに変更
            pic_dict[file[:-4]] = ImageTk.PhotoImage(img)   #画像ファイル名から拡張子を外したものをキーとしてPhotoImageを保存
        return pic_dict #PhotoImageたちのdictを返す



def ret_clickpos(event):
    '''現在マウスがどのマスをクリックしたか'''
    global mousePos
    cx, cy = event.x, event.y  #クリックされたx, y座標
    for x in range(8):
        for y in range(8):
            if 50*x <= cx <= 50*(x+1) and 100+50*y <= cy <= 100+50*(y+1): #座標からマスの位置を算出
                mousePos = (x, y)
    
    


if __name__=='__main__':
    mousePos = (-100, -100) #現在のマウスの位置
    game = Game() 
    game.mainloop()