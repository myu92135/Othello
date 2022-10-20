from PIL import Image, ImageTk
import tkinter as tk
from ocero import Ocero
import numpy as np
import random
class Game(tk.Frame):
    def __init__(self, master=tk.Tk()):
        
        super().__init__(master)
       
        self.pack()

        master.geometry('400x600')#ウィンドウの表示

        self.img_dict = self.import_Images('./Images')#画像の読み込み
        
        self.init_board() #ボードの初期化、描画

        self.update()
        
        self.play_game()

        self.show_info(nowstone=0) #ゲーム終了処理(勝敗の表示)

        

    def init_board(self):
        
        '''ゲームの初期設定'''
        self.canvas = tk.Canvas(self.master, width=400, height=600)
        # self.stone_canvases = [[tk.Canvas(self.master, width=50, height=50) for _ in range(8)] for _ in range(8)]
        
        self.canvas.place(x=0, y=0)
        
        
        self.pos_tags = [[(i,j) for i in range(8)] for j in range(8)] #ボードの座標名
        
        self.manager = Ocero()

        #画像の貼り付け
        

        self.canvas.create_image(0, 0,anchor='nw',image=self.img_dict['black_player_bg'], tag='bp')
        self.canvas.create_image(0, 500,anchor='nw', image=self.img_dict['white_player_bg'], tag='wp')
        self.canvas.create_image(0, 100, anchor='nw', image=self.img_dict['board'], tag='board')
        self.update()

        self.update_board()
        
        

    
    def update_board(self):
        '''盤面の更新と表示'''
        board = self.manager.getboard()
        for i in self.pos_tags:
            for j in i:
                x, y = j
                try:
                    self.canvas.delete(f'{j}')
                except:
                    pass
                if board[y, x] == -1:
                    self.canvas.create_image(25+x*50, 125+y*50, anchor='center', image=self.img_dict['black_stone'], tag=f'{j}')
                elif board[y, x]==1:
                    self.canvas.create_image(25+x*50, 125+y*50, anchor='center', image=self.img_dict['white_stone'], tag=f'{j}')
                
                
        self.update()
        
        


    def play_game(self, first='white', whitemode='human', blackmode='randomai'):
        '''ゲーム中の処理'''
        if first == 'black':
            nowTurnStone = -1
        else:
            nowTurnStone= 1
        while True:
            self.manager.display()
            self.show_info(nowTurnStone)#画面情報の更新
            nowPlayermode = whitemode if nowTurnStone ==1 else blackmode


            if self.manager.isCanSet(nowTurnStone)==[]:#パス
                nowTurnStone*=-1
                continue
            
            inp = self.move(nowPlayermode, nowTurnStone)
            print(inp)
            x, y = inp
            
            

            if nowTurnStone == 1:
                self.manager.set_white(pos=(int(x), int(y)))
            else:
                self.manager.set_black(pos=(int(x), int(y)))
            
            


            self.update_board()

            #ゲーム終了判定
            if self.manager.isCanSet(1) ==[] and self.manager.isCanSet(-1)==[]:
                w = np.count_nonzero(self.manager.board==1)
                b = np.count_nonzero(self.manager.board==-1)
                self.wincolor = 'white' if w > b else 'black'
                if w == b:
                    self.wincolor ='draw'
                
                break
            nowTurnStone*=-1
    

    
    
    def move(self, pmode, nowStone):
        '''どこに置くか決定する'''
        self.nowCanset = self.manager.isCanSet(nowStone)
        if pmode=='human':  #人間用
            for x, y in self.nowCanset:
                self.canvas.create_rectangle(22+50*x,100+22+50*y, 28+50*x, 28+100+50*y, fill='yellow', tags='canpos')
                self.update()
            
            clickpos = self.playerInput() #入力まち
            self.canvas.delete('canpos')
            return clickpos
        
        if pmode=='randomai': #ランダムに設置するAI
            return self.randomai(nowStone)
    
    def randomai(self, nowStone):
        canset = self.manager.isCanSet(nowStone)
        return random.choice(canset)

    def playerInput(self):
        global mousePos
        while True:
            self.canvas.bind("<ButtonPress-1>", ret_clickpos)
            
            if mousePos != (-100, -100) and mousePos in self.nowCanset:
                x, y =mousePos
                mousePos=(-100, -100)
                return (x, y)
            self.update()
    
    def show_info(self, nowstone):
        '''画面の情報を表示、更新する。
        ・石の数、どちらのターンか、勝敗'''
            
        #石の個数
        white_count = np.count_nonzero(self.manager.board==1)
        black_count = np.count_nonzero(self.manager.board==-1)
        try:
            self.canvas.delete('white_count')
            self.canvas.delete('black_count')
        except:
            pass
        self.canvas.create_text(180, 550, text=str(white_count), tags='white_count')
        self.canvas.create_text(180, 50, text=str(black_count), tags='black_count')

        
        #どちらのターンか(終了後は勝敗を表示)
        text_turn = 'こちらのターン' if nowstone!=0 else 'WIN'
        try:
            self.canvas.delete('turn')
        except:
            pass

        if nowstone == -1:
            self.canvas.create_text(230, 50, text=text_turn, tags='turn')
        elif nowstone == 1:
            self.canvas.create_text(230, 550, text=text_turn, tags='turn')
        
        if nowstone==0:
            if self.wincolor=='black':
                self.canvas.create_text(230, 50, text=text_turn, tags='turn')
            elif self.wincolor =='white':
                self.canvas.create_text(230, 550, text=text_turn, tags='turn')
        
        self.update()
            



    def import_Images(self, dir):
        '''オセロ用の画像を読み込む'''

        files =['black_stone.png',
                'white_stone.png',
                'board.png',
                'bg.png',
                'black_player_bg.png',
                'white_player_bg.png'
                ]
        sizes = [(45, 45),
                 (45, 45),
                 (400, 400),
                 (400, 600),
                 (400, 100),
                 (400, 100)]
        pic_dict={}
        for file, size in zip(files, sizes):
            path = dir + '/' + file
            img = Image.open(path)
            img = img.resize(size)
            pic_dict[file[:-4]] = ImageTk.PhotoImage(img)
        return pic_dict



def ret_clickpos(event):
    global mousePos
    cx, cy = event.x, event.y
    for x in range(8):
        for y in range(8):
            if 50*x <= cx <= 50*(x+1) and 100+50*y <= cy <= 100+50*(y+1):
                mousePos = (x, y)
    
    


if __name__=='__main__':
    mousePos = (-100, -100)
    game = Game()
    game.mainloop()