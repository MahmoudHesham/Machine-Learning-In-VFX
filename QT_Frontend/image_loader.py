import sys
import requests
import base64

from PyQt5 import QtWidgets,QtGui,QtCore

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ImageLoader(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ImageLoader, self).__init__(parent=parent)

        self.init_ui()

    def sizeHint(self):
        return QtCore.QSize(600, 400)

    def init_ui(self):
        
        self.image_placeholder = QtWidgets.QLabel("Image should be here.")
        self.image_placeholder.setMinimumHeight(300)
        
        self.load_img_btn = QtWidgets.QPushButton("Load Image")
        self.load_img_btn.clicked.connect(self.load_img_pressed)

        self.image_base64 = None

        self.submit_img_btn = QtWidgets.QPushButton("Submit Image")
        self.submit_img_btn.setEnabled(False)
        self.submit_img_btn.clicked.connect(self.submit_img_pressed)

        self.api_address_lbl = QtWidgets.QLabel("API Address: ")
        self.api_address_le = QtWidgets.QLineEdit("https://localhost:5001/api/SuperResolution")

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.image_placeholder)
        self.layout().addStretch(1)     
        self.layout().addWidget(self.api_address_lbl)
        self.layout().addWidget(self.api_address_le)
        self.layout().addWidget(self.load_img_btn)
        self.layout().addWidget(self.submit_img_btn)
        self.layout().addStretch(1)


    def load_img_pressed(self):

        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)")
        if fileName:
            self.image_placeholder.setPixmap(QtGui.QPixmap(fileName))
            self.submit_img_btn.setEnabled(True)

            self.image_name = fileName.split("/")[-1]
            with open(fileName, "rb") as image_file:
                self.image_base64 = base64.b64encode(image_file.read()).decode('utf-8')



    def submit_img_pressed(self):

        data = {"name": self.image_name, "base64": self.image_base64}

        api_address = self.api_address_le.text()
        req = requests.post(api_address, json=data, verify=False)

        if (req.status_code == 200):

            base64_returned_img = req.json()["base64"]
            hires_pixmap = QtGui.QPixmap()
            hires_pixmap.loadFromData(base64.b64decode(base64_returned_img))
            self.image_placeholder.setPixmap(hires_pixmap)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    im = ImageLoader()
    im.show()
    sys.exit(app.exec_())