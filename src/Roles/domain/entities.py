"""
Entidad de dominio para Role con posibles reglas de negocio
"""


class Role:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def change_name(self, new_name: str):
        if not new_name or len(new_name.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")
        self.name = new_name

    def update_description(self, new_desc: str):
        self.description = new_desc.strip()

    def __repr__(self):
        return f"<Role id={self.id}, name='{self.name}'>"
