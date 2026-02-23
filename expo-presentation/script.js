const slides = [...document.querySelectorAll('.slide')];
const counter = document.getElementById('slideCounter');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let current = 0;

function renderSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('active', i === index);
  });
  counter.textContent = `${index + 1} / ${slides.length}`;
}

function next() {
  current = (current + 1) % slides.length;
  renderSlide(current);
}

function prev() {
  current = (current - 1 + slides.length) % slides.length;
  renderSlide(current);
}

nextBtn.addEventListener('click', next);
prevBtn.addEventListener('click', prev);

window.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowRight' || event.key === 'PageDown' || event.key === ' ') {
    next();
  }
  if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
    prev();
  }
});

renderSlide(current);
