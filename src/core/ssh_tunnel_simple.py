"""
Módulo simplificado para túnel SSH
"""
import subprocess
import time
import os
import socket


def is_port_in_use(port: int) -> bool:
    """Verificar si un puerto está en uso (escuchando)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False  # Puerto libre
        except OSError:
            return True  # Puerto en uso


def start_ssh_tunnel(ssh_host: str, ssh_user: str, ssh_key_path: str = None, local_port: int = 5432, remote_port: int = 5432):
    """
    Iniciar túnel SSH simple

    Args:
        ssh_host: Host del servidor SSH (ej: 13.222.89.227)
        ssh_user: Usuario SSH
        ssh_key_path: Ruta a la clave SSH privada (opcional)
        local_port: Puerto local para el túnel (default: 5432)
        remote_port: Puerto remoto (default: 5432)

    Returns:
        bool: True si el túnel se inició correctamente
    """
    try:
        # Verificar si el puerto ya está en uso
        if is_port_in_use(local_port):
            print(f"⚠️ Puerto {local_port} ya está en uso")
            return True  # Asumimos que ya hay un túnel activo

        # Construir comando SSH
        ssh_cmd = [
            "ssh",
            "-N",  # No ejecutar comando remoto
            "-f",  # Ejecutar en background
            "-o", "StrictHostKeyChecking=no",
            "-o", "ServerAliveInterval=30",
            "-L", f"{local_port}:localhost:{remote_port}",
        ]

        # Agregar clave SSH si se proporciona
        if ssh_key_path:
            ssh_cmd.extend(["-i", ssh_key_path])

        # Agregar destino
        ssh_cmd.append(f"{ssh_user}@{ssh_host}")

        print(f"🔄 Iniciando túnel SSH: {ssh_user}@{ssh_host}")
        print(
            f"📍 Redirigiendo localhost:{local_port} -> {ssh_host}:{remote_port}")
        if ssh_key_path:
            print(f"🔑 Usando clave SSH: {ssh_key_path}")

        # Ejecutar comando SSH
        result = subprocess.run(
            ssh_cmd, capture_output=True, text=True, timeout=10)

        # Esperar un poco para que se establezca la conexión
        time.sleep(3)

        # Verificar si el túnel está funcionando
        if is_port_in_use(local_port):
            print(
                f"✅ Túnel SSH establecido exitosamente en puerto {local_port}")
            return True
        else:
            print(f"❌ Error: El túnel SSH no se pudo establecer")
            if result.stderr:
                print(f"Error SSH: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Timeout estableciendo túnel SSH - puede que haya funcionado")
        return is_port_in_use(local_port)
    except Exception as e:
        print(f"❌ Error iniciando túnel SSH: {e}")
        return False


def stop_ssh_tunnels():
    """Detener túneles SSH"""
    try:
        # En Windows, matar procesos ssh
        subprocess.run(["taskkill", "/f", "/im", "ssh.exe"],
                       capture_output=True, text=True)
        print("✅ Túneles SSH detenidos")
    except Exception as e:
        print(f"Error deteniendo túneles SSH: {e}")


def test_ssh_connection(ssh_host: str, ssh_user: str, ssh_key_path: str = None):
    """Probar conexión SSH"""
    try:
        cmd = ["ssh", "-o", "StrictHostKeyChecking=no",
               "-o", "ConnectTimeout=10"]

        # Agregar clave SSH si se proporciona
        if ssh_key_path:
            cmd.extend(["-i", ssh_key_path])

        cmd.extend([f"{ssh_user}@{ssh_host}", "echo 'Conexión SSH exitosa!'"])

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=15)

        if result.returncode == 0:
            print("✅ Conexión SSH exitosa")
            return True
        else:
            print("❌ Error en la conexión SSH")
            print(f"Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Error probando conexión SSH: {e}")
        return False


if __name__ == "__main__":
    # Script de prueba
    import sys

    if len(sys.argv) >= 2:
        action = sys.argv[1]

        if action == "start" and len(sys.argv) >= 4:
            ssh_host = sys.argv[2]
            ssh_user = sys.argv[3]
            ssh_key_path = sys.argv[4] if len(sys.argv) >= 5 else None
            success = start_ssh_tunnel(ssh_host, ssh_user, ssh_key_path)
            sys.exit(0 if success else 1)

        elif action == "test" and len(sys.argv) >= 4:
            ssh_host = sys.argv[2]
            ssh_user = sys.argv[3]
            ssh_key_path = sys.argv[4] if len(sys.argv) >= 5 else None
            success = test_ssh_connection(ssh_host, ssh_user, ssh_key_path)
            sys.exit(0 if success else 1)

        elif action == "stop":
            stop_ssh_tunnels()

        else:
            print(
                "Uso: python ssh_tunnel_simple.py <start|test|stop> [ssh_host] [ssh_user] [ssh_key_path]")
    else:
        # Usar variables de entorno
        ssh_host = os.getenv("SSH_TUNNEL_REMOTE_HOST", "13.222.89.227")
        ssh_user = os.getenv("REMOTE_SSH_USER", "ubuntu")
        ssh_key_path = os.getenv("SSH_KEY_PATH")

        print(f"Configuración desde .env:")
        print(f"SSH Host: {ssh_host}")
        print(f"SSH User: {ssh_user}")
        print(f"SSH Key: {ssh_key_path}")

        if ssh_host and ssh_user:
            start_ssh_tunnel(ssh_host, ssh_user, ssh_key_path)
        else:
            print("❌ Configurar SSH_TUNNEL_REMOTE_HOST y REMOTE_SSH_USER en .env")
