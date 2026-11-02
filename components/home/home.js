export class Home {
  constructor(data, hostElement) {
      this.data = Array.isArray(data) ? data : [];
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

  // Категории собираются из data.json, чтобы не расходиться с товарами
  getCategories() {
      const categories = new Map();
      this.data.forEach((item) => {
          const name = item.category || "Без категории";
          if (!categories.has(name)) {
              categories.set(name, (item.img && item.img[0]) || "");
          }
      });
      return [...categories.entries()].map(([name, img]) => ({ name, img }));
  }

  renderCategories() {
      const categories = this.getCategories();
      if (!categories.length) {
          this.container.innerHTML = `<p class="item__text">Каталог пока пуст.</p>`;
          return;
      }
      this.container.innerHTML = categories
          .map(({ name, img }) => `<a href="#category/${encodeURIComponent(name)}" class="item">
              <div class="item__img-box">
                  <img src="${img}" alt="${name}" class="item__img" loading="lazy">
              </div>
              <p class="item__text">${name}</p>
          </a>`)
          .join("");
  }
}
