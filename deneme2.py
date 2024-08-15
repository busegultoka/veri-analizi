from tkinter import*
import os
from tkinter import ttk
from datetime import datetime
 
global file_path
terms=["CAM UPER encoding","CAM UPER decoding","DENM UPER encoding","DENM UPER decoding","ULAK_MAP","ULAK_STN","ULAK_SLW","ULAK_CCRW","ULAK_TTG","ULAK_SHD","ULAK_SVIO","ULAK_VRU","ULAK_WWD","ULAK_mai","ULAK_loh","ULAK_rw","ULAK_wc","ULAK_tisr"]
term_widgets={}
selected_file=None

def log(file_path):
    files=os.listdir(file_path)
    listebox.delete(0,END)
    for file in files:
        if file.endswith(".log"):
            listebox.insert(END,file)
            
def select(event):
    global selected_file
    selected_index=listebox.curselection()
    if selected_index:
        selected_file=listebox.get(selected_index)
        file_path=selected_file
        print("Seçilen Dosya:",selected_file)
 
def ekle():
    log(file_path)
 
def oku(file_path):
    try:
        with open(file_path,'r') as file:
            lines=file.readlines()
        return lines
    except FileNotFoundError:
        print("Dosya Bulunamadı!")
        return []
    except Exception as e:
        print("Bir Hata Oluştu!:{e}")
        return []
 
def adet(file_path,terms):
    counts={term: 0 for term in terms}
    lines=oku(file_path)
    if not lines:
        return counts
    for line in lines:
        for term in terms:
            if term in line:
                counts[term]+=1
    return counts

def yazdır(counts):
    for term, count in counts.items():
        if term in term_widgets:
            term_widgets[term].config(text=str(count))
            
def birleştir(selected_file,terms):
    counts=adet(selected_file,terms)
    yazdır(counts)

def dateTime(selected_file,terms):
    date=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    saat=line[:2]
                    dakika=line[2:4]
                    saniye=line[4:6]
                    mili_saniye=line[7:11]
                    data=(saat,":",dakika,":",saniye,":",mili_saniye)
                    date.append(''.join(data))
        return date
    except Exception as e:
            print(f"Bir Hata Oluştu:{e}")

def latitude(selected_file,terms):
    latitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    keyword='<latitude>'
                    start=line.find(keyword)
                    index1=start+len(keyword)
                    keyword2='</latitude>'
                    stop=line.find(keyword2)
                    index2=stop
                    if start<len(line) and stop<=len(line) and start<=stop:
                        word=line[index1:stop]
                        latitudes.append(''.join(word))
        return latitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def longitude(selected_file,terms):
    longitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0]  in line:
                    kel='<longitude>'
                    st=line.find(kel) 
                    ind1=len(kel)+st
                    kel2='</longitude>'
                    sp=line.find(kel2)
                    ind2=sp
                    if st<len(line) and sp<=len(line) and st<=sp:
                        snc=line[ind1:sp]
                        longitudes.append(''.join(snc))
        return longitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def speedValue(selected_file,terms):
    speeds=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    kelime='<speedValue>'
                    baş=line.find(kelime)
                    indo1=baş+len(kelime)
                    kelime1='</speedValue>'
                    son=line.find(kelime1)
                    indo2=son
                    if indo1<len(line) and indo2<=len(line) and indo1<=indo2:
                        value=line[indo1:indo2]
                        speeds.append(''.join(value))
        return speeds
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def headingValue(selected_file,terms):
    heads=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    word='<headingValue>'
                    start=line.find(word)
                    index=start+len(word)
                    word2='</headingValue'
                    stop=line.find(word2)
                    index2=stop
                    if index<len(line) and stop<=len(line) and start<=stop:
                        head=line[index:stop]
                        heads.append(''.join(head))
            return heads
    except Exception as e:
        print(f"Bir Hata Oluştı:{e}")
        
