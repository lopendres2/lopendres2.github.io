export class Home {
  constructor(data, hostElement) {
      this.data = data;
      this.hostElement = hostElement;
      this.template = `
          <div class="container">
              <div class="inner"></div>
          </div>
      `;
      this.render();
  }

  render() {
      this.hostElement.innerHTML = this.template;
      this.container = this.hostElement.querySelector(".inner");
      this.renderCategories();
  }

  renderCategories() {
      const categories = ["обувь", "майки", "кроссы"];
      let text = "";
      categories.forEach((category, i) => {
          let item = `<a href="#category/${category}" class="item">
              <div class="item__img-box">
                  <img src="https://via.placeholder.com/150" alt="${category}" class="item__img">
              </div>
              <p class="item__text">${category}</p>
          </a>`;
          text = text + item;
      });
      this.container.innerHTML = text;
  }
}