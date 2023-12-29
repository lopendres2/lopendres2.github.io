from browser import document, window

tg = window.Telegram.WebApp
tg.expand()

tg.MainButton.textColor = '#FFFFFF'
tg.MainButton.color = '#2cab37'

item = ""

def on_click(event):
  # Получаем идентификатор товара из атрибута data-id кнопки.
  item_id = event.target.dataset['id']

  # Если кнопка нажата, то отображаем ее название в кнопке MainButton.
  if event.type == 'click':
    tg.MainButton.setText(f"Вы выбрали товар {item_id}!")
    item = item_id

# Подписываемся на событие нажатия кнопки.
document.querySelectorAll('.btn').forEach(button => button.addEventListener('click', on_click))
