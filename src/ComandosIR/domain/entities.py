"""
Domain entity for DeviceCommand with business rules
"""


class DeviceCommand:
    def __init__(self, id: int, device_id: int, name: str, description: str, command: str):
        self.id = id
        self.device_id = device_id
        self.name = name
        self.description = description
        self.command = command

    def change_name(self, new_name: str):
        if not new_name or len(new_name.strip()) < 3:
            raise ValueError("Name must have at least 3 characters.")
        self.name = new_name

    def update_description(self, new_desc: str):
        self.description = new_desc.strip()

    def update_command(self, new_command: str):
        if not new_command or len(new_command.strip()) < 1:
            raise ValueError("Command cannot be empty.")
        self.command = new_command.strip()

    def assign_device(self, new_device_id: int):
        if new_device_id <= 0:
            raise ValueError("Device ID must be a positive number.")
        self.device_id = new_device_id

    def __repr__(self):
        return f"<DeviceCommand(id={self.id}, name='{self.name}', device_id={self.device_id})>"

    def __repr__(self):
        return f"<ComandoIR id={self.id_comando}, nombre='{self.nombre}', sensor={self.id_sensor}>"
