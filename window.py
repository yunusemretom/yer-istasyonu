"""
Created by Yunus Emre TOM

"""

from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import serial.tools.list_ports
import time
from tkinter import messagebox
from watauto import *
from tkVideoPlayer import TkinterVideo
from connection_lib import *


def web_baslat():
    global hazir
    try:
        run_console_command1("WEB sitesi başlatılıyor. Lütfen bekleyin.")
        website_start()
        run_console_command1("WEB hazırlandı okuma başlatılıyor.")
        hazir = 1
    except Exception as e:
        run_console_command(f"Hata oluştu. Hata {e}")
        hazir = 0

def btn_clicked():
    run_console_command1("button clicked")
    print("Button Clicked")

def run_console_command(command):
    
    console_output.insert(tk.END, f">> {command}\n")
    
    # Otomatik olarak aşağıya kaydır
    console_output.see(tk.END)

def run_console_command1(command):
    
    console_output1.insert(tk.END, f">> {command}\n")
    
    # Otomatik olarak aşağıya kaydır
    console_output.see(tk.END)

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        #print("Tespit edilen portlar:")
        for port, desc, hwid in sorted(ports):
            #print(f"{port}: {desc} [ID: {hwid}]")
            if port not in langs:
                langs.append(port)
        
        Combo['values'] = langs
        Combo.set(langs)
    else:
        pass
        #run_console_command("port yok")
        #print("Bağlı port bulunamadı.")

def saat():
    
    current_time = time.localtime()

    # Saat ve dakika bilgilerini al
    hour = current_time.tm_hour
    minute = current_time.tm_min
    saat_d = str(hour) + ":"+str(minute) 
    
    
    canvas.itemconfig(saat_L, text=saat_d)

def tarih():
    
    current_time = time.localtime()

    # Saat ve dakika bilgilerini al
    gun = current_time.tm_mday
    ay = current_time.tm_mon
    yil = current_time.tm_year

    tarih_D = str(gun) + "."+ str(ay) + "."+ str(yil)
    canvas.itemconfig(tarih_L, text=tarih_D)

def port_yazdir():
    port = Combo.get()
    canvas.itemconfig(port_Y1, text=port)
    canvas.itemconfig(port_Y2, text=port)

def periodic_update():
    global left_value, right_value, hazir,x,y,gonder_H,gonder_H,gonder_K
    saat()
    tarih()
    list_serial_ports()
    port_yazdir()
    
    if hazir == 1:
        try:
            sonuc = link_bul()    
            if sonuc != None:
                split_coordinates = sonuc.split(',')
                print(split_coordinates)
                # Sol ve sağ değerlere erişim
                left_value = float(split_coordinates[0])
                right_value = float(split_coordinates[1])
                
                canvas.itemconfig(lat, text=left_value)
                canvas.itemconfig(lon, text=right_value)
                x=split_coordinates[0]
                y=split_coordinates[1]
                gonder_H =1


        except Exception as e:
            run_console_command(f"Hata oluştu. Hata {e}")
            hazir = 0
            
    if gonder_K == 1:
        gonder_H = 0
        degerler = mav_controller.distance()
        run_console_command1(degerler)
        try:
            if degerler["distance"] <1:
                gonder_K = 0
                
        except:
            pass

    window.after(10, periodic_update) 

def check_video_end():
        global uploaded
        # Video bitmişse, etiketi kaldırabilirsiniz
        if videoplayer.is_paused():
            videoplayer.pack_forget()

        else:
            # Video hala oynatılıyorsa, bir süre sonra tekrar kontrol et
            window.after(100, check_video_end)

def kapatma_istegi():
    result = messagebox.askokcancel("Çıkış", "Pencereyi kapatmak istiyor musunuz?")
    if result:
        window.destroy()
        try:
            browser_close()
        except:
            pass

def cordinate_load():
    global mav_controller
    if gonder_H == 1 and  baglanti_K ==1:
        mav_controller.change_mode("GUIDED")
        mav_controller.TARGET_LOCATIONS[0]["latitude"] = x
        mav_controller.TARGET_LOCATIONS[0]["longitude"] = y
    else:
        run_console_command("Konum verisi yok! Lütfen konum verisi için bekleyiniz...")

