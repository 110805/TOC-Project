from transitions.extensions import GraphMachine


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def say_hi(self, update):
        text = update.message.text
        return text.lower() == 'hello'

    def say_name(self, update):
        text = update.message.text
        return text.lower() == 'name'

    def reply(self,update):
        return 1

    def choice(self, update):
        text = update.message.text
        return text.lower() == 'recommend'

    def go_sport(self,update):
        text=update.message.text
        return text.lower()=='sport'

    def go_movie(self,update):
        text=update.message.text
        return text.lower()=='movie'

    def go_news(self,update):
        text=update.message.text
        return text.lower()=='news'

    def go_exit(self,update):
        text=update.message.text
        return text.lower()=='exit'

    def on_enter_hello(self, update):
        update.message.reply_text("Hi!")
        self.go_back(update)

    def on_enter_name(self, update):
        update.message.reply_text("My name is Jibot, an interesting name?")
        update.message.reply_text("What's your name?")
    
    def on_enter_reply_name(self,update):
        update.message.reply_text("A great name, nice to meet you")
        self.go_back(update)

    def on_enter_recommend(self,update):
        update.message.reply_text("sport,movie or news")

    def on_enter_sport(self,update):
        update.message.reply_text("http://www.espn.com/")
        self.go_recommend(update)

    def on_enter_movie(self,update):
        update.message.reply_text("https://movies.yahoo.com.tw/")
        self.go_recommend(update)

    def on_enter_news(self,update):
        update.message.reply_text("http://edition.cnn.com/")
        self.go_recommend(update)

    def on_enter_exit(self,update):
        update.message.reply_text("See you next time")
        self.go_back(update)
