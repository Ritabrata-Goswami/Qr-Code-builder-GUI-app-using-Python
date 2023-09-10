# Qr-Code-builder-GUI-app-using-Python-
GUI app that has a simple input form which takes information as input and convert it into QR code.
It takes input from each fields then concate it into one single string.
Then those data encrypted so that any other unotherized user can't steals information by simply scanning the qr code and instead he gets encoded string.
The QR code is build using
```
import pyqrcode
```
And encrypting this data using Fernet module.
```
from cryptography.fernet import Fernet
```
