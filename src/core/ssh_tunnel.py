"""
Módulo para manejar túneles SSH automáticamente
"""
import os
import subprocess
import time
import psutil
import socket
from typing import Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SSHTunnel:
    """Clase para manejar túneles SSH de forma automática"""

    def __init__(self,
                 ssh_host: str,
                 ssh_user: str,
                 local_port: int = 5432,
                 remote_host: str = "localhost",
                 remote_port: int = 5432,
                 ssh_key_path: Optional[str] = None):
        """
        Inicializar el túnel SSH

        Args:
            ssh_host: Host del servidor SSH (ej: 13.222.89.227)
            ssh_user: Usuario SSH
            local_port: Puerto local para el túnel (default: 5432)
            remote_host: Host remoto en el servidor (default: localhost)
            remote_port: Puerto remoto (default: 5432)
            ssh_key_path: Ruta a la clave SSH privada (opcional)
        """
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.ssh_key_path = ssh_key_path
        self.process: Optional[subprocess.Popen] = None
        self.pid_file = "ssh_tunnel.pid"

    def is_port_in_use(self, port: int) -> bool:
        """Verificar si un puerto está en uso"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def get_existing_tunnel_pid(self) -> Optional[int]:
        """Obtener PID de un túnel existente desde archivo"""
        try:
            if os.path.exists(self.pid_file):
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                    if psutil.pid_exists(pid):
                        return pid
                    else:
                        os.remove(self.pid_file)
        except (ValueError, FileNotFoundError, OSError):
            pass
        return None

    def kill_existing_tunnels(self):
        """Matar túneles SSH existentes en el puerto"""
        # Verificar PID guardado
        existing_pid = self.get_existing_tunnel_pid()
        if existing_pid:
            try:
                psutil.Process(existing_pid).terminate()
                logger.info(
                    f"Túnel SSH existente terminado (PID: {existing_pid})")
                time.sleep(1)
            except psutil.NoSuchProcess:
                pass

        # Buscar procesos SSH usando el puerto
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'ssh' and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if f"-L {self.local_port}:" in cmdline:
                        proc.terminate()
                        logger.info(
                            f"Proceso SSH terminado: {proc.info['pid']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Limpiar archivo PID
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def start_tunnel(self) -> bool:
        """
        Iniciar el túnel SSH

        Returns:
            bool: True si el túnel se inició correctamente
        """
        try:
            # Verificar si ya existe un túnel
            if self.is_port_in_use(self.local_port):
                logger.warning(f"Puerto {self.local_port} ya está en uso")
                existing_pid = self.get_existing_tunnel_pid()
                if existing_pid:
                    logger.info(f"Túnel SSH ya activo (PID: {existing_pid})")
                    return True
                else:
                    logger.info("Matando procesos existentes en el puerto...")
                    self.kill_existing_tunnels()
                    time.sleep(2)

            # Construir comando SSH
            ssh_cmd = [
                "ssh",
                "-N",  # No ejecutar comando remoto
                "-f",  # Ejecutar en background
                "-o", "StrictHostKeyChecking=no",  # No verificar host key
                "-o", "ServerAliveInterval=30",    # Keep alive
                "-o", "ServerAliveCountMax=3",     # Reintentos
                "-L", f"{self.local_port}:{self.remote_host}:{self.remote_port}",
            ]

            # Agregar clave SSH si se especifica
            if self.ssh_key_path and os.path.exists(self.ssh_key_path):
                ssh_cmd.extend(["-i", self.ssh_key_path])

            # Agregar usuario y host
            ssh_cmd.append(f"{self.ssh_user}@{self.ssh_host}")

            logger.info(f"Iniciando túnel SSH: {' '.join(ssh_cmd)}")

            # Ejecutar comando SSH
            self.process = subprocess.Popen(
                ssh_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Esperar un poco para que se establezca la conexión
            time.sleep(3)

            # Verificar si el túnel está funcionando
            if self.is_port_in_use(self.local_port):
                # Guardar PID
                with open(self.pid_file, 'w') as f:
                    f.write(str(self.process.pid))

                logger.info(
                    f"✅ Túnel SSH establecido exitosamente en puerto {self.local_port}")
                logger.info(f"PID del túnel: {self.process.pid}")
                return True
            else:
                logger.error("❌ Error: El túnel SSH no se pudo establecer")
                if self.process:
                    stdout, stderr = self.process.communicate()
                    if stderr:
                        logger.error(f"Error SSH: {stderr}")
                return False

        except Exception as e:
            logger.error(f"❌ Error iniciando túnel SSH: {e}")
            return False

    def stop_tunnel(self):
        """Detener el túnel SSH"""
        try:
            self.kill_existing_tunnels()
            logger.info("✅ Túnel SSH detenido")
        except Exception as e:
            logger.error(f"Error deteniendo túnel SSH: {e}")

    def status(self) -> Tuple[bool, Optional[int]]:
        """
        Verificar el estado del túnel

        Returns:
            Tuple[bool, Optional[int]]: (activo, pid)
        """
        pid = self.get_existing_tunnel_pid()
        active = self.is_port_in_use(self.local_port)
        return active, pid


def create_tunnel_from_env() -> Optional[SSHTunnel]:
    """Crear túnel SSH desde variables de entorno"""
    ssh_host = os.getenv("SSH_TUNNEL_REMOTE_HOST")
    ssh_user = os.getenv("REMOTE_SSH_USER", "root")
    local_port = int(os.getenv("SSH_TUNNEL_LOCAL_PORT", "5432"))
    remote_port = int(os.getenv("SSH_TUNNEL_REMOTE_PORT", "5432"))
    ssh_key_path = os.getenv("SSH_KEY_PATH")

    if not ssh_host:
        logger.warning("SSH_TUNNEL_REMOTE_HOST no configurado")
        return None

    return SSHTunnel(
        ssh_host=ssh_host,
        ssh_user=ssh_user,
        local_port=local_port,
        remote_port=remote_port,
        ssh_key_path=ssh_key_path
    )


if __name__ == "__main__":
    # Script para probar el túnel SSH
    import sys

    if len(sys.argv) < 2:
        print(
            "Uso: python ssh_tunnel.py <start|stop|status> [ssh_host] [ssh_user]")
        sys.exit(1)

    action = sys.argv[1]

    if action in ["start", "stop", "status"]:
        tunnel = create_tunnel_from_env()
        if not tunnel and len(sys.argv) >= 4:
            tunnel = SSHTunnel(sys.argv[2], sys.argv[3])

        if not tunnel:
            print(
                "❌ No se pudo crear el túnel. Configurar variables de entorno o usar argumentos.")
            sys.exit(1)

        if action == "start":
            success = tunnel.start_tunnel()
            sys.exit(0 if success else 1)
        elif action == "stop":
            tunnel.stop_tunnel()
        elif action == "status":
            active, pid = tunnel.status()
            if active:
                print(f"✅ Túnel activo (PID: {pid})")
            else:
                print("❌ Túnel no activo")
    else:
        print("Acción no válida. Usar: start, stop, o status")
        sys.exit(1)
