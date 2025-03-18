

function openNav() {
  document.getElementById("mySidepanel").style.right = "0";
}

function closeNav() {
  document.getElementById("mySidepanel").style.right = "-20vw";
}

let slideIndex = 1;
let slideTimeout;

showSlides(slideIndex);

function plusSlides(n) {
  clearTimeout(slideTimeout);
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  clearTimeout(slideTimeout);
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  
  slides[slideIndex-1].style.display = "block";
  slideTimeout = setTimeout(() => showSlides(slideIndex += 1), 10000);
}

window.addEventListener('DOMContentLoaded', (event) => {
  showSlides(slideIndex);
});



