###########      IMPORTING      ##########

import tkinter as tk #import tkinter for gui
import os #import os so the code stops running upon clicking the X

###########      IMPORTING      ##########



###########      BULK OF CODE      ##########
# everything in this section is executed every time something changes.

def my_tracer(a, b, c): # traced variables send 3 arguments to this
    try:
        fr=float(fv.get())
    except:
        fr=1000 #by default, no rounding happens. not recommended

    try:
        mod=cTime(mv.get())
    except:     #the modifier, added to the resulting time
        mod=0

    stext = sv.get().split(',') #start point
    for i in range (len(stext)):
        if stext[i][4:7]=='cmt':
            start=float(stext[i].split('"')[-2]) #crops out the useless stuff
            start = start - start%(1/fr) #rounds down the time to the start of a frame

    etext = ev.get().split(',') #end point
    for i in range (len(etext)):
        if etext[i][4:7]=='cmt':
            end=float(etext[i].split('"')[-2])
            end -= end%(1/fr)

    #print(end-start+mod)
    try:        # if youtube debug info is entered correctly, displays time as h m s ms
        if end-start+mod < 0:
            negative=True   # if start > end, a negative is put in front of the absolute value of
                            #the result
        else:
            negative=False
        new_text = negative*"- "+realtime(abs(end-start+mod))
    except:
        try: # inputs in the form of h:mm:ss instead of youtube debug points
             #note: does not apply extra frame or framerate but does apply modifier
             #this is because some video editing software displays times as m:ss:ff
             #and extra frame wouldn't be able to know this
            time = cTime(ev.get())-cTime(sv.get())+mod
            if time < 0:
                negative=True
            else:
                negative=False
            new_text = "-"*negative+uTime(abs(time))
        except:
            new_text = ""
    tv.set(new_text)
    #tv.set("- 999h 59m 59s 999ms")     #debug line to get longest conceivable input
###########      BULK OF CODE      ##########


###########      MISC. FUNCTIONS      ##########
def close():    # normally, pressing the close button on tkinter window doesn't terminate script
    os._exit(0) # <- ends script so it doesn't keep running


def cTime(a): #converts x:xx:xx.xxx to xxxxxx.xxx
    x=0
    for i in range(len(a.split(":"))):
        x+=60**i*float(a.split(":")[-(i+1)])
    return x

def uTime(a): #inverse of cTime
    a = round(a,3)
    t1, t0 = divmod(a, 1)
    t2, t1 = divmod(t1, 60)
    t3, t2 = divmod(t2, 60)
    t0= round(t0*1000)
    if t0==0:
        t4, t3 = divmod(t3,  60)
    else:
        t4=0

    if t4!=0:       #formatting :(
        return("%d:%02d:%02d:%02d" % (t4, t3, t2, t1))
    elif t3!=0 and t0!=0:   # despite similarities, realtime and uTime can't be merged into
                            #the same function because :::. and h/m/s/ms are read differently
        return("%d:%02d:%02d.%03d" % (t3, t2, t1, t0))
    elif t3!=0 and t0==0:
        return("%d:%02d:%02d" % (t3, t2, t1))
    elif t2!=0 and t0!=0:
        return("%d:%02d.%03d" % (t2, t1,t0))
    elif t2!=0 and t0==0:
        return(("%d:%02d" % (t2, t1)))
    elif t0!=0:
        return("%d.%03d" % (t1,t0))
    else:
        return(t1)
    

def realtime(time): # turn XXXXXX.xxx into XXXh XXm XXs xxxms
    time=round(time,3)
    ms=(1000*time)%1000
    time-=time%1
    s=time%60
    time=(time-s)/60      #finding number of hours, minutes, etc
    m=time%60
    time=(time-m)/60
    h=time

    #print(h)
    #print(m)
    #print(s)
    #print(ms)

    ms="{:03d}".format(int(ms)) #formatting
    if h!=0:
        h=int(h)
        m="{:02d}".format(int(m))
        s="{:02d}".format(int(s))
        return(str(h)+'h '+str(m)+'m '+str(s)+'s '+str(ms)+'ms')
    elif m!=0:
        m=int(m)
        s="{:02d}".format(int(s))
        return(str(m)+'m '+str(s)+'s '+str(ms)+'ms')
    else:
        s=int(s)
        return(str(s)+'s '+str(ms)+'ms')

#print(realtime(5.999999999999972))
#print(realtime(6.000000000000072))     # float precision tests
#print(uTime(5.999999999999972))        # binary floats are awful :(
#print(uTime(6.000000000000000072))
    
###########      MISC. FUNCTIONS      ##########



###########      GUI      ##########
    
while True:
    root = tk.Tk()
    root.title("SP's Retiming Tool")
    #root.iconbitmap('retime.ico')
    root.protocol("WM_DELETE_WINDOW", close) # procedure done upon clicking X

    tk.Label(root,text="Video Framerate",font=("Hobo Std", 16)).grid(row=0,column=0)
    tk.Label(root,text="Modifier",font=("Hobo Std", 16)).grid(row=0,column=1)

    fv= tk.StringVar()
    fv.trace('w', my_tracer)
    f=tk.Entry(root,width=10,font=("Hobo Std", 20),textvariable=fv) #framerate
    f.grid(row=1,column=0,columnspan=1)
    # ^ All input code will look something like this, allowing my_tracer() to
    #update every time any updates are made
    

    mv = tk.StringVar()
    mv.trace('w', my_tracer)
    m=tk.Entry(root,width=10,font=("Hobo Std", 20),textvariable=mv) #framerate
    m.grid(row=1,column=1,columnspan=1)
    # Modifier is added to the result, allowing for quick changes to it.
    #of course, this can be negative


    tk.Label(root,text="Start frame",
             font=("Hobo Std", 16)).grid(row=2,columnspan=3)
    sv = tk.StringVar() # using StringVar means the result can
                        #dynamically change as entry values change
    sv.trace('w', my_tracer) # run my_tracer if value was changed (w = write)
    s=tk.Entry(root,width=26,font=("Hobo Std", 20),textvariable=sv) #start debug info
    s.grid(row=3,column=0,columnspan=2)

    
    tk.Label(root,text="End frame",
             font=("Hobo Std", 16)).grid(row=4,columnspan=3)
    ev = tk.StringVar() # or StringVar(top) 
    ev.trace('w', my_tracer) # run my_tracer if value was changed (w = write)
    e=tk.Entry(root,width=26,font=("Hobo Std", 20),textvariable=ev) #end debug info
    e.grid(row=5,column=0,columnspan=2)

    tv = tk.StringVar() # or StringVar(top) 
    t = tk.Label(root, textvariable=tv,font=("Hobo Std", 30),background="white",width=18)
    t.grid(row=7,columnspan=2,pady=(10,5),padx=10)


    def clear(): #restores all inputs to default values and clears the output
        f.delete(0, tk.END)
        m.delete(0, tk.END)
        s.delete(0, tk.END)
        e.delete(0, tk.END)
        tv.set("")
        
    cb=tk.Button(root,text="Clear",font=("Hobo Std", 30),width=14,command=clear)
    cb.grid(row=8,columnspan=2,pady=5)

    root.mainloop() #executes the code

###########      GUI      ##########
