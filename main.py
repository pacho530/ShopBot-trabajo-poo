from app.bot import Bot
from app.chat_UI import ChatUI

if __name__ == "__main__":
    bot = Bot("ShopBot")
    app = ChatUI(bot)
    app.mainloop()


