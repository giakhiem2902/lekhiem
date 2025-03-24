import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_en.clicked.connect(self.call_api_encrypt)
        self.ui.btn_de.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        payload = {
            "plain_text": self.ui.txtpl.toPlainText(),
            "key": self.ui.txtkey.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Response JSON:", data) 

                if "encrypted_message" in data:
                    self.ui.txtci.setPlainText(data["encrypted_message"])  
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()
                else:
                    print("Error: Key 'encrypted_message' not found in response")
            else:
                print("Error while calling API. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error:", str(e)) 

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        payload = {
            "cipher_text": self.ui.txtci.toPlainText(),
            "key": self.ui.txtkey.toPlainText() 
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Response JSON:", data)  # Debug API response

                if "decrypted_message" in data:
                    self.ui.txtpl.setPlainText(data["decrypted_message"])  

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()
                else:
                    print("Error: Key 'decrypted_message' not found in response")
            else:
                print("Error while calling API. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("Error:", str(e)) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
