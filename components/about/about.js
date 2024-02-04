import { Slider } from '../slider/slider.js'

export class About{
    constructor(data, hostElement){
        this.data = data;
        this.hostElement = hostElement;

        this.template = `
        <div class="container container_flex ">
        <div class="slider" id="slider">
          <div class="slider__slides" id="slides">
          </div>
        </div>
        <div class="dots" id="dotContainer"></div>
      </div>
        `
        this.render()
    }
    render(){
        this.hostElement.innerHTML = this.template;
        let index = location.hash.match(/[0-9]/gi)[0];
        const sliderContainer = this.hostElement.querySelector('.slider__slides');
        const slider = new Slider(this.data[index].img, sliderContainer );
        this.renderDescr(this.data[index])
    }

    renderDescr(data){
        const container = document.querySelector('.container')
        const frag = document.createDocumentFragment();

        const title = document.createElement('h1');
        title.innerText = data.name;
        title.classList.add('container__title');
        frag.appendChild(title);
        const text = document.createElement('p');
        text.innerText = 'Описание';
        text.classList.add('container__title_small');
        frag.appendChild(text);
        const descr = document.createElement('p');
        descr.innerText = data.description;
        descr.classList.add('container__description');
        frag.appendChild(descr);

        container.appendChild(frag)
    }

    
}