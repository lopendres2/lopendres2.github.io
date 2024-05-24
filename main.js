import { App } from "./components/app/app.js";
import { Telegram } from './components/telegram/telegram.js'

const Application = new App(document.querySelector(".app"));
Application.render();

const tg = new Telegram();









// let usercard = document.getElementById("usercard");

// let p = document.createElement("p");

// p.innerText = `${tg.initDataUnsafe.user.first_name} ${tg.initDataUnsafe.user.last_name}`;

// usercard.appendChild(p);

