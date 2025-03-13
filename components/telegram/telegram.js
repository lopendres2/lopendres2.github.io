export class Telegram {
  constructor() {
      this.tg = window.Telegram.WebApp;
      this.render();
  }

  render() {
      this.tg.expand();
      this.tg.MainButton.textColor = "#FFFFFF";
      this.tg.MainButton.color = "#0f53e6";
  }
}