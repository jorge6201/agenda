class Cliente:
    def __init__(self, id, nombre, apellido, telefono, fecha_llamada, nota=""):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.fecha_llamada = fecha_llamada  # formato YYYY-MM-DD
        self.nota = nota

    def __str__(self):
        return f"[{self.id}] {self.nombre} {self.apellido} - Tel: {self.telefono} - Llamar: {self.fecha_llamada} - Nota: {self.nota}"
