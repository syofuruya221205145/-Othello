import tkinter

FS=("Times New Roman",30)
FL=("Times New Roma",100)

BLACK=1
WHITE=2

mx=0
my=0
proc=0
turn=0
msg=""
space=0
iro=[0]*2
who=["1P","2P"]
msg = "先手、後手を選んでください"
board=[
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,2,1,0,0,0],
    [0,0,0,1,2,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]


def click(e):  #クリックした位置を返す関数
    global mx,my
    mx=int(e.x/80)
    my=int(e.y/80)
    if mx>7:mx=7
    if my>7:my=7
    
#描画
def banmen():
    cvs.delete("all")
    cvs.create_text(320,680,text=msg,fill="black") #下のコメント部分
    for y in range(8):
        for x in range(8):
            X=x*80
            Y=y*80
            cvs.create_rectangle(X,Y,X+80,Y+80,outline="black") #マス目を分ける線
            if board[y][x]==BLACK:
                cvs.create_oval(X+10,Y+10,X+70,Y+70,fill="black",width=0) #黒石を設置
            if board[y][x]==WHITE:
                cvs.create_oval(X+10,Y+10,X+70,Y+70,fill="white",width=0)#白石を設置
            
    cvs.update()

def initialization():  #盤面初期化する
    global space
    space=60
    for y in range(8):
        for x in range(8):
            board[y][x]=0
    board[3][4]=BLACK
    board[4][3]=BLACK
    board[3][3]=WHITE
    board[4][4]=WHITE

#石を挟むと返す関数
def put(x,y,color):
    board[y][x]=color
    for dy in range(-1,2):
        for dx in range(-1,2):
            k=0
            sx=x  #初期化
            sy=y  #初期化
            while True:
                sx+=dx
                sy+=dy
                #盤面からでる
                if sx>7 or sx<0 or sy>7 or sy<0:
                    break
                #何も置かれていない
                if board[sy][sx]==0:
                    break
                #相手の石があったら
                if board[sy][sx]==3-color:
                    k+=1
                #自分の石
                if board[sy][sx]==color:
                    for i in range(k):
                        sx-=dx
                        sy-=dy
                        board[sy][sx]=color
                    break

#石を置いた時に何個返せるか
def reverse_num(x,y,color):
    if board[y][x]>0:
        return -1
    total=0
    for dy in range(-1,2):
        for dx in range(-1,2):
            k=0
            sx=x  #初期化
            sy=y  #初期化
            while True:
                sx+=dx
                sy+=dy
                if sx>7 or sx<0 or sy>7 or sy<0:
                    break
                if board[sy][sx]==3-color:
                    k+=1
                if board[sy][sx]==0:
                    break
                if board[sy][sx]==color:
                    for i in range(k):
                        total+=k
                    break
    return total

#打てる石があるか調べる
def possible(color):
    for y in range(8):
        for x in range(8):
            if reverse_num(x,y,color)>0:
                return True
    return False

#盤面の石の数を数える(勝利判定で使用)
def number():
    b=0
    w=0
    for y in range(8):
        for x in range(8):
            if board[y][x]==BLACK:b+=1
            if board[y][x]==WHITE:w+=1
    return b,w



def main():
    global proc,turn,msg,space
    banmen()
    if proc==0:
        cvs.create_text(320,200,text="リバーシ",fill="green",font=FL)
        cvs.create_text(160,440,text="1P",fill="green",font=FS)
        cvs.create_text(320,440,text="←先手(黒)→",fill="green",font=FS)
        cvs.create_text(480,440,text="2P",fill="green",font=FS)
        if(mx==1 or mx==2)and my==5:
            initialization()
            iro[0]=BLACK
            iro[1]=WHITE
            turn=0
            proc=1
        if(mx==5 or mx==6)and my==5:
            initialization()
            iro[0]=WHITE
            iro[1]=BLACK
            turn=1
            proc=1
    elif proc==1:
        msg="1Pの番です"
        
        if turn==1:
            msg="2Pの番です"
        proc=2
    elif proc==2:
        if turn==0:     #1P
            if reverse_num(mx,my,iro[turn])>0:
                put(mx,my,iro[turn])
                space-=1
                proc=3
        else:           #2P
            if reverse_num(mx,my,iro[turn])>0:
                put(mx,my,iro[turn])
                space-=1
                proc=3
    elif proc==3:       #打つ番交代
        msg=""
        turn=1-turn
        proc=4
    
    elif proc==4:#打てるますがあるか
        if space==0:
            proc=5
        elif possible(BLACK)==False and possible(WHITE)==False:
            msg="どちらも打てないので終了"
            proc=5
        elif  possible(iro[turn])==False:
            msg="あなたは打てないのでパス"
            proc=3
        else:
            proc=1
    elif proc==5:#勝利判定
        b,w=number()
        result_text = ""
        msg="黒{},白{}で".format(b,w)
        if b>w :
            msg = ("黒{},白{}で黒の勝ち!!".format(b,w))
        elif w>b:
            msg = ("黒{},白{}で白の勝ち!!".format(b,w))
        else:
            msg = ("黒{},白{}で引き分け".format(b,w))
        proc = 0

    root.after(200,main)
root=tkinter.Tk()
root.title("リバーシ")
root.resizable(False,False)
root.bind("<Button>",click)
cvs=tkinter.Canvas(width=640,height=710,bg="light blue")
cvs.pack()
root.after(200,main)
root.mainloop()