def tablo():
    date=dateTime(selected_file,terms)
    latitudes=latitude(selected_file,terms)
    longitudes=longitude(selected_file,terms)
    speeds=speedValue(selected_file,terms)
    heads=headingValue(selected_file,terms)
    if date is None:
        date=[]
    if latitudes  is None:
        latitudes=[]
    if longitudes is None:
        longitudes=[]
    if  speeds is None:
        speeds=[]
    if heads is None:
        heads=[]
    for i in range(len(date)):
        time=date[i] if i <len(date) else ''
        lat=latitudes[i] if i<len(latitudes) else ''
        long=longitudes[i] if i <len(longitudes) else ''
        speed=speeds[i] if i<len(speeds) else ''
        hea=heads[i] if i<len(heads) else ''
        table.insert('','end',values=(time,lat,long,speed,hea))

def sure(selected_file,terms):
    sureler=[]
    fark=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    saat=line[:2]
                    dakika=line[2:4]
                    saniye=line[4:6]
                    mili_saniye=line[7:10]
                    zaman=f"{saat}:{dakika}:{saniye}.{mili_saniye}"
                    sureler.append(datetime.strptime(zaman,"%H:%M:%S.%f"))
            for i in range(1,len(sureler)):
                      fark.append(sureler[i]-sureler[i-1])
            return  fark
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def fark_yaz(selected_file,terms):
    fark=sure(selected_file,terms)
    if fark is None:
        fark=[]
    for i in (range(len(fark))):
        çıkar=str(fark[i]) if i<len(fark) else ''
        clock.insert(END,çıkar)
                                
def new_window():
      window2=Tk()
      window2.title("CAM UPER encoding")
      window2.config(bg="white")
      window2.geometry("800x350")

      sb2=Scrollbar(window2)
      
      global table
      table=ttk.Treeview(window2,columns=("Column1","Column2","Column3","Column4","Column5"),show="headings",yscrollcommand=sb2.set)
      sb2.config(orient="vertical",command=table.yview)
      sb2.grid(row=0,column=1,padx=2,pady=2,sticky="ns")

      table.heading("Column1",text="Saat")
      table.heading("Column2",text="Latitude")
      table.heading("Column3",text="Longitude ")
      table.heading("Column4",text="speedValue")
      table.heading("Column5",text="headingValue")

      table.column("Column1",width=100)
      table.column("Column2",width=100)
      table.column("Column3",width=100)
      table.column("Column4",width=100)
      table.column("Column5",width=100)
      
      tablo()

      table.grid(row=0,column=0,padx=2,pady=2)
      
      close=Button(window2,text="Çıkış",font="arial 12",bg="white",command=window2.destroy)
      close.grid(row=1,column=3,padx=2,pady=2)

      global clock

      clock=Listbox(window2,bg="white",font="arial 12")
      clock.grid(row=0,column=2,padx=2,pady=2)

      listele=Button(window2,text="Süreleri Listele",font="arial 12",bg="white",command= lambda:fark_yaz(selected_file,terms))
      listele.grid(row=1,column=2,padx=2,pady=2)

      window2.mainloop()
      
def deco_saat(selected_file,terms):
    dates=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[1] in line:
                    saat=line[:2]
                    dakika=line[2:4]
                    saniye=line[4:6]
                    mili_saniye=line[7:11]
                    date=saat,":",dakika,":",saniye,":",mili_saniye
                    dates.append(''.join(date))
        return dates
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def deco_latitude(selected_file,terms):
    deco_latitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[1] in line:
                    wd='<latitude>'
                    bş=line.find(wd)
                    id1=bş+len(wd)
                    wd2='</latitude>'
                    sn=line.find(wd2)
                    id2=sn
                    if id1<len(line) and id2<=len(line) and id1<=id2:
                        dl=line[id1:sn]
                        deco_latitudes.append(''.join(dl))
        return deco_latitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def deco_longitude(selected_file,terms):
    deco_longitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[1] in line:
                    kl='<longitude>'
                    sy=line.find(kl)
                    inx=sy+len(kl)
                    kl2='</longitude>'
                    sy2=line.find(kl2)
                    if inx<len(line) and sy2<=len(line) and inx<=sy2:
                        longi=line[inx:sy2]
                        deco_longitudes.append(''.join(longi))
        return deco_longitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def altitude_values(selected_file,terms):
    altitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[1] in line:
                    alt='<altitudeValue>'
                    star=line.find(alt)
                    terim=star+len(alt)
                    üst='</altitudeValue>'
                    sto=line.find(üst)
                    if terim<len(line) and sto<=len(line) and terim<=sto:
                        alti=line[terim:sto]
                        altitudes.append(''.join(alti))
        return altitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def stationID(selected_file,terms):
    stations=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[1] in line:
                    stat='<stationID>'
                    sta=line.find(stat)
                    inx=sta+len(stat)
                    stot='</stationID>'
                    stopp=line.find(stot)
                    if inx<len(line) and stopp<=len(line) and inx<=stopp:
                        station=line[inx:stopp]
                        stations.append(''.join(station))
        return stations
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")
                                   
