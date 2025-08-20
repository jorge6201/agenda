from models import Cliente
import database
import notifications
import datetime

def menu():
    while True:
        print("\n===== AGENDA DE CLIENTES =====")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Ver recordatorios")
        print("0. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            telefono = input("Teléfono: ")
            fecha_llamada = input("Fecha de llamada (YYYY-MM-DD): ")
            nota = input("Nota: ")
            cliente = Cliente(None, nombre, apellido, telefono, fecha_llamada, nota)
            database.agregar_cliente(cliente)
            print("✅ Cliente agregado con éxito.")

        elif opcion == "2":
            clientes = database.listar_clientes()
            for c in clientes:
                print(c)

        elif opcion == "3":
            id_cliente = int(input("ID del cliente a actualizar: "))
            nombre = input("Nuevo nombre: ")
            apellido = input("Nuevo apellido: ")
            telefono = input("Nuevo teléfono: ")
            fecha_llamada = input("Nueva fecha de llamada (YYYY-MM-DD): ")
            nota = input("Nueva nota: ")
            cliente = Cliente(id_cliente, nombre, apellido, telefono, fecha_llamada, nota)
            database.actualizar_cliente(cliente)
            print("✅ Cliente actualizado.")

        elif opcion == "4":
            id_cliente = int(input("ID del cliente a eliminar: "))
            database.eliminar_cliente(id_cliente)
            print("✅ Cliente eliminado.")

        elif opcion == "5":
            notifications.mostrar_recordatorios()

        elif opcion == "0":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    database.crear_tabla()
    menu()
