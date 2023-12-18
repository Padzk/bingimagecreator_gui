from tkinter import *
from tkinter.filedialog import *
from BingImageCreator import *
from multiprocessing import *
from datetime import datetime
from time import *
from random import randint
from PIL import Image, ImageTk

icon_size = 128       #tamaño en pixeles de cada icono en la cuadrilla
grid_width = 1        #tamaño de iconos por ancho y alto de la cuadrilla
thumb_size = 384    #tamaño en pixeles de la vista previa 
cookie_count = 4      #numero de campos de cookies
canvas_size = icon_size*2   #tamaño en pixeles del lienzo de los iconos

def getRandomColor():return "#"+''.join(hex(randint(2,4))[2:] for x in range(3))
pal = ["#111","#222","#444","#eee","#f46","#f88","#fee"]
tk = Tk()
tk.geometry("640x480")
tk["bg"],tk["padx"],tk["pady"] = pal[1],2,2

var_log = StringVar()
var_log.set("imagine this is some informative text or something")
var_promt = StringVar()
var_attempts = IntVar()
var_attempts.set(1)
var_thumbindex = IntVar()
var_currentimgname = StringVar()
var_currentimgname.set("asdfghjkl.jpeg")
#0 = U_ Cookie, 1 = use_cookie, 2 = gen_count, 3 = img_downloads, 4 = errors
vars_cookies = [[StringVar(),BooleanVar(),IntVar(),IntVar(),IntVar()] for x in range(cookie_count)]
vars_cookies[0][1].set(True)

