import { Router } from "../../utils/router.js";
import { data } from '../../data/data.js';

export class App {
  router = new Router([]);
  template = ``;
  items = fetch('https://raw.githubusercontent.com/lopendres2/lopendres2.github.io/blob/main/data/data.js',  { mode: 'no-cors'});

  constructor(hostElement) {
    this.hostElement = hostElement;
  }

  async render() {
    this.hostElement.innerHTML = this.template;

    this.router.add("Home", () => {
      this.hostElement.innerHTML = "";
      import("../home/home.js").then(({ Home }) => {
        new Home(this.items.json(), this.hostElement).render();
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