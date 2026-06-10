from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
# Agregar el resto de componentes segun requiera

# CONSTANTES (parametros de inicializacion)
ANCHO, ALTO = 700, 500
TITULO = 'Generador de QR'
text_btn = 'Recortar Link'
text_btn2 = 'QR'
text_input = 'Ingrease link para recortar o QR'

# CLASE PRINCIPAL (VENTANA)
class MainWindow(QWidget):
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.set_window()
        self.config_window()
        self.event_handler()
        self.show()

    def set_window(self):
        # Estructurar el diseño de mi ventana
        self.btn = QPushButton(text_btn)
        self.btn2 = QPushButton(text_btn2)
        self.btn.setStyleSheet('''
                    color: #000000;
                    background-color: #00ffff;
                    border-radius: 15px;
                    padding: 10px;
                    front-weight: 600;
        ''')
        self.btn2.setStyleSheet('''
                    color: #000000;
                    background-color: #ff1900;
                    border-radius: 15px;
                    padding: 10px;
                    front-weight: 600;
        ''')
        self.texto = QLabel()
        self.input = QLineEdit(text_input)
        self.imagen = QPixmap('nigga.jpg')
        self.texto.setPixmap(self.imagen)
        self.texto.setScaledContents(True)
        self.imagen_reescalada = self.imagen.scaled(100, 100)
        self.texto.setPixmap(self.imagen_reescalada)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.input, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.btn, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.btn2, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.texto, alignment=Qt.AlignCenter)
        
        self.setLayout(self.main_layout)


    def config_window(self):
        self.resize(ANCHO, ALTO)
        self.setWindowTitle(TITULO)
        font = QFont('Arial', 15, QFont.Cursive, True)
        self.setFont(font)
        # Adaptar segun requiera

    def event_handler(self):
        # GESTION Y MANEJO DE EVENTOS (INTERACCION DEL USUARIO)
        self.btn.clicked.connect(self.set_text)
        self.btn2.clicked.connect(self.set_QR)

    def set_text(self):
        cadena = self.input.text()
        self.texto.setText(cadena)

    def set_QR(self):
        qr = self.print.QR()
        self.qr.setQR(qr)
        qr.clicked.connect(si)

    def si():
        self.imagen.show()

# FUNCION PARA EJECUTAR LA APP
def run():
    app = QApplication([])
    main_window = MainWindow()
    app.exec_()

if __name__ == "__main__":
    run()
#Acortador de Enlaces y Generador de códigos QR. Una aplicación muy práctica: el usuario introduce una URL larga, presiona un botón y la app genera un código QR en pantalla que se puede guardar como imagen, además de ofrecer una versión de la URL acortada usando una API gratuita. Lo que aprenderás: Integrar librerías externas de Python (como qrcode) con elementos visuales de PyQt. Componentes clave: QLineEdit, QPushButton y un QLabel dinámico para mostrar el código QR generado.