photoimages_list = []
thumbnails = {}
thumbnails[icon_size] = []
thumbnails[thumb_size] = []
previews = []
max_tilecount = 2**2
def dothis(cookie):
    global icon_size,grid_width,max_tilecount
    cook, use, gen_count, dl_img_count, error_count = cookie
    dir = var_directory.get()
    cok = cook.get()
    imggen= ImageGen(auth_cookie=cok,auth_cookie_SRCHHPGUSR=cok)
    for i in range(var_attempts.get()): 
        lis = False
        promttt = var_promt.get()
        try: 
            lis = imggen.get_images(promttt)
            gen_count.set(gen_count.get()+1)
        except Exception as error: 
            error_count.set(error_count.get()+1)
            var_log.set("Error "+str(error_count.get())+": "+str(error))
            status_board["fg"] = "#f66"
            print(error)
        if lis: 
            dt_string = datetime.now().strftime("%Y%m%d%H%M%S") 
            imggen.save_images(lis,dir,dt_string)
            for i in range(9):
                ti = var_thumbindex.get()
                fil = dt_string+"_"+str(i)+".jpeg"
                file = dir+fil
                max_tilecount = grid_width**2
                if ti>max_tilecount: 
                    grid_width += 1
                    max_tilecount = grid_width**2
                    icon_size = int(canvas_size/grid_width)
                    thumbnails[icon_size] = []
                    images_canvas.delete("all")
                    for k in range(len(photoimages_list)):     
                        thumbnails[icon_size].append(ImageTk.PhotoImage(photoimages_list[k][1].resize((icon_size,icon_size))))
                        images_canvas.create_image(k%grid_width,k//grid_width,anchor=NW ,image=thumbnails[icon_size][k])
                    images_canvas.scale(ALL,0,0,icon_size,icon_size)

                pic = None
                try: 
                    pic = Image.open(file)
                    dl_img_count.set(dl_img_count.get()+1)
                except: print(file+" does not exist!")
                if pic:
                    xx,yy = icon_size*(ti%grid_width),icon_size*(ti//grid_width)
                    photoimages_list.append((file, pic,fil))
                    thumbnails[icon_size].append(ImageTk.PhotoImage(photoimages_list[ti][1].resize((icon_size,icon_size))))
                    previews.append(ImageTk.PhotoImage(photoimages_list[ti][1].resize((thumb_size,thumb_size))))
                    images_canvas.create_image(xx,yy,anchor=NW ,image=thumbnails[icon_size][ti])
                    thumbnail["image"] = previews[ti]
                    var_thumbindex.set(ti+1)
            tk.update()
def doGenImg():
    var_promt.set(promt_entry.get("1.0","end-1c"))
    available_cookies = [x for x in vars_cookies if x[1].get()]
    starttime = time()
    """pool = Pool()
    pool.map(dothis,available_cookies)
    pool.close()"""
    """processes = []
    for cookie in available_cookies:
        p = Process(target=dothis,args=(cookie,))
        processes.append(p)
        p.start()
    for process in processes:process.join()"""
    for i in available_cookies:dothis(i)
    print('That took {} seconds'.format(time() - starttime))

var_directory = StringVar()
var_directory.set("/home/pawpad/bing_gen/")

#promt area
promt_frame = Frame(tk,bg=pal[1])

promt_selector_frame = Frame(promt_frame,bg=pal[1])
for i in range(4):
    ae = Button(promt_selector_frame,padx=0,pady=0,bd=0,highlightthickness=0,text=str(i+1),font=("default",6),width=3,bg=pal[4],activebackground=pal[5],fg=pal[6],activeforeground=pal[6])
    ae.pack(padx=2,pady=2)
promt_selector_frame.pack(side=LEFT)




promt_entry= Text(promt_frame,height=4,width=76,bd=0,bg=pal[2],fg=pal[3],highlightthickness=0,padx=1,pady=0,font=("default",9), wrap="word",)
promt_start = Button(promt_frame,command=doGenImg,height=1,width=10,bg=pal[4],activebackground=pal[5],relief=FLAT,highlightthickness=0,padx=0,pady=0,text="GENERATE",fg="#fee",bd=2,activeforeground=pal[6])
p = "The quick brown fox jumps over the lazy dog"
promt_entry.insert("1.0",p)
promt_entry.pack(side=LEFT,padx=2,pady=2)
promt_start.pack(anchor=NE,padx=2,pady=2)

batch_timesentry = Entry(promt_frame,textvariable=var_attempts,width=3,bd=0,highlightthickness=0,justify=CENTER,bg=pal[2],fg=pal[3])
batch_label = Label(promt_frame,text="Repeats:",bg=pal[1],fg=pal[3],bd=0,highlightthickness=0,padx=0,pady=0)
batch_label.pack()
batch_timesentry.pack()
promt_frame.pack()

#images area
second_area = Frame(tk,bg="#222")

def printpos(e):
    global icon_size,grid_width
    xx,yy = e.x//icon_size,e.y//icon_size
    ind =   xx+(grid_width*yy)
    try:
        thumbnail["image"] = previews[ind]
        print(photoimages_list[ind][2])
        var_currentimgname.set(photoimages_list[ind][2])
    except: thumbnail["image"] = None

img_canv_and_cookies = Frame(second_area,padx=0,pady=0,highlightthickness=0,bd=0,bg=pal[1])

images_canvas = Canvas(img_canv_and_cookies,height=canvas_size,width=canvas_size,bd=0,highlightthickness=0,bg=pal[2])
images_canvas.bind("<Motion>",printpos)

images_canvas.pack(padx=2,pady=2)

cookies_frame = Frame(img_canv_and_cookies,bg="#222")
def toggle_cookie(x):
    if x[0]["state"] == "normal": 
        x[0].config(state= "disabled")
        vars_cookies[x[1]][1].set(False)
    else:
        x[0].config(state= "normal")
        vars_cookies[x[1]][1].set(True)

cookie_entries = []
for i in range(cookie_count):
    info_pal = ["#6c6","#66f","#f66"]
    for k in range(3):
        count1 = Label(cookies_frame,textvariable=vars_cookies[i][2+k],width=4,bg=info_pal[k],fg="#fff",font=("default",6),bd=0,padx=2,pady=3,highlightthickness=0)
        count1.grid(column=k,row=i,padx=2)

    entry = Entry(cookies_frame,width=24,bd=0,highlightthickness=0,textvariable=vars_cookies[i][0],state=DISABLED if i != 0 else NORMAL,bg=pal[2],fg=pal[3],disabledbackground=pal[0],disabledforeground=pal[2],font=("default",8))
    entryy = (entry,i)
    button = Button(cookies_frame,textvariable=vars_cookies[i][1],bd=0,width=2,command=lambda pi = entryy:toggle_cookie(pi),highlightthickness=0,padx=4,pady=0,bg=pal[4],activebackground=pal[5],fg=pal[6],activeforeground=pal[6],font=("default",8),anchor=SE)

    entry.grid(column=3,row=i,padx=2)
    button.grid(column=4,row=i,padx=2,pady=2)
    cookie_entries.append((entry,button))
print(cookie_entries)

thumbimage = Image.new("RGB",(1,1),pal[2])
thumbphotoimage = ImageTk.PhotoImage(thumbimage)

thumbnail = Label(second_area,text="test",bd=0,image=thumbphotoimage,width=thumb_size,height=thumb_size,bg=pal[2],highlightthickness=0)
thumbnail.grid(column=1,row=0,padx=2,pady=2)



second_area.pack()


dir_frame = Frame(tk,bg=pal[1])
dir_label = Label(dir_frame,text="Save to Directory:",bd=0,bg="#222",fg="#eee",highlightthickness=0,font=("default",8),padx=2,pady=0)
dir_entry = Entry(dir_frame,textvariable=var_directory,width=72,bd=0,bg="#444",fg="#eee",highlightthickness=0,font=("default",8))
dir_label.pack(side=LEFT)
dir_entry.pack(side=LEFT,padx=2)

def getdir():
    var_directory.set(askdirectory())

pickdir = Button(dir_frame,width =16,padx=0,pady=0,bd=0,bg=pal[4],fg=pal[6],activebackground=pal[5],highlightthickness=0,text="PICK DIRECTORY",activeforeground=pal[6],font=("default",8),command=getdir)
pickdir.pack(side=LEFT,padx=2)

dir_frame.pack(padx=2,pady=2)

cookies_frame.pack()

status_board = Label(img_canv_and_cookies,width=32,height=1,padx=0,pady=0,bd=0,highlightthickness=0,textvariable=var_log,font=("default",8),bg=pal[1],fg=pal[3])
status_board.pack(padx=0,pady=1)

imgname_label = Label(img_canv_and_cookies,width=32,padx=0,pady=0,bd=0,highlightthickness=0,font=("default",8),textvariable=var_currentimgname)
imgname_label.pack()

img_canv_and_cookies.grid(column=0,row=0)



tk.mainloop()