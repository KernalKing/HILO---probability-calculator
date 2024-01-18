import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QPainter, QColor, QPolygon

class KartenWahrscheinlichkeitApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('KernelKing_HILO')
        self.setStyleSheet("background-color: #f0f0f0;")

        mainLayout = QVBoxLayout()
        self.titel_label = QLabel("Enjoy!", self)
        self.titel_label.setFont(QFont('Arial', 24, QFont.Bold))
        self.titel_label.setStyleSheet("color: #2e2e2e; background-color: #ffd700; padding: 10px; border-radius: 10px;")
        mainLayout.addWidget(self.titel_label, alignment=Qt.AlignCenter)

        centralLayout = QVBoxLayout()
        eingabeLayout = QVBoxLayout()
        self.eingabe_label = QLabel("Which card do you see?", self)
        self.eingabe_label.setFont(QFont('Arial', 20, QFont.Bold))
        eingabeLayout.addWidget(self.eingabe_label)

        self.auswahl_karte = QComboBox(self)
        self.auswahl_karte.setFont(QFont('Arial', 18))
        kartenwerte = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.auswahl_karte.addItems(kartenwerte)
        eingabeLayout.addWidget(self.auswahl_karte)

        self.berechnen_button = QPushButton("|Calculate|", self)
        self.berechnen_button.setFont(QFont('Arial', 18))
        self.berechnen_button.clicked.connect(self.berechne_wahrscheinlichkeiten)
        eingabeLayout.addWidget(self.berechnen_button)

        centralLayout.addLayout(eingabeLayout)
        ergebnisLayout = QHBoxLayout()

        self.ergebnis_label_hoeher = QLabel("", self)
        self.ergebnis_label_hoeher.setFont(QFont('Arial', 14))
        self.ergebnis_label_hoeher.setStyleSheet("color: white; background-color: green; padding: 10px; border-radius: 5px;")
        ergebnisLayout.addWidget(self.createArrowWidget("up", self.ergebnis_label_hoeher))

        self.ergebnis_label_niedriger = QLabel("", self)
        self.ergebnis_label_niedriger.setFont(QFont('Arial', 14))
        self.ergebnis_label_niedriger.setStyleSheet("color: white; background-color: red; padding: 10px; border-radius: 5px;")
        ergebnisLayout.addWidget(self.createArrowWidget("down", self.ergebnis_label_niedriger))

        centralLayout.addLayout(ergebnisLayout)
        mainLayout.addLayout(centralLayout)
        self.setLayout(mainLayout)

    def createArrowWidget(self, direction, label):
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)

        arrowLabel = QLabel()
        arrowLabel.setFixedSize(20, 20)
        arrowLabel.setStyleSheet("background-color: transparent;")
        arrowLabel.paintEvent = lambda event, l=arrowLabel, d=direction: self.paintArrow(event, l, d)
        layout.addWidget(arrowLabel, 0, 0 if direction == "up" else 1, alignment=Qt.AlignCenter)
        layout.addWidget(label, 0, 1 if direction == "up" else 0)
        
        descriptionText = "Higher/Same" if direction == "up" else "Lower"
        descriptionLabel = QLabel(descriptionText, self)
        descriptionFont = QFont('Arial', 10)
        descriptionFont.setBold(True)  
        descriptionFont.setItalic(True)  
        descriptionLabel.setFont(descriptionFont)
        layout.addWidget(descriptionLabel, 1, 0, 1, 2, alignment=Qt.AlignCenter)

        return widget

    def paintArrow(self, event, label, direction):
        painter = QPainter(label)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("green" if direction == "up" else "red"))
        painter.setPen(Qt.NoPen)

        points = [QPoint(10, 0), QPoint(20, 20), QPoint(0, 20)] if direction == "up" else [QPoint(0, 0), QPoint(20, 0), QPoint(10, 20)]
        painter.drawPolygon(QPolygon(points))

    def berechne_wahrscheinlichkeiten(self):
        karte_wert = self.auswahl_karte.currentText().split()[0]
        kartenwerte = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        if karte_wert not in kartenwerte:
            self.ergebnis_label_hoeher.setText("Invalid Card!")
            self.ergebnis_label_niedriger.setText("")
            return

        index_gegebene_karte = kartenwerte.index(karte_wert)
        hoeher_als_gegeben = len(kartenwerte) - (index_gegebene_karte + 1)
        niedriger_als_gegeben = index_gegebene_karte

        wahrscheinlichkeit_hoeher_oder_gleich = ((hoeher_als_gegeben * 4) + 3) / 52
        wahrscheinlichkeit_niedriger = (niedriger_als_gegeben * 4) / 52

        self.ergebnis_label_hoeher.setText(f"{wahrscheinlichkeit_hoeher_oder_gleich * 100:.2f}%")
        self.ergebnis_label_niedriger.setText(f"{wahrscheinlichkeit_niedriger * 100:.2f}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KartenWahrscheinlichkeitApp()
    ex.show()
    sys.exit(app.exec_())

#Made with heart <3
#Lets Gamble <3
