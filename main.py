import tkinter as tk
from tkinter import ttk, messagebox
from models import Cliente
import database
import notifications

from tkcalendar import DateEntry


# ==============================
# Ventana de formulario cliente
# ==============================
def formulario_cliente(root, cliente=None, callback=None):
    win = tk.Toplevel(root)
    win.title("Editar Cliente")
    win.geometry("700x400")

    frame_left = ttk.Frame(win)
    frame_left.pack(side="left", fill="y", padx=10, pady=10)

    frame_right = ttk.Frame(win)
    frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # --- Datos básicos ---
    nombre_var = tk.StringVar(value=cliente.nombre if cliente else "")
    apellido_var = tk.StringVar(value=cliente.apellido if cliente else "")
    telefono_var = tk.StringVar(value=cliente.telefono if cliente else "")
    fecha_var = tk.StringVar(value=cliente.fecha_llamada if cliente else "")

    ttk.Label(frame_left, text="Nombre:").pack(anchor="w")
    ttk.Entry(frame_left, textvariable=nombre_var).pack(fill="x")

    ttk.Label(frame_left, text="Apellido:").pack(anchor="w")
    ttk.Entry(frame_left, textvariable=apellido_var).pack(fill="x")

    ttk.Label(frame_left, text="Teléfono:").pack(anchor="w")
    ttk.Entry(frame_left, textvariable=telefono_var).pack(fill="x")

    ttk.Label(frame_left, text="Fecha llamada:").pack(anchor="w")
    fecha_entry = DateEntry(frame_left, textvariable=fecha_var, date_pattern="yyyy-mm-dd")
    fecha_entry.pack(fill="x")

    # --- Notas ---
    ttk.Label(frame_right, text="Historial de Notas:").pack(anchor="w")



#------------------


    # Caja de texto con scroll
    text_frame = ttk.Frame(frame_right)
    text_frame.pack(fill="both", expand=True)

    notas_text = tk.Text(text_frame, wrap="word", height=15)
    notas_text.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(text_frame, orient="vertical", command=notas_text.yview)
    scroll.pack(side="right", fill="y")

    notas_text.config(yscrollcommand=scroll.set)

    # Cargar notas en el TextBox
    def cargar_notas():
        notas_text.delete("1.0", "end")
        if cliente:
            notas = database.obtener_notas(cliente.id)
            for n in notas:
                notas_text.insert("end", f"{n[1]} - {n[2]}\n")

    cargar_notas()

    nueva_nota_var = tk.StringVar()
    ttk.Entry(frame_right, textvariable=nueva_nota_var).pack(fill="x", pady=5)

    def guardar_nota():
        if cliente and nueva_nota_var.get().strip():
            database.agregar_nota(cliente.id, nueva_nota_var.get().strip())
            nueva_nota_var.set("")
            cargar_notas()
            if callback: callback()

    ttk.Button(frame_right, text="Agregar Nota", command=guardar_nota).pack()


#---------------------


    # --- Guardar cliente ---
    def guardar_cliente():
        if not nombre_var.get() or not apellido_var.get():
            messagebox.showerror("Error", "Nombre y Apellido son obligatorios")
            return
        if cliente:  # actualización
            cliente.nombre = nombre_var.get()
            cliente.apellido = apellido_var.get()
            cliente.telefono = telefono_var.get()
            cliente.fecha_llamada = fecha_var.get()
            database.actualizar_cliente(cliente)
        else:  # nuevo
            nuevo = Cliente(None, nombre_var.get(), apellido_var.get(), telefono_var.get(),
                            fecha_var.get(), "")
            database.agregar_cliente(nuevo)
        if callback: callback()
        win.destroy()

    ttk.Button(frame_left, text="Guardar Cliente", command=guardar_cliente).pack(pady=10)



