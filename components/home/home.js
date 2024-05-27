export class Home {
  constructor(data, hostElement) {
    this.data = data;
    this.hostElement = hostElement;
    this.template = `
        <div class="container">
            <div class="inner"></div>
            <div class="usercard" id="usercard">	
        </div>
      `;
    this.container;
    this.WebApp = window.Telegram.WebApp;
    this.render();
  }

  render() {
    this.hostElement.innerHTML = this.template;
    this.container = this.hostElement.querySelector(".inner");
    alert("home render");
    this.renderCarts();
    this.applyHandler();
  }

  applyHandler() {
    this.container.addEventListener("click", this.onClick.bind(this));
  }

  onClick(event) {
    const current = event.target;

    if (!current.classList.contains("item__btn")) {
      return;
    }

    console.log("Товар" + " " + current.id);
  }

  renderCarts() {
    let text = "";
    alert("render cards");
    this.data.forEach((el, i) => {
      let item = `<a href="#about/item=${i}" class="item">
          <div class="item__img-box">
              <img src="${el.img[0]}" alt="" class="item__img">
          </div>
          <p class="item__text">${el.price}</p>
          <p class="item__text">${el.name}</p>
          <button class="item__btn" id="${i}">+ Добавить</button>
      </a>`;
      text = text + item;
    });
    this.container.innerHTML = text;
  }
}