def gonder():   
    global gonder_K

    if gonder_H == 1 and baglanti_K == 1:
        
        mav_controller.takeoff(20)
        mav_controller.go_waypoint()
        gonder_K = 1    
        
    else:
        run_console_command("Konum verisi yok! Lütfen konum verisi için bekleyiniz...")

def RTL_MODE():
    global gonder_K, gonder_H
    gonder_K = 0
    gonder_H = 0
    try:
        mav_controller.change_mode("RTL")
    except:
        run_console_command("Baglanti yok!.. HATA")

def Emergency():
    try:
        mav_controller.disarm()
    except:
        run_console_command("Baglanti yok!.. HATA")

def baglan_f():
    global mav_controller
    port = Combo.get()
    try:
        mav_controller.connection_port(port)
    except:

        run_console_command("Port uyumlu değil!..")

langs = []
left_value = ""
right_value = ""
hazir = 0
uploaded= False
x=0
y=0
gonder_H=0 #gondermeye hazırlık
gonder_K = 0 #gonderme kontrol
baglanti_K = 0 #baglanti kontrolu

mav_controller = MavlinkController()

window = Tk()
window.title("GRAVITEAM")
window.geometry("1200x700")
window.configure(bg = "#ffffff")
window.iconbitmap("icon.ico")

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 700,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    600.0, 350.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
gonder_B = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = gonder,
    relief = "flat")

gonder_B.place(
    x = 920, y = 325,
    width = 97,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
yukle = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = cordinate_load,
    relief = "flat")

yukle.place(
    x = 920, y = 237,
    width = 97,
    height = 29)

img2 = PhotoImage(file = f"img2.png")
rtl = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = RTL_MODE,
    relief = "flat")

rtl.place(
    x = 869, y = 373,
    width = 199,
    height = 31)

img3 = PhotoImage(file = f"img3.png")
emg = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = Emergency,
    relief = "flat")

emg.place(
    x = 869, y = 423,
    width = 199,
    height = 31)

