"""
Domain entity for DeviceType with possible business rules
"""


class DeviceType:
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

    def change_name(self, new_name: str):
        if not new_name or len(new_name.strip()) < 3:
            raise ValueError("Name must have at least 3 characters.")
        self.name = new_name

    def update_description(self, new_desc: str):
        self.description = new_desc.strip()

    def __repr__(self):
        return f"<DeviceType id={self.id}, name='{self.name}'>"