# ==============================
# Ventana principal
# ==============================
def main():
    database.crear_tabla()
    
    database.crear_tabla()
    database.crear_tabla_notas()

    root = tk.Tk()
    root.title("Agenda de Clientes")
    root.geometry("700x400")

    # Tabla
    tree = ttk.Treeview(root, columns=("Nombre", "Apellido", "Teléfono", "Fecha", "Nota"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Teléfono", text="Teléfono")
    tree.heading("Fecha", text="Fecha Llamada")
    tree.heading("Nota", text="Nota")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    
        # Función para editar al hacer doble click
    def editar_doble_click(event):
        seleccion = tree.selection()
        if not seleccion:
            return
        cliente_id = int(seleccion[0])
        clientes = database.listar_clientes()
        cliente = next((c for c in clientes if c.id == cliente_id), None)
        if cliente:
            formulario_cliente(root, cliente, callback=cargar_clientes)

    # Asociar doble click al Treeview
    tree.bind("<Double-1>", editar_doble_click)
    tree.bind("<Return>", editar_doble_click)


    # Función para recargar clientes en la tabla
    def cargar_clientes():
        for row in tree.get_children():
            tree.delete(row)
        clientes = database.listar_clientes()
        
        #for c in clientes:
            #tree.insert("", "end", iid=c.id, values=(c.nombre, c.apellido, c.telefono, c.fecha_llamada, c.nota))

        for c in clientes:
            ultima_nota = database.obtener_ultima_nota(c.id)
            tree.insert("", "end", iid=c.id,
                    values=(c.nombre, c.apellido, c.telefono, c.fecha_llamada, ultima_nota))


    cargar_clientes()

    # Botones
    frame_btn = ttk.Frame(root)
    frame_btn.pack(fill="x", pady=5)

    def agregar():
        formulario_cliente(root, callback=cargar_clientes)

    def editar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente para editar.")
            return
        cliente_id = int(seleccion[0])
        clientes = database.listar_clientes()
        cliente = next((c for c in clientes if c.id == cliente_id), None)
        if cliente:
            formulario_cliente(root, cliente, callback=cargar_clientes)

    def eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente para eliminar.")
            return
        cliente_id = int(seleccion[0])
        confirm = messagebox.askyesno("Confirmar", "¿Eliminar este cliente?")
        if confirm:
            database.eliminar_cliente(cliente_id)
            cargar_clientes()
            
            
    # Campo de búsqueda
    search_var = tk.StringVar()
    entry_buscar = ttk.Entry(frame_btn, textvariable=search_var, width=20)
    entry_buscar.pack(side="left", padx=5)

    def buscar(event=None):  # <-- añadimos event=None para que funcione tanto con botón como con <Return>
        filtro = search_var.get().strip()
        if not filtro:
            # Si el campo está vacío, recargar todos los clientes
            cargar_clientes()
            return
        clientes = database.buscar_clientes(filtro)
        for row in tree.get_children():
            tree.delete(row)
        for c in clientes:
            tree.insert("", "end", iid=c.id, values=(c.nombre, c.apellido, c.telefono, c.fecha_llamada, c.nota))

    # Botón buscar
    ttk.Button(frame_btn, text="Buscar", command=buscar).pack(side="left", padx=5)

    # Vincular tecla <Return> al campo de búsqueda
    entry_buscar.bind("<Return>", buscar)



    def ver_recordatorios():
        clientes = notifications.clientes_para_llamar()
        if not clientes:
            messagebox.showinfo("Recordatorios", "No hay clientes pendientes de llamada hoy.")
        else:
            texto = "\n".join([f"{c.nombre} {c.apellido} ({c.telefono}) - {c.fecha_llamada}" for c in clientes])
            messagebox.showinfo("Clientes para llamar", texto)

    ttk.Button(frame_btn, text="Agregar", command=agregar).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Editar", command=editar).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Eliminar", command=eliminar).pack(side="left", padx=5)
    ttk.Button(frame_btn, text="Ver Recordatorios", command=ver_recordatorios).pack(side="left", padx=5)

    # Mostrar notificaciones al inicio
    pendientes = notifications.clientes_para_llamar()
    if pendientes:
        texto = "\n".join([f"{c.nombre} {c.apellido} ({c.telefono}) - {c.fecha_llamada}" for c in pendientes])
        messagebox.showinfo("Aviso inicial", f"Clientes pendientes:\n\n{texto}")

   
    root.mainloop()


if __name__ == "__main__":
    main()