lat = canvas.create_text(
    83.5, 252.0,
    text = "0.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

lon = canvas.create_text(
    262.5, 248.0,
    text = "0.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y1 = canvas.create_text(
    980.5, 210.0,
    text = "",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y2 = canvas.create_text(
    885.5, 297.0,
    text = "",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

tarih_L = canvas.create_text(
    626.5, 214.0,
    text = "27:08:2006",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

saat_L = canvas.create_text(
    624.5, 252.0,
    text = "22:05",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

yukseklik = canvas.create_text(
    246.0, 329.5,
    text = "00.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(24.0)))

img4 = PhotoImage(file = f"img4.png")
baglan = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = baglan_f,
    relief = "flat")

baglan.place(
    x = 334, y = 418,
    width = 105,
    height = 37)

img5 = PhotoImage(file = f"img5.png")
web_starter = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = web_baslat,
    relief = "flat")

web_starter.place(
    x = 519, y = 290,
    width = 165,
    height = 41)


console_output1 = scrolledtext.ScrolledText(window, bg="black", fg="white")  # Konsol çıktısının arka planını siyah, metin rengini beyaz yapalım
console_output1.place(
    x = 23, y = 534,
    width = 550,
    height = 155)

console_output = scrolledtext.ScrolledText(window, bg="black", fg="white")  # Konsol çıktısının arka planını siyah, metin rengini beyaz yapalım
console_output.place(
    x = 625, y = 534,
    width = 550,
    height = 155)


Combo = ttk.Combobox(window, values = langs)
Combo.set("Port Seç")
Combo.place(x = 110, y = 439)


videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"hazirlik.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video
check_video_end()

videoplayer.lift(gonder_B)
videoplayer.lift(yukle)
videoplayer.lift(rtl)
videoplayer.lift(emg)
videoplayer.lift(baglan)
videoplayer.lift(console_output1)
videoplayer.lift(console_output)
videoplayer.lift(Combo)

periodic_update()
window.protocol("WM_DELETE_WINDOW", kapatma_istegi)

list_serial_ports()



window.resizable(False, False)
window.mainloop()

"""
Created by Yunus Emre TOM

"""

from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import serial.tools.list_ports
import time
from tkinter import messagebox
from watauto import *
from tkVideoPlayer import TkinterVideo
from connection_lib import *


def web_baslat():
    global hazir
    try:
        run_console_command1("WEB sitesi başlatılıyor. Lütfen bekleyin.")
        website_start()
        run_console_command1("WEB hazırlandı okuma başlatılıyor.")
        hazir = 1
    except Exception as e:
        run_console_command(f"Hata oluştu. Hata {e}")
        hazir = 0

def btn_clicked():
    run_console_command1("button clicked")
    print("Button Clicked")

def run_console_command(command):
    
    console_output.insert(tk.END, f">> {command}\n")
    
    # Otomatik olarak aşağıya kaydır
    console_output.see(tk.END)

def run_console_command1(command):
    
    console_output1.insert(tk.END, f">> {command}\n")
    
    # Otomatik olarak aşağıya kaydır
    console_output.see(tk.END)

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        #print("Tespit edilen portlar:")
        for port, desc, hwid in sorted(ports):
            #print(f"{port}: {desc} [ID: {hwid}]")
            if port not in langs:
                langs.append(port)
        
        Combo['values'] = langs
        Combo.set(langs)
    else:
        pass
        #run_console_command("port yok")
        #print("Bağlı port bulunamadı.")

def saat():
    
    current_time = time.localtime()

    # Saat ve dakika bilgilerini al
    hour = current_time.tm_hour
    minute = current_time.tm_min
    saat_d = str(hour) + ":"+str(minute) 
    
    
    canvas.itemconfig(saat_L, text=saat_d)

def tarih():
    
    current_time = time.localtime()

    # Saat ve dakika bilgilerini al
    gun = current_time.tm_mday
    ay = current_time.tm_mon
    yil = current_time.tm_year

    tarih_D = str(gun) + "."+ str(ay) + "."+ str(yil)
    canvas.itemconfig(tarih_L, text=tarih_D)

def port_yazdir():
    port = Combo.get()
    canvas.itemconfig(port_Y1, text=port)
    canvas.itemconfig(port_Y2, text=port)

def periodic_update():
    global left_value, right_value, hazir,x,y,gonder_H,gonder_H,gonder_K
    saat()
    tarih()
    list_serial_ports()
    port_yazdir()
    
    if hazir == 1:
        try:
            sonuc = link_bul()    
            if sonuc != None:
                split_coordinates = sonuc.split(',')
                print(split_coordinates)
                # Sol ve sağ değerlere erişim
                left_value = float(split_coordinates[0])
                right_value = float(split_coordinates[1])
                
                canvas.itemconfig(lat, text=left_value)
                canvas.itemconfig(lon, text=right_value)
                x=split_coordinates[0]
                y=split_coordinates[1]
                gonder_H =1


        except Exception as e:
            run_console_command(f"Hata oluştu. Hata {e}")
            hazir = 0
            
    if gonder_K == 1:
        gonder_H = 0
        degerler = mav_controller.distance()
        run_console_command1(degerler)
        try:
            if degerler["distance"] <1:
                gonder_K = 0
                
        except:
            pass

    window.after(10, periodic_update) 

def check_video_end():
        global uploaded
        # Video bitmişse, etiketi kaldırabilirsiniz
        if videoplayer.is_paused():
            videoplayer.pack_forget()

        else:
            # Video hala oynatılıyorsa, bir süre sonra tekrar kontrol et
            window.after(100, check_video_end)

def kapatma_istegi():
    result = messagebox.askokcancel("Çıkış", "Pencereyi kapatmak istiyor musunuz?")
    if result:
        window.destroy()
        try:
            browser_close()
        except:
            pass

def cordinate_load():
    global mav_controller
    if gonder_H == 1 and  baglanti_K ==1:
        mav_controller.change_mode("GUIDED")
        mav_controller.TARGET_LOCATIONS[0]["latitude"] = x
        mav_controller.TARGET_LOCATIONS[0]["longitude"] = y
    else:
        run_console_command("Konum verisi yok! Lütfen konum verisi için bekleyiniz...")

def gonder():   
    global gonder_K

    if gonder_H == 1 and baglanti_K == 1:
        
        mav_controller.takeoff(20)
        mav_controller.go_waypoint()
        gonder_K = 1    
        
    else:
        run_console_command("Konum verisi yok! Lütfen konum verisi için bekleyiniz...")

def RTL_MODE():
    global gonder_K, gonder_H
    gonder_K = 0
    gonder_H = 0
    try:
        mav_controller.change_mode("RTL")
    except:
        run_console_command("Baglanti yok!.. HATA")

def Emergency():
    try:
        mav_controller.disarm()
    except:
        run_console_command("Baglanti yok!.. HATA")

def baglan_f():
    global mav_controller
    port = Combo.get()
    try:
        mav_controller.connection_port(port)
    except:

        run_console_command("Port uyumlu değil!..")

langs = []
left_value = ""
right_value = ""
hazir = 0
uploaded= False
x=0
y=0
gonder_H=0 #gondermeye hazırlık
gonder_K = 0 #gonderme kontrol
baglanti_K = 0 #baglanti kontrolu

mav_controller = MavlinkController()

window = Tk()
window.title("GRAVITEAM")
window.geometry("1200x700")
window.configure(bg = "#ffffff")
window.iconbitmap("icon.ico")

canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 700,
    width = 1200,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    600.0, 350.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
gonder_B = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = gonder,
    relief = "flat")

gonder_B.place(
    x = 920, y = 325,
    width = 97,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
yukle = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = cordinate_load,
    relief = "flat")

yukle.place(
    x = 920, y = 237,
    width = 97,
    height = 29)

img2 = PhotoImage(file = f"img2.png")
rtl = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = RTL_MODE,
    relief = "flat")

rtl.place(
    x = 869, y = 373,
    width = 199,
    height = 31)

img3 = PhotoImage(file = f"img3.png")
emg = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = Emergency,
    relief = "flat")

emg.place(
    x = 869, y = 423,
    width = 199,
    height = 31)

lat = canvas.create_text(
    83.5, 252.0,
    text = "0.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

lon = canvas.create_text(
    262.5, 248.0,
    text = "0.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y1 = canvas.create_text(
    980.5, 210.0,
    text = "",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y2 = canvas.create_text(
    885.5, 297.0,
    text = "",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

tarih_L = canvas.create_text(
    626.5, 214.0,
    text = "27:08:2006",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

saat_L = canvas.create_text(
    624.5, 252.0,
    text = "22:05",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

yukseklik = canvas.create_text(
    246.0, 329.5,
    text = "00.00",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(24.0)))

img4 = PhotoImage(file = f"img4.png")
baglan = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = baglan_f,
    relief = "flat")

baglan.place(
    x = 334, y = 418,
    width = 105,
    height = 37)

img5 = PhotoImage(file = f"img5.png")
web_starter = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = web_baslat,
    relief = "flat")

web_starter.place(
    x = 519, y = 290,
    width = 165,
    height = 41)


console_output1 = scrolledtext.ScrolledText(window, bg="black", fg="white")  # Konsol çıktısının arka planını siyah, metin rengini beyaz yapalım
console_output1.place(
    x = 23, y = 534,
    width = 550,
    height = 155)

console_output = scrolledtext.ScrolledText(window, bg="black", fg="white")  # Konsol çıktısının arka planını siyah, metin rengini beyaz yapalım
console_output.place(
    x = 625, y = 534,
    width = 550,
    height = 155)


Combo = ttk.Combobox(window, values = langs)
Combo.set("Port Seç")
Combo.place(x = 110, y = 439)


videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"hazirlik.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video
check_video_end()

videoplayer.lift(gonder_B)
videoplayer.lift(yukle)
videoplayer.lift(rtl)
videoplayer.lift(emg)
videoplayer.lift(baglan)
videoplayer.lift(console_output1)
videoplayer.lift(console_output)
videoplayer.lift(Combo)

periodic_update()
window.protocol("WM_DELETE_WINDOW", kapatma_istegi)

list_serial_ports()



window.resizable(False, False)
window.mainloop()
