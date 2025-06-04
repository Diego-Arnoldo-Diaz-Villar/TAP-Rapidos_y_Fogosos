import tkinter as tk
from tkinter import font, messagebox
import pygame
import subprocess
import sys
import os

pygame.mixer.init()

jugador_local = ""

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
    global jugador_local
    if not jugador_local:
        tk.messagebox.showwarning("Registro requerido", "Debes registrar tu nombre antes de jugar.")
        return
    ruta = os.path.join(os.path.dirname(__file__), "juego.py")
    subprocess.Popen([sys.executable, ruta, jugador_local])


def salir():
    root.destroy()

def opciones():
    ventana_opciones = tk.Toplevel(root)
    ventana_opciones.title("Opciones")
    ventana_opciones.geometry("400x400")
    ventana_opciones.configure(bg="#2b2b2b")
    ventana_opciones.resizable(False, False)

    subtitulo = tk.Label(ventana_opciones, text="Opciones del Juego", fg="white", bg="#2b2b2b", font=("Helvetica", 18, "bold"))
    subtitulo.pack(pady=20)

    def registrar_jugador():
        ventana_registro = tk.Toplevel(ventana_opciones)
        ventana_registro.title("Registrar Jugador")
        ventana_registro.geometry("400x250")
        ventana_registro.configure(bg="#1e1e1e")

        label = tk.Label(ventana_registro, text="Nombre del jugador:", fg="white", bg="#1e1e1e", font=("Helvetica", 12))
        label.pack(pady=(30, 5))
        entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        entry.pack(pady=5)

        def guardar_jugador():
            global jugador_local
            jugador_local = entry.get().strip() or "Jugador"
            print(f"Jugador registrado: {jugador_local}")
            ventana_registro.destroy()

        btn_guardar = tk.Button(ventana_registro, text="Guardar", command=guardar_jugador, **boton_style)
        btn_guardar.pack(pady=30)

    def ver_records():
        import sqlite3

        try:
            conn = sqlite3.connect("records.db")
            cursor = conn.cursor()
            cursor.execute("SELECT jugador, puntuacion, fecha FROM records ORDER BY puntuacion DESC LIMIT 10")

            resultados = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            tk.messagebox.showerror("Error", f"No se pudieron obtener los récords: {e}")
            return

        ventana_records = tk.Toplevel(ventana_opciones)
        ventana_records.title("Records")
        ventana_records.geometry("400x400")
        ventana_records.configure(bg="#1e1e1e")

        tk.Label(ventana_records, text="TOP 10 RECORDS", fg="white", bg="#1e1e1e", font=("Helvetica", 16, "bold")).pack(pady=10)

        for jugador, record, fecha in resultados:
            texto = f"{jugador}: {record} puntos ({fecha})"
            tk.Label(ventana_records, text=texto, fg="white", bg="#1e1e1e", font=("Helvetica", 12)).pack(anchor="w", padx=20)

    # Botones
    boton_registrar = tk.Button(ventana_opciones, text="Registrar Jugador", command=registrar_jugador, **boton_style)
    boton_registrar.pack(pady=20)

    boton_ver_records = tk.Button(ventana_opciones, text="Ver Records", command=ver_records, **boton_style)
    boton_ver_records.pack(pady=10)


btn_jugar = tk.Button(root, text="JUGAR", command=iniciar_juego, **boton_style)
btn_opciones = tk.Button(root, text="OPCIONES", command=opciones, **boton_style)
btn_salir = tk.Button(root, text="SALIR", command=salir, **boton_style)

btn_jugar.pack(pady=15)
btn_opciones.pack(pady=15)
btn_salir.pack(pady=15)

ruta_musica = os.path.join(os.path.dirname(__file__), "car-music-hip-hop-beat-street-racing-background-intro-theme-290635.mp3")
pygame.mixer.music.load(ruta_musica)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

root.mainloop()
