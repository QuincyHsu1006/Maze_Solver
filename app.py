import base64
import numpy as np
import random
import cv2
import eel


@eel.expose
def return_image(urL):
    changed_img = data_url_to_image(urL)
    Solve(changed_img)
    


#將base64轉換為圖片
def data_url_to_image(urL):      
    encoded_data = urL.split(',')[1]
    img = base64.b64decode(encoded_data)
    npimg = np.frombuffer(img,np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    return img


#將圖片轉換為base64
def image_to_base64(img):
    b64_str = cv2.imencode('.png',img)[1].tobytes()
    blob = base64.b64encode(b64_str)
    blob = blob.decode('utf-8')
    return blob


row = 0
col = 0


#開始尋找解答
def Solve(img):
    global row,col
    if (img.shape[0]-2)%16 != 0 or (img.shape[1]-2)%16 != 0:
        eel.Find_error()()
        return

    row = (img.shape[0]-2)//16
    col = (img.shape[1]-2)//16  
    #print(row,col)
    
    Maze = np.zeros((row,col,5))
    Maze,entrance,exit = Build_maze_by_image(img)
    Find_route(img,Maze,entrance,exit)


#用上傳的圖片建立迷宮，找到入口、出口
def Build_maze_by_image(img):
    Maze = np.zeros((row,col,5))
    entrance = 0
    exit = 0

    for i in range(0,row):
        for j in range(0,col):
            
            if any(img[i*16+1 , j*16+2]):   #up
                Maze[i][j][0] = 1

            if any(img[i*16+2 , j*16+1]):   #left
                Maze[i][j][1] = 1

            if any(img[i*16+16 , j*16+15]):  #down
                Maze[i][j][2] = 1

            if any(img[i*16+15 , j*16+16]):  #right
                Maze[i][j][3] = 1

    for i in range(0,col):
        if Maze[0][i][0] == 1:
            entrance = i

    for i in range (0,col):
        if Maze[row-1][i][2] == 1:
            exit = i

    return Maze,entrance,exit


#用dfs建立隨機迷宮，找到入口、出口
@eel.expose
def Build_maze_by_random(r,c):
    global row,col
    row = r
    col = c

    Maze = np.zeros((r,c,5))
    entrance = random.randint(c//2-2, c//2+1)
    exit = random.randint(c//2-2, c//2+1)

    nr = 0
    nc = entrance
    visited = [(nr,nc)]

    while visited:
        Maze[nr][nc][4] = 1
        unvisit = []

        if nr > 0 and Maze[nr-1][nc][4] == 0:
            unvisit.append("up")

        if nc > 0 and Maze[nr][nc-1][4] == 0:
            unvisit.append("left")

        if nr < row-1 and Maze[nr+1][nc][4] == 0:
            unvisit.append("down")

        if nc < col-1 and Maze[nr][nc+1][4] == 0:
            unvisit.append("right")


        if len(unvisit):
            visited.append([nr,nc])
            dir = random.choice(unvisit)

            if dir == "up":
                Maze[nr][nc][0] = 1
                nr-=1
                Maze[nr][nc][2] = 1

            if dir == "left":
                Maze[nr][nc][1] = 1
                nc-=1
                Maze[nr][nc][3] = 1

            if dir == "down":
                Maze[nr][nc][2] = 1
                nr+=1
                Maze[nr][nc][0] = 1
            
            if dir == "right":
                Maze[nr][nc][3] = 1
                nc+=1
                Maze[nr][nc][1] = 1
        
        else:
            nr,nc = visited.pop()

    Maze[0][entrance][0] = 1
    Maze[r-1][exit][2] = 1

    img = np.zeros((r*16+2, c*16+2, 3), dtype='uint8')
    img.fill(255)

    cv2.rectangle(img, (c*16,0), (c*16+1,r*16+1), (0,0,0), -1)
    cv2.rectangle(img, (0,r*16), (c*16+1,r*16+1), (0,0,0), -1)
    cv2.rectangle(img, (exit*16+2,r*16), (exit*16+15,r*16+1), (255,255,255), -1)

    for i in range(r):
        for j in range(c):
            cv2.rectangle(img, (j*16,i*16), (j*16+1,i*16+1),(0,0,0),-1)

            if Maze[i][j][0] == 0:
                cv2.rectangle(img, (j*16+2,i*16), (j*16+15,i*16+1),(0,0,0),-1)

            if Maze[i][j][1] == 0:
                cv2.rectangle(img, (j*16,i*16+2), (j*16+1,i*16+15),(0,0,0),-1)

    blob = image_to_base64(img)
    Find_route(img,Maze,entrance,exit)
    return blob


#尋找路徑
def Find_route(img,Maze,entrance,exit):
    Path = np.zeros((row,col,2))
    Visited = np.zeros((row,col))
    Visited[0][entrance] = 1

    def dfs(r,c):

        if r == row-1 and c == exit:    #終點
            Show_path(img,Path,exit,entrance) 
            return
        
        if r-1 >= 0 and Maze[r][c][0] == 1 and Visited[r-1][c] == 0:  #up
            Path[r-1][c][0] = r
            Path[r-1][c][1] = c

            Visited[r-1][c] = 1
            dfs(r-1,c)
            Visited[r-1][c] = 0

        if c-1 >= 0 and Maze[r][c][1] == 1 and Visited[r][c-1] == 0:  #left
            Path[r][c-1][0] = r
            Path[r][c-1][1] = c
            
            Visited[r][c-1] = 1
            dfs(r,c-1)
            Visited[r][c-1] = 0

        if r+1 < row and Maze[r][c][2] == 1 and Visited[r+1][c] == 0:  #down
            Path[r+1][c][0] = r
            Path[r+1][c][1] = c
           
            Visited[r+1][c] = 1
            dfs(r+1,c)
            Visited[r+1][c] = 0

        if c+1 < col and Maze[r][c][3] == 1 and Visited[r][c+1] == 0:  #right
            Path[r][c+1][0] = r
            Path[r][c+1][1] = c
            
            Visited[r][c+1] = 1
            dfs(r,c+1)
            Visited[r][c+1] = 0

    dfs(0,entrance)


#顯示路徑
def Show_path(img,Path,exit,entrance):
    nr = (row-1)
    nc = exit
    cv2.rectangle(img, (nc*16+8,nr*16+8), (nc*16+9,nr*16+17), (0,0,255), -1)    #exit
    cv2.rectangle(img, (entrance*16+8,8), (entrance*16+9,0), (0,0,255), -1)     #entrance
    
    while nr != 0 or nc != entrance:
        #print(nr,nc)
        pr = int(Path[nr][nc][0])
        pc = int(Path[nr][nc][1])
        cv2.rectangle(img, (nc*16+8,nr*16+8), (pc*16+9,pr*16+9), (0,0,255), -1)
        cv2.rectangle(img, (pc*16+8,pr*16+8), (pc*16+9,pr*16+9), (0,0,255), -1)
        
        nr = pr
        nc = pc
    
    blob = image_to_base64(img)
    eel.setImage(blob)()


eel.init("web")
eel.start("main.html",geometry={"size":(400,300)},mode="chrome-app")

