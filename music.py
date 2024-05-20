from tkinter import *
from PIL import ImageTk, Image
import os
from pygame import mixer
from Tooltip import Tooltip
from tkinter import Tk
from mutagen.mp3 import MP3
import pygame.mixer as mx
from tkinter import ttk
import time

class MusicPlayer():

    mixer.init()

    def play_music(self, event=None):
        running = self.listbox.get(ACTIVE)
        self.running_song['text'] =  running 
        self.duracion_cancion(running)
        mixer.music.load(running)
        mixer.music.play()
        song = MP3(running) 
        total_length = song.info.length
        self.progreso_barra.config(maximum=total_length)
        self.continuar[0] = True
        self.guardar_progreso()


    def pause_music(self, event=None):
        if not self.aPaused:
            mixer.music.pause()
            self.aPaused = True
        else:
            mixer.music.unpause()
            self.aPaused = False
            if not self.aPaused:
                self.actualizar_tiempo_reproduccion()
                self.progreso_avance()

                
    def stop_music(self, event=None):
        mixer.music.stop()  
        self.progreso_barra['value'] = 0  
        self.lblTiempoReproduccion.config(text="00:00 /")
        self.actualizar_tiempo_reproduccion()  
      

    def rewind_music(self, event=None):
        if mixer.music.get_busy():
            mixer.music.pause()
            tiempo_reproduccion = 0
            if self.continuar[0] == True:
                tiempo_reproduccion = mixer.music.get_pos() / 1000
                
            else:
                tiempo_reproduccion = self.progreso_barra['value']

            new_pos = max(0, tiempo_reproduccion - 10)
            
            mixer.music.set_pos(new_pos)

            mixer.music.unpause()

            self.progreso_barra['value'] = new_pos

            tiempo_actual_formateado = self.convertir_segundos_a_formato_tiempo(new_pos)
            self.lblTiempoReproduccion.config(text=tiempo_actual_formateado + " /")

    def forward_music(self, event=None):
        if mixer.music.get_busy():
            mixer.music.pause()
            tiempo_reproduccion = 0
            if self.continuar[0] == True:
                tiempo_reproduccion = mixer.music.get_pos() / 1000
                
            else:
                tiempo_reproduccion = self.progreso_barra['value']

            new_pos = max(0, tiempo_reproduccion + 10)
            
            mixer.music.set_pos(new_pos)

            mixer.music.unpause()

            self.progreso_barra['value'] = new_pos

            tiempo_actual_formateado = self.convertir_segundos_a_formato_tiempo(new_pos)
            self.lblTiempoReproduccion.config(text=tiempo_actual_formateado + " /")

    def next_music(self, event=None):
        playing = self.running_song['text']
        index = self.songs.index(playing)
        new_index = (index + 1) % len(self.songs) 
        playing = self.songs[new_index]
        
        mixer.music.load(playing)
        mixer.music.play()

        self.listbox.delete(0, END)
        self.show()
        self.listbox.select_set(new_index)
        
        self.running_song['text'] = playing

       
        self.lblTiempoReproduccion.config(text="00:00 /")
        self.progreso_barra['value'] = 0

        self.duracion_cancion(playing) 
        self.continuar[0] = True
        self.guardar_progreso()

        self.actualizar_tiempo_reproduccion()


    def previous_music(self, event=None):
        playing = self.running_song['text']
        index = self.songs.index(playing)
        new_index = index - 1
        playing = self.songs[new_index]
        mixer.music.load(playing)
        mixer.music.play()

        self.listbox.delete(0, END)

        self.show()

        self.listbox.select_set(new_index)
        self.running_song['text'] = playing

        self.lblTiempoReproduccion.config(text="00:00 /")
        self.progreso_barra['value'] = 0

        self.duracion_cancion(playing)  
        self.continuar[0] = True
        self.guardar_progreso()

        self.actualizar_tiempo_reproduccion()

    def show(self):
        for i in self.songs:
            self.listbox.insert(END, i)

    def update_volume(self, event):
        volume = self.volume_slider.get() / 100.0

        self.set_volume(volume)

    def set_volume(self, volume):
        mixer.music.set_volume(volume)



    def duracion_cancion(self, cancion):
        ruta_cancion = cancion 
        audio_info = MP3(ruta_cancion)
        duracion_total = audio_info.info.length
        duracion_formateada = self.convertir_segundos_a_formato_tiempo(duracion_total)
        
        self.lblDuracioncancion.config(text= duracion_formateada) 
        
    def actualizar_tiempo(self):
        ahora = time.time()
        duracion = int(ahora - self.inicio)
        horas = duracion // 3600
        minutos = (duracion % 3600) // 60
        segundos = duracion % 60
        self.lbltiempo.config(text=f"{horas:02}:{minutos:02}:{segundos:02}")
        self.ventana.after(1000, self.actualizar_tiempo)
        
    def actualizar_tiempo_reproduccion(self):
        if mixer.music.get_busy():
            if self.continuar[0] == True:
                tiempo_reproduccion = mixer.music.get_pos() / 1000
            else:
                tiempo_reproduccion = self.progreso_barra['value']
            tiempo_actual_formateado = self.convertir_segundos_a_formato_tiempo(tiempo_reproduccion)
            self.lblTiempoReproduccion.config(text=tiempo_actual_formateado + " /")
        self.ventana.after(100, self.actualizar_tiempo_reproduccion)
    
    def convertir_segundos_a_formato_tiempo(self, segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return "{:02}:{:02}".format(minutos, segundos)

    def guardar_progreso(self):
        if self.continuar[0] and not self.aPaused:
            if mixer.music.get_busy():
                current_position = mixer.music.get_pos() / 1000
                self.progreso_barra['value'] = current_position
                self.progreso_barra.after(100, self.guardar_progreso)
            else:
                self.progreso_avance()

    def progreso_avance(self):
        if self.continuar[0] == False:
            if mixer.music.get_busy():
                new_value = self.progreso_barra['value'] + 0.1
                if new_value <= self.progreso_barra['maximum']:
                    self.progreso_barra['value'] = new_value
                self.progreso_barra.after(100, self.progreso_avance)

    def progreso_barra_click(self, event):
        progress_length = self.progreso_barra.winfo_width()
        click_x = event.x
        nueva_posicion = (click_x / progress_length) * self.progreso_barra["maximum"]
        mixer.music.stop()
        mixer.music.play(start=nueva_posicion)
        self.progreso_barra['value'] = nueva_posicion
        self.continuar[0] = False
        self.progreso_avance()
        self.actualizar_tiempo_reproduccion()

    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("REPRODUCTOR DE MÚSICA")
        self.ventana.geometry('450x300')
        self.ventana.configure(background = "#ffffff")
        self.ventana.resizable(width = FALSE, height = FALSE)

        # COLORES
        self.Color1 = "#ffffff"  #Blanco
        self.Color2 = "#3C1DC6" #Morado
        self.Color3 = "#333333" #Negro
        self.Color4 = "#FFC0CB" #Lila

        # EVENTS
        self.aPaused = False
        self.total_length = 0
        self.is_playing= False
        self.inicio = time.time()
        self.continuar = [False]

        # FRAMES
        self.left_frame = Frame(self.ventana, width = 150, height = 150, bg = self.Color1)
        self.left_frame.grid (row = 0, column = 0, padx = 1, pady = 1)

        self.right_frame = Frame(self.ventana, width = 300, height = 200, bg = self.Color3)
        self.right_frame.grid (row = 0, column = 2, padx = 0)

        self.down_frame = Frame(self.ventana, width = 450, height = 300, bg = self.Color4)
        self.down_frame.grid (row = 1, column = 0, columnspan = 3, padx = 0, pady = 1)

        # RIGHT FRAME 
        self.listbox = Listbox(self.right_frame, selectmode = SINGLE, font = "Arial 9 bold", width = 22, bg = self.Color3, fg = self.Color1)
        self.listbox.grid(row = 0, column = 0)

        self.w = Scrollbar(self.right_frame)
        self.w.grid(row = 0, column = 1)

        self.listbox.config(yscrollcommand =self.w.set)
        self.w.config(command = self.listbox.yview)

        # IMAGENES
        self.img_1 = Image.open(r"MUSICPLAYER\Iconos\1.png")
        self.img_1 = self.img_1.resize((130, 130))
        self.img_1 = ImageTk.PhotoImage(self.img_1)
        self.app_image = Label(self.left_frame, height = 140, image = self.img_1, padx = 10, bg = self.Color1)
        self.app_image.place(x = 8, y = 10)

        self.img_2 = Image.open(r"MUSICPLAYER\Iconos\2.png")
        self.img_2 = self.img_2.resize((30, 30))
        self.img_2 = ImageTk.PhotoImage(self.img_2)
        self.play_button = Button(self.down_frame, width = 40, height = 40, image = self.img_2, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.play_music)
        self.play_button.place(x = 56 + 8, y = 80)
        Tooltip(self.play_button, text = "Presione para iniciar la reproducción.\nAlt+r")
        self.ventana.bind('<Alt-r>', self.play_music)

        self.img_3 = Image.open(r"MUSICPLAYER\Iconos\3.png")
        self.img_3 = self.img_3.resize((30, 30))
        self.img_3 = ImageTk.PhotoImage(self.img_3)
        self.prev_button = Button(self.down_frame, width = 40, height = 40, image = self.img_3, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.previous_music)
        self.prev_button.place(x = 10 + 8, y = 80)
        Tooltip(self.prev_button, text = "Presione para reproducir la canción anterior. \nAlt+b")
        self.ventana.bind('Alt-b', self.previous_music)

        self.img_4 = Image.open(r"MUSICPLAYER\Iconos\4.png")
        self.img_4 = self.img_4.resize((30, 30))
        self.img_4 = ImageTk.PhotoImage(self.img_4)
        self.next_button = Button(self.down_frame, width = 40, height = 40, image = self.img_4, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.next_music)
        self.next_button.place(x = 102 + 8, y = 80)
        Tooltip(self.next_button, text = "Presione para reprdoucir la siguiente canción. \Alt+n")
        self.ventana.bind('<Alt-n>', self.next_music)

        self.img_5 = Image.open(r"MUSICPLAYER\Iconos\5.png")
        self.img_5 = self.img_5.resize((30, 30))
        self.img_5 = ImageTk.PhotoImage(self.img_5)
        self.pause_button = Button(self.down_frame, width = 40, height = 40, image = self.img_5, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.pause_music)
        self.pause_button.place(x = 148 + 8, y = 80)
        Tooltip(self.pause_button, text = "Presione para pausar la canción. \Alt+p")
        self.ventana.bind('<Alt-p>', self.pause_music)

        self.img_6 = Image.open(r"MUSICPLAYER\Iconos\6.png")
        self.img_6 = self.img_6.resize((30, 30))
        self.img_6 = ImageTk.PhotoImage(self.img_6)
        self.stop_button = Button(self.down_frame, width = 40, height = 40, image = self.img_6, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.stop_music)
        self.stop_button.place(x = 194 + 8, y = 80)
        Tooltip(self.stop_button, text = "Presione para detener la cancion. \Alt+s")
        self.ventana.bind('<Alt-s>', self.stop_music)

        self.img_7 = Image.open(r"MUSICPLAYER\Iconos\7.png") 
        self.img_7 = self.img_7.resize((30, 30))
        self.img_7 = ImageTk.PhotoImage(self.img_7)
        self.rewind_button = Button(self.down_frame, width = 40, height = 40, image = self.img_7, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.rewind_music)
        self.rewind_button.place(x = 240 + 8, y = 80)
        Tooltip(self.rewind_button, text = "Presione para retroceder 10 segundos la cancion. \Alt+d")
        self.ventana.bind('<Alt-d>', self.rewind_music)

        self.img_8 = Image.open(r"MUSICPLAYER\Iconos\8.png") 
        self.img_8 = self.img_8.resize((30, 30))
        self.img_8 = ImageTk.PhotoImage(self.img_8)
        self.forward_button = Button(self.down_frame, width = 40, height = 40, image = self.img_8, padx = 10, bg = self.Color1, font =("Ivy 10"), command=self.forward_music)
        self.forward_button.place(x = 286 + 8, y = 80)
        Tooltip(self.forward_button, text = "Presione para adelantar 10 segundos la cancion. \Alt+f")
        self.ventana.bind('<Alt-f>', self.forward_music)

        self.running_song = Label(self.down_frame, text = "Elige una canción", font = ("Helvetica", 12), width = 60, height = 1, padx = 10, bg = self.Color1, fg= self.Color3, anchor = NW)
        self.running_song.place(x = 0, y = 1)

        self.volume_slider = Scale(self.ventana, from_=0, to=100, orient=HORIZONTAL, command=self.update_volume,  length=110, sliderlength=15, troughcolor="green", borderwidth=1)
        self.volume_slider.set(50)
        self.volume_slider.place(relx=1, rely=0.90, anchor="e", width=110)
        Tooltip(self.volume_slider, "Ajusta el volumen")


        self.lblTiempoReproduccion = Label(self.ventana, text="00:00 /", font=("Helvetica", 12))
        self.lblTiempoReproduccion.place(relx=0.5, rely=0.75, anchor="center")
        Tooltip(self.lblTiempoReproduccion, "Tiempo de reproducción actual")

        self.lblDuracioncancion = Label(self.ventana, text="00:00 ", font=("Helvetica", 12))
        self.lblDuracioncancion.place(relx=0.61, rely=0.75, anchor="center")
        Tooltip(self.lblDuracioncancion, "Duración total de la canción")

        self.progreso_barra = ttk.Progressbar(self.ventana, orient="horizontal", length=0, mode="determinate")
        self.progreso_barra.place(relx=0.5, rely=0.67, anchor="center", width=450)
        self.progreso_barra.bind("<Button-1>", self.progreso_barra_click)
        Tooltip(self.progreso_barra, "Dale click para adelantar la canción")

        self.progreso_avance()
        self.actualizar_tiempo_reproduccion()

        self.lbltiempo = Label(self.ventana, text="00:00:00", font=("Helvetica", 12))
        self.lbltiempo.place(relx=0.10, rely=0.07, anchor="center")
        self.actualizar_tiempo()

        os.chdir(r'MUSICPLAYER\Canciones')
        self.songs = os.listdir()

        self.show()

        self.music_state = StringVar()
        self.music_state.set("Choose One!")

        self.ventana.mainloop()