
import sqlite3
from models import Cliente

from datetime import datetime

DB_NAME = "clientes.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    return conn

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            fecha_llamada DATE,
            nota TEXT
        )
    """)
    conn.commit()
    conn.close()

def agregar_cliente(cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nombre, apellido, telefono, fecha_llamada, nota)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente.nombre, cliente.apellido, cliente.telefono, cliente.fecha_llamada, cliente.nota))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    filas = cursor.fetchall()
    conn.close()
    return [Cliente(*fila) for fila in filas]

def actualizar_cliente(cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nombre=?, apellido=?, telefono=?, fecha_llamada=?, nota=?
        WHERE id=?
    """, (cliente.nombre, cliente.apellido, cliente.telefono, cliente.fecha_llamada, cliente.nota, cliente.id))
    conn.commit()
    conn.close()

def eliminar_cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
    conn.commit()
    conn.close()


def buscar_clientes(filtro):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM clientes
        WHERE telefono LIKE ? OR nombre LIKE ? OR apellido LIKE ?
    """, (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"))
    filas = cursor.fetchall()
    conn.close()
    return [Cliente(*fila) for fila in filas]




#CRUD tabla_notas
def crear_tabla_notas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            texto TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clientes(id)
        )
    """)
    conn.commit()
    conn.close()
    
    
    


def agregar_nota(cliente_id, texto):
    conn = conectar()
    cursor = conn.cursor()
    # Guardar hora local en lugar de UTC
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO notas (cliente_id, fecha, texto) VALUES (?, ?, ?)", (cliente_id, fecha, texto))
    conn.commit()
    conn.close()


def obtener_notas(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, texto FROM notas WHERE cliente_id=? ORDER BY fecha DESC", (cliente_id,))
    filas = cursor.fetchall()
    conn.close()
    return filas  # lista de tuplas (id, fecha, texto)

def obtener_ultima_nota(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT texto FROM notas WHERE cliente_id=? ORDER BY fecha DESC LIMIT 1", (cliente_id,))
    fila = cursor.fetchone()
    conn.close()
    return fila[0] if fila else ""
