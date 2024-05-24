import { Router } from "../../utils/router.js";
import { data } from '../../data/data.js';

export class App {
  router = new Router([]);
  template = ``;
  items

  constructor(hostElement) {
    this.hostElement = hostElement;
  }

  async render() {
    this.hostElement.innerHTML = this.template;
    this.items = await fetch('https://raw.githubusercontent.com/lopendres2/lopendres2.github.io/main/data/data.js');
    
    this.router.add("Home", () => {
      this.hostElement.innerHTML = "";
      import("../home/home.js").then(({ Home }) => {
        new Home(this.items, this.hostElement).render();
      });
    });
    this.router.add("About", () => {
      this.hostElement.innerHTML = "";
      import("../about/about.js").then(({ About }) => {
        new About(this.items.json(), this.hostElement).render();
      });
    });
    this.router.onHashChange();
  }
}