from PyQt5 import QtCore, QtGui, QtWidgets, uic, QtSerialPort
from PyQt5.QtCore import QThread, pyqtSignal
import serial
import sys
import time

dimensione_gui = 100#%  (100% or 125%) percentage of screen resizing -- in base a ridimensionamento schermo

servo1_home = 90
servo2_home = 130
servo3_home = 120
servo4_home = 130
servo5_home = 0
servo6_home = 60
durata = 1
pausa = 1
limite_posizioni = 20

servo1 = servo1_home
servo2 = servo2_home
servo3 = servo3_home
servo4 = servo4_home
servo5 = servo5_home
servo6 = servo6_home
ripetizione = False
porta = ""

baudrate_list = [115200, 57600, 38400, 19200, 9600]

class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        uic.loadUi('./serial_configuration.ui', self)
        self.setMaximumSize(260, 200)
        self.setWindowTitle("Configurazione")
        self.pushButton_ricarica.clicked.connect(self.click_ricarica)
        self.pushButton_fatto.clicked.connect(self.click_fatto)
        self.pushButton_fatto.setEnabled(False)

        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            self.comboBox_porta.addItem(info.portName())

        for baudrate in baudrate_list:
            self.comboBox_baudrate.addItem(str(baudrate), baudrate)

        if self.comboBox_porta.currentText() != "":
            self.pushButton_fatto.setEnabled(True)


    def click_ricarica(self):
        self.comboBox_porta.clear()
        for info in QtSerialPort.QSerialPortInfo.availablePorts():
            self.comboBox_porta.addItem(info.portName())
        if self.comboBox_porta.currentText() != "":
            self.pushButton_fatto.setEnabled(True)

    def click_fatto(self):
        global baudrate
        global porta
        baudrate = self.comboBox_baudrate.currentData()
        porta = self.comboBox_porta.currentText()
        config.close()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        global dimensione_gui
        uic.loadUi(f'./main_v1.5_{dimensione_gui}.ui', self)
        if dimensione_gui == 125:
            self.setFixedSize(440, 530)
        elif dimensione_gui == 100:
            self.setFixedSize(460, 530)
        self.setWindowTitle("Interfaccia di controllo")

        self.horizontalSlider_1.setMinimum(6)
        self.horizontalSlider_1.setMaximum(175)
        self.horizontalSlider_1.setValue(180-servo1_home)
        self.horizontalSlider_1.valueChanged.connect(self.slider_1_changed)
        self.horizontalSlider_1.sliderReleased.connect(self.slider_released)

        self.horizontalSlider_2.setMinimum(7)
        self.horizontalSlider_2.setMaximum(173)
        self.horizontalSlider_2.setValue(servo2_home)
        self.horizontalSlider_2.valueChanged.connect(self.slider_2_changed)
        self.horizontalSlider_2.sliderReleased.connect(self.slider_released)

        self.horizontalSlider_3.setMinimum(10)
        self.horizontalSlider_3.setMaximum(170)
        self.horizontalSlider_3.setValue(180-servo3_home)
        self.horizontalSlider_3.valueChanged.connect(self.slider_3_changed)
        self.horizontalSlider_3.sliderReleased.connect(self.slider_released)

        self.horizontalSlider_4.setMinimum(10)
        self.horizontalSlider_4.setMaximum(170)
        self.horizontalSlider_4.setValue(180-servo4_home)
        self.horizontalSlider_4.valueChanged.connect(self.slider_4_changed)
        self.horizontalSlider_4.sliderReleased.connect(self.slider_released)

        self.horizontalSlider_5.setMinimum(0)
        self.horizontalSlider_5.setMaximum(180)
        self.horizontalSlider_5.setValue(servo5_home)
        self.horizontalSlider_5.valueChanged.connect(self.slider_5_changed)
        self.horizontalSlider_5.sliderReleased.connect(self.slider_released)

        self.horizontalSlider_6.setMinimum(25)
        self.horizontalSlider_6.setMaximum(100)
        self.horizontalSlider_6.setValue(servo6_home)
        self.horizontalSlider_6.valueChanged.connect(self.slider_6_changed)
        self.horizontalSlider_6.sliderReleased.connect(self.slider_released)

        self.doubleSpinBox_durata.setMinimum(0.5)
        self.doubleSpinBox_durata.setMaximum(10)
        self.doubleSpinBox_durata.setSingleStep(0.5)
        self.doubleSpinBox_durata.setValue(1)
        self.doubleSpinBox_durata.valueChanged.connect(self.durata_changed)

        self.doubleSpinBox_pausa.setMinimum(0)
        self.doubleSpinBox_pausa.setMaximum(10)
        self.doubleSpinBox_pausa.setSingleStep(0.5)
        self.doubleSpinBox_pausa.setValue(1)
        self.doubleSpinBox_pausa.valueChanged.connect(self.pausa_changed)

        self.pushButton_salva.clicked.connect(self.click_salva)
        self.pushButton_reset.clicked.connect(self.click_reset)
        self.pushButton_esegui.clicked.connect(self.click_esegui)
        self.pushButton_home.clicked.connect(self.click_home)
        self.checkBox.stateChanged.connect(self.check_ripetizione)

        self.label_numeropos.setText(f"Posizioni: {posizioni}")
        self.label_val1.setText(str(servo1))
        self.label_val2.setText(str(servo2))
        self.label_val3.setText(str(servo3))
        self.label_val4.setText(str(servo4))
        self.label_val5.setText(str(servo5))
        self.label_val6.setText(str(servo6))
        self.progressBar.setValue(0)

    def slider_1_changed(self, i):
        global servo1
        servo1 = 180-i
        self.label_val1.setText(str(servo1))

    def slider_2_changed(self, i):
        global servo2
        servo2 = i
        self.label_val2.setText(str(servo2))

    def slider_3_changed(self, i):
        global servo3
        servo3 = 180-i
        self.label_val3.setText(str(servo3))

    def slider_4_changed(self, i):
        global servo4
        servo4 = 180-i
        self.label_val4.setText(str(servo4))

    def slider_5_changed(self, i):
        global servo5
        servo5 = i
        self.label_val5.setText(str(servo5))

    def slider_6_changed(self, i):
        global servo6
        servo6 = i
        self.label_val6.setText(str(servo6))

    def slider_released(self):
        invio = "p," + str(servo1) + "," + str(servo2) + "," + str(servo3) + "," + str(servo4) + "," + str(servo5) + "," + str(servo6) + "\n"
        arduino.write(invio.encode())

    def durata_changed(self, i):
        global durata
        durata = i

    def pausa_changed(self, i):
        global pausa
        pausa = i

    def click_salva(self):
        global limite_posizioni
        global posizioni
        if limite_posizioni > posizioni:
            invio = "s," + str(durata) + "," + str(pausa) + "\n"
            arduino.write(invio.encode())
            posizioni = posizioni + 1
            self.label_numeropos.setText(f"Posizioni: {posizioni}")

    def click_reset(self):
        global posizioni
        if posizioni > 0:
            invio = "r\n"
            arduino.write(invio.encode())
            posizioni = posizioni - 1
            self.label_numeropos.setText(f"Posizioni: {posizioni}")

    def click_esegui(self):
        global posizioni
        global ripetizione
        if posizioni > 0:
            invio = "e\n"
            arduino.write(invio.encode())
            self.pushButton_home.setEnabled(False)
            self.pushButton_salva.setEnabled(False)
            self.pushButton_reset.setEnabled(False)
            self.pushButton_esegui.setEnabled(False)
            self.horizontalSlider_1.setEnabled(False)
            self.horizontalSlider_2.setEnabled(False)
            self.horizontalSlider_3.setEnabled(False)
            self.horizontalSlider_4.setEnabled(False)
            self.horizontalSlider_5.setEnabled(False)
            self.horizontalSlider_6.setEnabled(False)
            self.doubleSpinBox_pausa.setEnabled(False)
            self.doubleSpinBox_durata.setEnabled(False)
            if ripetizione == False:
                self.checkBox.setEnabled(False)
            self.thread = External()
            self.thread.progress.connect(self.progress_bar)
            self.thread.update_1.connect(self.slider_1_update)
            self.thread.update_2.connect(self.slider_2_update)
            self.thread.update_3.connect(self.slider_3_update)
            self.thread.update_4.connect(self.slider_4_update)
            self.thread.update_5.connect(self.slider_5_update)
            self.thread.update_6.connect(self.slider_6_update)
            self.thread.start()


    def progress_bar(self, value):
        self.progressBar.setValue(value)

    def slider_1_update(self, value):
        self.horizontalSlider_1.setValue(180-value)

    def slider_2_update(self, value):
        self.horizontalSlider_2.setValue(value)

    def slider_3_update(self, value):
        self.horizontalSlider_3.setValue(180-value)

    def slider_4_update(self, value):
        self.horizontalSlider_4.setValue(180-value)

    def slider_5_update(self, value):
        self.horizontalSlider_5.setValue(value)

    def slider_6_update(self, value):
        self.horizontalSlider_6.setValue(value)


    def check_ripetizione(self, s):
        global ripetizione
        if s == 2:
            invio = "rn"
            ripetizione = True
            arduino.write(invio.encode())
            conferma = arduino.readline()
        if s == 0:
            invio = "rf"
            ripetizione = False
            arduino.write(invio.encode())

    def click_home(self):
        global servo1_home
        global servo2_home
        global servo3_home
        global servo4_home
        global servo5_home
        global servo6_home
        self.horizontalSlider_1.setValue(180-servo1_home)
        self.horizontalSlider_2.setValue(servo2_home)
        self.horizontalSlider_3.setValue(180-servo3_home)
        self.horizontalSlider_4.setValue(180-servo4_home)
        self.horizontalSlider_5.setValue(servo5_home)
        self.horizontalSlider_6.setValue(servo6_home)
        self.slider_released()

