from database import listar_clientes
import datetime

def clientes_para_llamar():
    hoy = datetime.date.today().isoformat()
    clientes = listar_clientes()
    return [c for c in clientes if c.fecha_llamada <= hoy]  # vencidos o igual a hoy

def mostrar_recordatorios():
    clientes = clientes_para_llamar()
    if not clientes:
        print("✅ No hay clientes pendientes de llamada hoy.")
    else:
        print("📞 Clientes para llamar hoy o vencidos:")
        for c in clientes:
            print("  ", c)
