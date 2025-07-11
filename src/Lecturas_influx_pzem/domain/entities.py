from datetime import datetime

class LecturaPZEM:
    """Entidad de dominio para una lectura del PZEM."""
    def __init__(
        self,
        time: datetime,
        deviceId: str,
        mac: str,
        voltage: float,
        current: float,
        power: float,
        energy: float,
        frequency: float,
        powerFactor: float
    ):
        self.time = time
        self.deviceId = deviceId
        self.mac = mac
        self.voltage = voltage
        self.current = current
        self.power = power
        self.energy = energy
        self.frequency = frequency
        self.powerFactor = powerFactor