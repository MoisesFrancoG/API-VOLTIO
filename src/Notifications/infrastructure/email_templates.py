"""
Servicio de templates dinámicos para emails de notificaciones
"""

from typing import Dict, Tuple


class EmailTemplateService:
    """
    Servicio para generar templates HTML dinámicos según el tipo de alerta
    """

    @staticmethod
    def get_alert_config(error_type: str) -> Dict[str, str]:
        """
        Obtiene la configuración específica para cada tipo de alerta
        """
        configs = {
            "TIMEOUT": {
                "emoji": "⏰",
                "title": "Dispositivo Sin Respuesta",
                "color": "#FF6B35",  # Naranja
                "urgency": "Media",
                "icon_bg": "#FFF3E0",
                "actions": [
                    "Verifica que el dispositivo esté encendido",
                    "Revisa la conexión Wi-Fi del dispositivo",
                    "Asegúrate de que no haya interferencias en la red",
                    "Reinicia el dispositivo si es necesario"
                ]
            },
            "OFFLINE": {
                "emoji": "🔴",
                "title": "Dispositivo Desconectado",
                "color": "#E74C3C",  # Rojo
                "urgency": "Alta",
                "icon_bg": "#FFEBEE",
                "actions": [
                    "Verifica que el dispositivo tenga energía",
                    "Revisa el cable de alimentación",
                    "Comprueba la conexión a internet",
                    "Contacta soporte si el problema persiste"
                ]
            },
            "ERROR": {
                "emoji": "⚠️",
                "title": "Error en Dispositivo",
                "color": "#F39C12",  # Amarillo/Naranja
                "urgency": "Alta",
                "icon_bg": "#FFF8E1",
                "actions": [
                    "Revisa los logs del dispositivo",
                    "Verifica que no haya errores de hardware",
                    "Reinicia el dispositivo",
                    "Contacta soporte técnico inmediatamente"
                ]
            },
            "WARNING": {
                "emoji": "⚠️",
                "title": "Advertencia del Sistema",
                "color": "#3498DB",  # Azul
                "urgency": "Baja",
                "icon_bg": "#E3F2FD",
                "actions": [
                    "Revisa la configuración del dispositivo",
                    "Verifica que los sensores estén funcionando",
                    "Actualiza el firmware si está disponible",
                    "Programa mantenimiento preventivo"
                ]
            },
            "CRITICAL": {
                "emoji": "🚨",
                "title": "ALERTA CRÍTICA",
                "color": "#C0392B",  # Rojo oscuro
                "urgency": "Crítica",
                "icon_bg": "#FFCDD2",
                "actions": [
                    "🚨 ATENCIÓN INMEDIATA REQUERIDA",
                    "Contacta soporte técnico URGENTEMENTE",
                    "No manipules el dispositivo",
                    "Documenta el estado actual del dispositivo"
                ]
            },
            "MAINTENANCE": {
                "emoji": "🔧",
                "title": "Mantenimiento Programado",
                "color": "#8E44AD",  # Púrpura
                "urgency": "Informativa",
                "icon_bg": "#F3E5F5",
                "actions": [
                    "El dispositivo estará fuera de servicio temporalmente",
                    "El mantenimiento se completará automáticamente",
                    "No se requiere acción de tu parte",
                    "Recibirás notificación cuando termine"
                ]
            }
        }

        return configs.get(error_type, configs["ERROR"])

    @staticmethod
    def generate_dynamic_html(
        user_name: str,
        device_name: str,
        mac_address: str,
        error_type: str,
        message: str
    ) -> str:
        """
        Genera HTML dinámico personalizado según el tipo de alerta
        """
        config = EmailTemplateService.get_alert_config(error_type)

        # Generar lista de acciones dinámicamente
        actions_html = ""
        for action in config["actions"]:
            actions_html += f"<li>{action}</li>\n                            "

        # CSS dinámico según urgencia
        urgency_styles = {
            "Crítica": "animation: pulse 2s infinite;",
            "Alta": "border-left: 5px solid #E74C3C;",
            "Media": "border-left: 3px solid #F39C12;",
            "Baja": "border-left: 2px solid #3498DB;",
            "Informativa": "border-left: 2px solid #8E44AD;"
        }

        urgency_style = urgency_styles.get(config["urgency"], "")

        html_template = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{config['emoji']} {config['title']} - VOLTIO</title>
            <style>
                @keyframes pulse {{
                    0% {{ box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.7); }}
                    70% {{ box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }}
                    100% {{ box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }}
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    overflow: hidden;
                    {urgency_style}
                }}
                
                .header {{
                    background: linear-gradient(135deg, {config['color']} 0%, #2c3e50 100%);
                    color: white;
                    padding: 30px 20px;
                    text-align: center;
                }}
                
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }}
                
                .urgency-badge {{
                    background: rgba(255,255,255,0.2);
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-size: 12px;
                    margin-top: 10px;
                    display: inline-block;
                }}
                
                .content {{
                    padding: 30px;
                }}
                
                .alert-icon {{
                    font-size: 48px;
                    text-align: center;
                    margin: 20px 0;
                    padding: 20px;
                    background: {config['icon_bg']};
                    border-radius: 10px;
                }}
                
                .device-info {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 4px solid {config['color']};
                }}
                
                .device-info h3 {{
                    margin-top: 0;
                    color: {config['color']};
                }}
                
                .alert-type {{
                    background: {config['color']};
                    color: white;
                    padding: 3px 8px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                
                .actions {{
                    background: #e8f4f8;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                
                .actions h3 {{
                    color: #2c3e50;
                    margin-top: 0;
                }}
                
                .actions ul {{
                    margin: 0;
                    padding-left: 20px;
                }}
                
                .actions li {{
                    margin: 8px 0;
                    color: #34495e;
                }}
                
                .footer {{
                    background: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    font-size: 12px;
                }}
                
                .timestamp {{
                    background: #ecf0f1;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 12px;
                    color: #7f8c8d;
                    text-align: center;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>{config['emoji']} {config['title']}</h1>
                    <div class="urgency-badge">Urgencia: {config['urgency']}</div>
                </div>
                
                <div class="content">
                    <div class="alert-icon">
                        {config['emoji']}
                    </div>
                    
                    <h2>Hola {user_name},</h2>
                    
                    <p>Hemos detectado un problema con uno de tus dispositivos:</p>
                    
                    <div class="device-info">
                        <h3>📱 Información del Dispositivo</h3>
                        <p><strong>Nombre:</strong> {device_name}</p>
                        <p><strong>MAC Address:</strong> {mac_address}</p>
                        <p><strong>Tipo de Alerta:</strong> <span class="alert-type">{error_type}</span></p>
                    </div>
                    
                    <div class="device-info">
                        <h3>📋 Descripción del Problema</h3>
                        <p>{message}</p>
                    </div>
                    
                    <div class="timestamp">
                        🕐 Detectado automáticamente por el Sistema VOLTIO
                    </div>
                    
                    <div class="actions">
                        <h3>🔧 Acciones Recomendadas</h3>
                        <ul>
                            {actions_html}
                        </ul>
                    </div>
                    
                    <p><strong>Nota:</strong> Esta notificación también está disponible en tu panel de control de VOLTIO.</p>
                </div>
                
                <div class="footer">
                    <p>🔔 Sistema de Notificaciones VOLTIO</p>
                    <p>Este es un email automático - No respondas a este correo</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html_template
