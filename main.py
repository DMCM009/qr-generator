from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import urllib.request
import urllib.parse

# CONSTANTES (parámetros de inicialización)
ANCHO, ALTO = 700, 650
TITULO = 'Generador de QR y Acortador de Enlaces'

class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.set_window()
        self.config_window()
        self.event_handler()
        self.show()

    def show_custom_msg(self, icon, title, text):
        """Muestra una ventana emergente con estilo personalizado (texto blanco y fondo oscuro)."""
        msg_box = QMessageBox(icon, title, text, QMessageBox.Ok, self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QPushButton {
                color: #ffffff;
                background-color: #00ffff;
                color: #000000;
                border-radius: 5px;
                padding: 6px 15px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #00cccc;
            }
        """)
        msg_box.exec_()

    def set_window(self):
        # Usamos un diseño vertical (QVBoxLayout) para estructurar la app limpiamente
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

        # Título de la aplicación llamativo
        self.title_label = QLabel("⚡ QR & LINK SHORTENER ⚡")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00ffff; font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.main_layout.addWidget(self.title_label)

        # Entrada de texto para el enlace
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ingresa aquí el link del video o imagen...")
        self.input.setStyleSheet('''
            QLineEdit {
                color: #ffffff;
                background-color: #2b2b36;
                border: 2px solid #444454;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #00ffff;
            }
        ''')
        self.main_layout.addWidget(self.input)

        # Layout horizontal para posicionar los botones uno al lado del otro
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(15)

        self.btn = QPushButton('✂️ Recortar Link')
        self.btn2 = QPushButton('🔲 Generar QR')

        # Estilos llamativos con efecto interactivo (:hover)
        self.btn.setStyleSheet('''
            QPushButton {
                color: #000000;
                background-color: #00ffff;
                border-radius: 15px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #00cccc;
            }
        ''')
        self.btn2.setStyleSheet('''
            QPushButton {
                color: #ffffff;
                background-color: #ff1900;
                border-radius: 15px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #cc1400;
            }
        ''')

        self.button_layout.addWidget(self.btn)
        self.button_layout.addWidget(self.btn2)
        self.main_layout.addLayout(self.button_layout)

        # Layout horizontal para el campo de resultado y su botón de copiar
        self.result_layout = QHBoxLayout()
        self.result_layout.setSpacing(10)

        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setPlaceholderText("El link recortado aparecerá aquí...")
        self.result_input.setStyleSheet('''
            QLineEdit {
                color: #00ffff;
                background-color: #1a1a24;
                border: 1px dashed #00ffff;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
            }
        ''')
        self.result_layout.addWidget(self.result_input)

        # Botón para copiar enlace
        self.copy_btn = QPushButton('📋 Copiar')
        self.copy_btn.setStyleSheet('''
            QPushButton {
                color: #ffffff;
                background-color: #444454;
                border-radius: 10px;
                padding: 14px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #666676;
            }
        ''')
        self.result_layout.addWidget(self.copy_btn)
        self.main_layout.addLayout(self.result_layout)

        # Zona centralizada para mostrar el QR resultante o los estados de carga
        self.texto = QLabel()
        self.texto.setAlignment(Qt.AlignCenter)
        self.texto.setMinimumSize(250, 250)
        self.texto.setStyleSheet("background-color: #2b2b36; border-radius: 10px; color: #aaaaaa; font-size: 14px;")
        self.texto.setText("El código QR se visualizará en esta área")
        
        self.main_layout.addWidget(self.texto, alignment=Qt.AlignCenter)
        self.setLayout(self.main_layout)

    def config_window(self):
        self.resize(ANCHO, ALTO)
        self.setWindowTitle(TITULO)
        self.setStyleSheet("background-color: #1e1e2e;") # Color de fondo general
        font = QFont('Arial', 11)
        self.setFont(font)

    def event_handler(self):
        self.btn.clicked.connect(self.set_text)
        self.btn2.clicked.connect(self.set_QR)
        self.copy_btn.clicked.connect(self.copy_link)

    def set_text(self):
        url = self.input.text().strip()
        if not url:
            self.show_custom_msg(QMessageBox.Warning, "Atención", "Por favor, ingresa un enlace válido primero.")
            return

        self.result_input.setText("Procesando y recortando enlace...")
        QApplication.processEvents() # Fuerza la actualización de la interfaz gráfica instantáneamente

        try:
            # Conexión directa a la API de TinyURL
            api_url = "http://tinyurl.com/api-create.php?url=" + urllib.parse.quote(url)
            with urllib.request.urlopen(api_url, timeout=8) as response:
                short_url = response.read().decode('utf-8')
                self.result_input.setText(short_url)
                
                # Limpiamos visualmente el espacio inferior y damos un mensaje de éxito
                self.texto.setPixmap(QPixmap()) 
                self.texto.setText("¡Enlace recortado con éxito!")
                self.texto.setStyleSheet("background-color: #2b2b36; border-radius: 10px; color: #00ffff; font-size: 16px; font-weight: bold;")
        except Exception as e:
            self.result_input.setText("")
            self.show_custom_msg(QMessageBox.Critical, "Error", f"No se pudo recortar el enlace.\nDetalle: {e}")

    def set_QR(self):
        url = self.input.text().strip()
        if not url:
            self.show_custom_msg(QMessageBox.Warning, "Atención", "Por favor, ingresa un enlace para generar el QR.")
            return

        self.texto.setText("Generando código QR...")
        QApplication.processEvents()

        try:
            # Conexión directa a la API de QRServer para traer el código renderizado en 250x250 píxeles
            api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(url)}"
            with urllib.request.urlopen(api_url, timeout=8) as response:
                data = response.read()
                
                # Cargamos la imagen directamente desde los bytes de memoria
                imagen_qr = QPixmap()
                imagen_qr.loadFromData(data)
                
                # Renderizamos en la app y asignamos fondo blanco al QLabel para que se pueda escanear fácilmente
                self.texto.setPixmap(imagen_qr)
                self.texto.setStyleSheet("background-color: #ffffff; padding: 15px; border-radius: 10px;")
        except Exception as e:
            self.texto.setText("Error al generar el QR")
            self.texto.setStyleSheet("background-color: #2b2b36; border-radius: 10px; color: #ff1900;")
            self.show_custom_msg(QMessageBox.Critical, "Error", f"No se pudo obtener el código QR.\nDetalle: {e}")

    def copy_link(self):
        """Copia el enlace recortado al portapapeles."""
        link_text = self.result_input.text().strip()
        # Verificamos que sea un enlace válido antes de copiar
        if link_text.startswith("http"):
            clipboard = QApplication.clipboard()
            clipboard.setText(link_text)
            self.show_custom_msg(QMessageBox.Information, "Copiado", "¡Enlace copiado al portapapeles con éxito!")
        else:
            self.show_custom_msg(QMessageBox.Warning, "Atención", "No hay ningún enlace válido para copiar.")

# FUNCIÓN PARA EJECUTAR LA APP
def run():
    app = QApplication([])
    main_window = MainWindow()
    app.exec_()

if __name__ == "__main__":
    run()