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
Combo.place(x = 110, y = 340)


videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"hazirlik.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video
check_video_end()

videoplayer.lift(b0)
videoplayer.lift(b1)
videoplayer.lift(b2)
videoplayer.lift(b3)
videoplayer.lift(b4)
videoplayer.lift(console_output1)
videoplayer.lift(console_output)
videoplayer.lift(Combo)

periodic_update()
window.protocol("WM_DELETE_WINDOW", kapatma_istegi)

list_serial_ports()










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
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 833, y = 292,
    width = 97,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 833, y = 177,
    width = 97,
    height = 29)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 789, y = 346,
    width = 199,
    height = 31)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 790, y = 392,
    width = 199,
    height = 31)

img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = web_baslat,
    relief = "flat")

b4.place(
    x = 90, y = 393,
    width = 165,
    height = 41)

lot = canvas.create_text(
    85.5, 139.0,
    text = "0.00000",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

lon = canvas.create_text(
    262.5, 139.0,
    text = "0.00000",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y1 = canvas.create_text(
    893.5, 147.0,
    text = "27.422222",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y2 = canvas.create_text(
    798.5, 262.0,
    text = "27.422222",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

tarih_L = canvas.create_text(
    1120.5, 40.0,
    text = "27:08:2006",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

saat_L = canvas.create_text(
    1120.5, 81.0,
    text = "22:05",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

yukseklik = canvas.create_text(
    246.0, 230.5,
    text = "38.63",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(24.0)))

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
Combo.place(x = 110, y = 340)


videoplayer = TkinterVideo(master=window, scaled=True)
videoplayer.load(r"hazirlik.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video
check_video_end()

videoplayer.lift(b0)
videoplayer.lift(b1)
videoplayer.lift(b2)
videoplayer.lift(b3)
videoplayer.lift(b4)
videoplayer.lift(console_output1)
videoplayer.lift(console_output)
videoplayer.lift(Combo)

periodic_update()
window.protocol("WM_DELETE_WINDOW", kapatma_istegi)

list_serial_ports()










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
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 833, y = 292,
    width = 97,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 833, y = 177,
    width = 97,
    height = 29)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 789, y = 346,
    width = 199,
    height = 31)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b3.place(
    x = 790, y = 392,
    width = 199,
    height = 31)

img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = web_baslat,
    relief = "flat")

b4.place(
    x = 90, y = 393,
    width = 165,
    height = 41)

lot = canvas.create_text(
    85.5, 139.0,
    text = "0.00000",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

lon = canvas.create_text(
    262.5, 139.0,
    text = "0.00000",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y1 = canvas.create_text(
    893.5, 147.0,
    text = "27.422222",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

port_Y2 = canvas.create_text(
    798.5, 262.0,
    text = "27.422222",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(16.0)))

tarih_L = canvas.create_text(
    1120.5, 40.0,
    text = "27:08:2006",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

saat_L = canvas.create_text(
    1120.5, 81.0,
    text = "22:05",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(15.0)))

yukseklik = canvas.create_text(
    246.0, 230.5,
    text = "38.63",
    fill = "#000000",
    font = ("InriaSerif-Regular", int(24.0)))