def tablo2():
    dates=deco_saat(selected_file,terms)
    deco_latitudes=deco_latitude(selected_file,terms)
    deco_longitudes=deco_longitude(selected_file,terms)
    altitudes=altitude_values(selected_file,terms)
    stations=stationID(selected_file,terms)
    if dates is None:
        dates=[]
    if deco_latitudes is None:
        deco_latitudes=[]
    if deco_longitudes is None:
        deco_longitudes=[]
    if altitudes is None:
        altitudes=[]
    if stations is None:
        stations=[]
    for i in (range(len(dates))):
        clock=dates[i] if i<len(dates) else ''
        lt=deco_latitudes[i] if i<len(deco_latitudes) else ''
        lg=deco_longitudes[i] if i<len(deco_longitudes) else ''
        alt_value=altitudes[i] if i<len(altitudes) else ''
        st=stations[i] if i<len(stations) else ''
        table2.insert('','end',values=(clock,lt,lg,alt_value,st))

def sure2(selected_file,terms):
    sureler2=[]
    farklar2=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[0] in line:
                    saat2=line[:2]
                    dakika2=line[2:4]
                    saniye2=line[4:6]
                    mili_saniye2=line[7:10]
                    saat2=f"{saat2}:{dakika2}:{saniye2}.{mili_saniye2}"
                    sureler2.append(datetime.strptime(saat2,"%H:%M:%S.%f"))
            for i in range(1,len(sureler2)):
                farklar2.append(sureler2[i]-sureler2[i-1])
        return farklar2
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def fark2(selected_file,terms):
    farklar2=sure2(selected_file,terms)
    if farklar2 is None:
        farklar2=[]
    for i in range(1,len(farklar2)):
        çıkar2=str(farklar2[i]) if i<len(farklar2) else ''
        sf2.insert(END,çıkar2)
        
def new_window2():
    window3=Tk()
    window3.title("CAM UPER decoding")
    window3.config(bg="white")
    window3.geometry("800x350")
  
    sb3=Scrollbar(window3)
    
    global table2

    table2=ttk.Treeview(window3,column=("Column1","Column2","Column3","Column4","Column5"),show="headings",yscrollcommand=sb3.set)
    sb3.config(orient="vertical",command=table2.yview)
    sb3.grid(row=0,column=1,padx=2,pady=2,sticky="ns")

    table2.heading("Column1",text="Saat")
    table2.heading("Column2",text="Latitude")
    table2.heading("Column3",text="Longitude")
    table2.heading("Column4",text="altitudeValue")
    table2.heading("Column5",text="headiingValue")

    table2.column("Column1",width=100)
    table2.column("Column2",width=100)
    table2.column("Column3",width=100)
    table2.column("Column4",width=100)
    table2.column("Column5",width=100)

    table2.grid(row=0,column=0,padx=2,pady=2)

    tablo2()

    kapat2=Button(window3,text="Çıkış",font="arial 12",bg="white",command=window3.destroy)
    kapat2.grid(row=2,column=3,padx=2,pady=2)

    global sf2

    sf2=Listbox(window3,font="arial 12",bg="white")
    sf2.grid(row=0,column=2,padx=2,pady=2)

    clock2=Button(window3,text="Süreleri Göster",bg="white",font="arial 12",command= lambda:fark2(selected_file,terms))
    clock2.grid(row=1,column=2,padx=2,pady=2)
                
    
    window3.mainloop()

