import socket
import threading
import sqlite3
import os

DB_PATH = "records.db"

def inicializar_bd():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador TEXT NOT NULL,
                puntuacion INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def guardar_record(nombre, puntuacion):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO records (jugador, puntuacion) VALUES (?, ?)", (nombre, int(puntuacion)))
            conn.commit()
        print(f"[RECORD GUARDADO] {nombre}: {puntuacion}")
    except Exception as e:
        print(f"[ERROR AL GUARDAR EN BD] {e}")

def manejar_cliente(cliente_socket, direccion):
    try:
        datos = cliente_socket.recv(1024).decode()
        if ":" in datos:
            nombre, puntuacion = datos.split(":")
            guardar_record(nombre.strip(), puntuacion.strip())
    except Exception as e:
        print(f"[ERROR CLIENTE] {e}")
    finally:
        cliente_socket.close()

def iniciar_servidor(host='0.0.0.0', puerto=5050):
    inicializar_bd()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen()
    print(f"[SERVIDOR ACTIVO] Esperando conexiones en {host}:{puerto}...")

    while True:
        cliente_socket, direccion = servidor.accept()
        print(f"[NUEVA CONEXIÓN] {direccion}")
        threading.Thread(target=manejar_cliente, args=(cliente_socket,)).start()

def manejar_cliente(cliente_socket):
    try:
        datos = cliente_socket.recv(1024).decode()
        if ":" in datos:
            nombre, puntuacion = datos.split(":")
            guardar_record(nombre, puntuacion)

            # Enviar los mejores 3 scores actuales
            top_scores = obtener_top_scores()
            respuesta = "\n".join([f"{jugador}: {puntos}" for jugador, puntos in top_scores])
            cliente_socket.sendall(respuesta.encode())
        cliente_socket.close()
    except Exception as e:
        print(f"[ERROR AL MANEJAR CLIENTE] {e}")
        cliente_socket.close()

def obtener_top_scores():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT jugador, MAX(puntuacion) 
                FROM records 
                GROUP BY jugador 
                ORDER BY MAX(puntuacion) DESC 
                LIMIT 3
            """)
            return cursor.fetchall()
    except Exception as e:
        print(f"[ERROR AL CONSULTAR TOP SCORES] {e}")
        return []


if __name__ == "__main__":
    iniciar_servidor()
