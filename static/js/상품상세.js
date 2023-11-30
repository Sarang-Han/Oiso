let slideIndex = 0;
showSlides(slideIndex);


window.onload = function() {
    let slides = document.getElementsByClassName("slide");
    let arrowButtons = document.getElementsByClassName("slider-btn");

    // 이미지가 하나만 있을 경우 화살표 버튼 숨김
    if (slides.length <= 1) {
        for (let i = 0; i < arrowButtons.length; i++) {
            arrowButtons[i].style.display = 'none';
        }
    }
};

// 화살표 버튼 클릭 시 호출
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("slide");

    if (n >= slides.length) {slideIndex = 0}
    if (n < 0) {slideIndex = slides.length - 1}

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slides[slideIndex].style.display = "block";
}