def referenceTime(selected_file,terms):
    referenceTimes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[2] in line:
                    kelime1='<referenceTime>'
                    start=line.find(kelime1)
                    index1=start+len(kelime1)
                    kelime2='</referenceTime>'
                    stop=line.find(kelime2)
                    if index1<len(line) and stop<=len(line) and index1<=stop:
                        reference=line[index1:stop]
                        referenceTimes.append(''.join(reference))
        return referenceTimes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def causeCode(selected_file,terms):
    causeCodes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[2] in line:
                    word='<causeCode>'
                    start=line.find(word)
                    index=start+len(word)
                    word2='</causeCode>'
                    stop=line.find(word2)
                    if index<len(line) and stop<=len(line) and index<=stop:
                        cause=line[index:stop]
                        causeCodes.append(''.join(cause))
        return causeCodes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def sub_cause_code(selected_file,terms):
    subCause=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[2] in line:
                    word='<subCauseCode>'
                    start=line.find(word)
                    index=start+len(word)
                    word2='</subCauseCode>'
                    stop=line.find(word2)
                    if  start<len(line) and stop<=len(line) and start<=stop:
                        sub=line[index:stop]
                        subCause.append(''.join(sub))
        return subCause
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def denm_speed(selected_file,terms):
    denm_speed_values=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[2] in line:
                    word='<speedValue>'
                    start=line.find(word)
                    index=start+len(word)
                    word2='</speedValue>'
                    stop=line.find(word2)
                    if index<len(line) and stop<=len(line) and index<=stop:
                        denm=line[index:stop]
                        denm_speed_values.append(''.join(denm))
        return denm_speed_values
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")

def denm_longitude(selected_file,terms):
    denm_longitudes=[]
    try:
        with open(selected_file,'r') as file:
            for line in file:
                if terms[2] in line:
                    word='<longitude>'
                    start=line.find(word)
                    index=start+len(word)
                    word2='</longitude>'
                    stop=line.find(word2)
                    if index<len(line) and stop<=len(line) and index<=stop:
                        dem=line[index:stop]
                        denm_longitudes.append(''.join(dem))
        return denm_longitudes
    except Exception as e:
        print(f"Bir Hata Oluştu:{e}")
        
def tablo3():
    referenceTimes=referenceTime(selected_file,terms)
    causeCodes=causeCode(selected_file,terms)
    subCause=sub_cause_code(selected_file,terms)
    denm_speed_values=denm_speed(selected_file,terms)
    denm_longitudes=denm_longitude(selected_file,terms)
    if referenceTimes is None:
        referenceTimes=[]
    if causeCodes is None:
        causeCodes=[]
    if subCause is None:
        subCause=[]
    if denm_speed_values is None:
        denm_speed_vaues=[]
    if denm_longitudes is None:
        denm_longitudes=[]
    for i in range(len(referenceTimes)):
        time=referenceTimes[i] if i<len(referenceTimes) else ''
        code=causeCodes[i] if i <len(causeCodes) else ''
        sub_code=subCause[i] if i<len(subCause) else ''
        denm_value=denm_speed_values[i] if i <len(denm_speed_values) else ''
        denm_long=denm_longitudes[i] if i<len(denm_longitudes) else ''
        table3.insert('','end',values=(time,code,sub_code,denm_value,denm_long))
        
