import threading
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import pygame
pygame.mixer.init()

jugador1 = ""
jugador2 = ""

root = tk.Tk()
root.title("RÁPIDO Y FOGOSO")
root.geometry("800x600")
root.configure(bg="#1a1a1a")
root.resizable(False, False)

titulo_fuente = font.Font(family="Impact", size=40, weight="bold")
boton_fuente = font.Font(family="Helvetica", size=14, weight="bold")

titulo = tk.Label(root, text="RÁPIDO Y FOGOSO", fg="white", bg="#1a1a1a", font=titulo_fuente)
titulo.pack(pady=60)

boton_style = {
    "width": 20,
    "height": 2,
    "bg": "#e60000",
    "fg": "white",
    "activebackground": "#990000",
    "font": boton_fuente,
    "bd": 0,
    "highlightthickness": 0
}

def iniciar_juego():
    import crash_car_corregido
    threading.Thread(target=crash_car_corregido.iniciar_juego).start()

def salir():
    root.destroy()

def opciones():
    ventana_opciones = tk.Toplevel(root)
    ventana_opciones.title("Opciones")
    ventana_opciones.geometry("400x300")
    ventana_opciones.configure(bg="#2b2b2b")
    ventana_opciones.resizable(False, False)

    subtitulo = tk.Label(ventana_opciones, text="Opciones del Juego", fg="white", bg="#2b2b2b", font=("Helvetica", 18, "bold"))
    subtitulo.pack(pady=20)

    def registrar_jugadores():
        ventana_registro = tk.Toplevel(ventana_opciones)
        ventana_registro.title("Registrar Jugadores")
        ventana_registro.geometry("400x300")
        ventana_registro.configure(bg="#1e1e1e")

        label1 = tk.Label(ventana_registro, text="Jugador 1:", fg="white", bg="#1e1e1e", font=("Helvetica", 12))
        label1.pack(pady=(20, 5))
        entry1 = tk.Entry(ventana_registro, font=("Helvetica", 12))
        entry1.pack(pady=5)

        label2 = tk.Label(ventana_registro, text="Jugador 2:", fg="white", bg="#1e1e1e", font=("Helvetica", 12))
        label2.pack(pady=(20, 5))
        entry2 = tk.Entry(ventana_registro, font=("Helvetica", 12))
        entry2.pack(pady=5)

        def guardar_jugadores():
            global jugador1, jugador2
            jugador1 = entry1.get() if entry1.get() else "Jugador 1"
            jugador2 = entry2.get() if entry2.get() else "Jugador 2"
            print(f"Jugador 1: {jugador1}")
            print(f"Jugador 2: {jugador2}")
            ventana_registro.destroy()

        btn_guardar = tk.Button(ventana_registro, text="Guardar", command=guardar_jugadores, **boton_style)
        btn_guardar.pack(pady=30)

    def ver_records():
        ventana_records = tk.Toplevel(ventana_opciones)
        ventana_records.title("Records de Jugadores")
        ventana_records.geometry("400x300")
        ventana_records.configure(bg="#1e1e1e")
        ventana_records.resizable(False, False)

        titulo_records = tk.Label(
            ventana_records,
            text="🏁 RECORDS DE JUGADORES 🏁",
            fg="white",
            bg="#1e1e1e",
            font=("Helvetica", 16, "bold")
        )
        titulo_records.pack(pady=20)

        frame_contenedor = tk.Frame(ventana_records, bg="#2d2d2d", bd=2, relief="groove")
        frame_contenedor.pack(padx=40, pady=10, fill="both", expand=True)

        jugador1_nombre = jugador1 if jugador1 else "Jugador 1"
        jugador2_nombre = jugador2 if jugador2 else "Jugador 2"

        label_j1 = tk.Label(
            frame_contenedor,
            text=f"{jugador1_nombre}",
            fg="white",
            bg="#2d2d2d",
            anchor="w",
            font=("Helvetica", 14, "bold")
        )
        label_p1 = tk.Label(
            frame_contenedor,
            text="Puntos: 0",
            fg="white",
            bg="#2d2d2d",
            anchor="e",
            font=("Helvetica", 14)
        )

        label_j2 = tk.Label(
            frame_contenedor,
            text=f"{jugador2_nombre}",
            fg="white",
            bg="#2d2d2d",
            anchor="w",
            font=("Helvetica", 14, "bold")
        )
        label_p2 = tk.Label(
            frame_contenedor,
            text="Puntos: 0",
            fg="white",
            bg="#2d2d2d",
            anchor="e",
            font=("Helvetica", 14)
        )

        label_j1.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        label_p1.grid(row=0, column=1, sticky="e", padx=20)

        label_j2.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        label_p2.grid(row=1, column=1, sticky="e", padx=20)

    boton_registrar = tk.Button(ventana_opciones, text="Registrar Jugadores", command=registrar_jugadores, **boton_style)
    boton_records = tk.Button(ventana_opciones, text="Ver Records", command=ver_records, **boton_style)

    boton_registrar.pack(pady=10)
    boton_records.pack(pady=10)

btn_jugar = tk.Button(root, text="JUGAR", command=iniciar_juego, **boton_style)
btn_opciones = tk.Button(root, text="OPCIONES", command=opciones, **boton_style)
btn_salir = tk.Button(root, text="SALIR", command=salir, **boton_style)

btn_jugar.pack(pady=15)
btn_opciones.pack(pady=15)
btn_salir.pack(pady=15)

# Cargar la música solo una vez
pygame.mixer.music.load("car-music-hip-hop-beat-street-racing-background-intro-theme-290635.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

root.mainloop()
