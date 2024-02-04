export class Slider {
    constructor(data, hostElement){
        this.data = data,
        this.hostElement = hostElement
        this.currentSlide = 0;
        this.startX;
        this.isSwiping = true;
        this.dotContainer = document.querySelector('#dotContainer');
        this.render()
    }

    render() {
        this.createSlides();
        this.updateDots();
        this.applyHandler();
    }

    applyHandler(){
        this.hostElement.addEventListener('touchstart', this.handleTouchStart.bind(this));
        this.hostElement.addEventListener('touchmove', this.handleTouchMove.bind(this));
        this.hostElement.addEventListener('touchend', this.handleTouchEnd.bind(this));
  
        // Дополнительные обработчики для восстановления слайдера после свайпа
        this.hostElement.addEventListener('transitionend', () => {
          this.hostElement.style.transition = 'none';
          this.hostElement.style.transform = 'translateX(' + (-this.currentSlide * 100) + '%)';
          setTimeout(() => {
            this.hostElement.style.transition = 'transform 0.5s ease';
          });
        });
    }

    nextSlide() {
        this.setSlide(this.currentSlide + 1);
    }
  
    prevSlide() {
        this.setSlide(this.currentSlide - 1);
    }

    setSlide(index){
        const offset = -index * 100 + '%';
        this.hostElement.style.transform = 'translateX(' + offset + ')';
        this.currentSlide = index;
        this.updateDots();
    }
    
    updateDots(){
        this.dotContainer.innerHTML = '';
        for (let i = 0; i < this.data.length; i++) {
            const dot = document.createElement('div');
            dot.className = `dots__dot ${i === this.currentSlide ? 'active' : ''}`;
            dot.onclick = () => this.setSlide(i);
            this.dotContainer.appendChild(dot);
        }
    }

    handleTouchStart(event) {
        this.startX = event.touches[0].clientX;
        this.isSwiping = true;
    }
  
    handleTouchMove(event) {
        if (!this.isSwiping) return;
        const diffX = event.touches[0].clientX - this.startX;
        this.hostElement.style.transition = 'transform 0s ease';
        this.hostElement.style.transform = 'translateX(' + (-this.currentSlide * 100 + diffX) + '%';
    }
  
    handleTouchEnd(event) {
        if (!this.isSwiping) return;
        this.isSwiping = false;
        this.hostElement.style.transition = 'transform 0.5s ease';
        const threshold = 0.2;
        const distance = event.changedTouches[0].clientX - this.startX;
  
        if (Math.abs(distance) > window.innerWidth * threshold) {
          if (distance > 0) {
            this.prevSlide();
          } else {
            this.nextSlide();
          }
        } else {
          this.setSlide(this.currentSlide);
        }
    }
  
    createSlides(){
        const frag = document.createDocumentFragment();
        this.data.forEach((el,i)=>{
          let slide = document.createElement('div');
          let img = document.createElement('img');
          slide.classList.add('slider__slide');
          img.classList.add('slider__img');
          img.setAttribute('src', el)
          img.setAttribute('alt', i)
          slide.appendChild(img)
          frag.appendChild(slide)
        })
        this.hostElement.appendChild(frag)
      }
  
    

}