def new_window3():
    window4=Tk()
    window4.title("DENM UPER encoding")
    window4.config(bg="white")
    window4.geometry("600x350")

    sb3=Scrollbar(window4)
    global table3
    table3=ttk.Treeview(window4,column=("Column1","Column2","Column3","Column4","Column5"),show="headings",yscrollcommand=sb3.set)

    sb3.config(orient="vertical",command=table3.yview)
    sb3.grid(row=0,column=1,padx=2,pady=2,sticky="ns")
     
    table3.heading("Column1",text="referenceTime")
    table3.heading("Column2",text="causeCode")
    table3.heading("Column3",text="subCauseCode")
    table3.heading("Column4",text="speedValue")
    table3.heading("Column5",text="longitude")

    table3.column("Column1",width=100)
    table3.column("Column2",width=100)
    table3.column("Column3",width=100)
    table3.column("Column4",width=100)
    table3.column("Column5",width=100)

    table3.grid(row=0,column=0,padx=2,pady=2)

    çıkış3=Button(window4,text="Çıkış",bg="white",font="arial 12",command=window4.destroy)
    çıkış3.grid(row=1,column=1,padx=2,pady=2)

    tablo3()

    window4.mainloop()
  
def windows():
    window=Tk()
    window.title("V2X")
    window.geometry("1100x550")
    window.config(bg="white")
 
    ip=Label(window,text="IP:",font="arial 12",bg="white")
    ip.grid(row=0,column=0,padx=2,pady=2)
 
    global ip_entry
    ip_entry=Entry(window,font="arial 12",bg="white")
    ip_entry.grid(row=0,column=1,padx=2,pady=2)
 
    key=Label(window,text="Şifre:",font="arial 12",bg="white")
    key.grid(row=0,column=2,padx=2,pady=2)
 
    global key_entry
    key_entry=Entry(window,font="arial 12",bg="white")
    key_entry.grid(row=0,column=3,padx=2,pady=2)
 
    global file_path
    file_path=("/Users/Ova/OneDrive/Masaüstü/staj yaptıklarım/kodla/")
    
    sign=Button(window,text="Giriş",font="arial 12",bg="white",command=ekle)
    sign.grid(row=0,column=4,padx=2,pady=2)
 
    out=Button(window,text="Çıkış",font="arial 12",bg="white",command=window.destroy)
    out.grid(row=4,column=4,padx=2,pady=2)
 
    frame=Frame(window,bg="white")
    frame.grid(row=1,column=0,padx=2,pady=2,sticky="ns")
 
    sb=Scrollbar(frame)
    sb.grid(row=0,column=1,sticky="ns")
 
    global listebox
    listebox=Listbox(frame,bg="white",width=40,height=20,yscrollcommand=sb.set)
    listebox.grid(row=0,column=0,padx=2,pady=2)
    listebox.bind("<<ListboxSelect>>",select)
 
    sb.config(orient="vertical",command=listebox.yview)
 
    analys=Button(frame,text="Analiz Et",font="arial 12",bg="white",command=lambda: birleştir(selected_file,terms))
    analys.grid(row=1,column=0,padx=2,pady=2)
 
    frame2=Frame(window,bg="white")
    frame2.grid(row=1,column=1,padx=2,pady=2)

    for i, term in enumerate(terms[:9]):
        label = Label(frame2, text=f"{term}:", font="arial 12", bg="white")
        label.grid(row=i, column=0, padx=2, pady=2)
        
        result_label = Label(frame2, font="arial 12", width=10)
        result_label.grid(row=i, column=1, padx=2, pady=2)
        
        term_widgets[term] = result_label
 
    frame3 = Frame(window, bg="white")
    frame3.grid(row=1, column=2, padx=2, pady=2)
 
    for i, term in enumerate(terms[9:], start=1):
        label = Label(frame3, text=f"{term}:", font="arial 12", bg="white")
        label.grid(row=i, column=0, padx=2, pady=2)
        
        result_label = Label(frame3, font="arial 12", width=10)
        result_label.grid(row=i, column=1, padx=2, pady=2)
        
        term_widgets[term] = result_label

        göster=Button(frame2,text="Göster",font="arial 12",bg="white",command=new_window)
        göster.grid(row=0,column=2,padx=2,pady=2)

        göster2=Button(frame2,text="Göster",font="arial 12",bg="white",command=new_window2)
        göster2.grid(row=1,column=2,padx=2,pady=2)

        göster3=Button(frame2,text="Göster",font="arial 12",bg="white",command=new_window3)
        göster3.grid(row=2,column=2,padx=2,pady=2)
 
    
    window.mainloop()
windows()
