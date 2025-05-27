from PyQt5.QtWidgets import QApplication
import sys
from bot import Bot
from chat_UI import ChatUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = Bot("ShopBot")
    ventana = ChatUI(bot)
    ventana.show()
    sys.exit(app.exec_())