class External(QThread):          #Runs a counter thread.
    progress = pyqtSignal(int)
    update_1 = pyqtSignal(int)
    update_2 = pyqtSignal(int)
    update_3 = pyqtSignal(int)
    update_4 = pyqtSignal(int)
    update_5 = pyqtSignal(int)
    update_6 = pyqtSignal(int)
    def run(self):
        global posizioni
        global ripetizione
        while True:
            Prev = 0
            for n in range(1, posizioni+1):
                conferma = arduino.readline()
                update = conferma[0:len(conferma)-2].decode("utf-8").split(",")
                self.update_1.emit(int(update[1]))
                self.update_2.emit(int(update[2]))
                self.update_3.emit(int(update[3]))
                self.update_4.emit(int(update[4]))
                self.update_5.emit(int(update[5]))
                self.update_6.emit(int(update[6]))
                self.progress.emit(0)
                tasso = 0.21  #For 100 to make it in less than half a second -- Affinchè 100 li faccia in meno di mezzo secondo
                filtro = 0
                while True:
                    Smoothed = round(100/posizioni*n)*tasso + Prev*(1-tasso)
                    Prev = Smoothed
                    if filtro != round(Smoothed):
                        self.progress.emit(round(Smoothed))
                        if round(Smoothed) == round(100/posizioni*n):
                            break
                    filtro = round(Smoothed)
                    time.sleep(0.010)
            if ripetizione == False:
                window.pushButton_home.setEnabled(True)
                window.pushButton_salva.setEnabled(True)
                window.pushButton_reset.setEnabled(True)
                window.pushButton_esegui.setEnabled(True)
                window.horizontalSlider_1.setEnabled(True)
                window.horizontalSlider_2.setEnabled(True)
                window.horizontalSlider_3.setEnabled(True)
                window.horizontalSlider_4.setEnabled(True)
                window.horizontalSlider_5.setEnabled(True)
                window.horizontalSlider_6.setEnabled(True)
                window.doubleSpinBox_pausa.setEnabled(True)
                window.doubleSpinBox_durata.setEnabled(True)
                window.checkBox.setEnabled(True)
                break

app = QtWidgets.QApplication(sys.argv)
config = Dialog()
config.show()
config.exec_()
if porta == "":
    sys.exit()

#################################
arduino = serial.Serial(f"{porta}", baudrate=baudrate)
time.sleep(3)

setup = "setup," + str(servo1_home) + "," + str(servo2_home) + "," + str(servo3_home) + "," + str(servo4_home) + "," + str(servo5_home) + "," + str(servo6_home) + "," + str(limite_posizioni) + "\n"
arduino.write(setup.encode())

setup_1 = arduino.readline()
posizioni = int(setup_1[0:len(setup_1)-2].decode("utf-8"))
#################################

window = MainWindow()
window.show()
app.exec_()
