from browser import document, window

tg = window.Telegram.WebApp
tg.expand()

tg.MainButton.textColor = '#FFFFFF'
tg.MainButton.color = '#2cab37'

item = ""

def on_click(event):
    if tg.MainButton.isVisible:
        tg.MainButton.hide()
    else:
        tg.MainButton.setText(f"Вы выбрали товар {event.target.id[-1]}!")
        item = event.target.id[-1]
        tg.MainButton.show()

for i in range(1, 7):
    btn = document[f"btn{i}"]
    btn.bind("click", on_click)