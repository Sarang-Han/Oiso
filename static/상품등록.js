function checkImageCount() {
    var imageInput = document.getElementById('image');
    var imageCount = imageInput.files.length;
    var imageCountDisplay = document.getElementById('image-count');
    imageCountDisplay.innerText = imageCount + '/10';

    if (imageCount > 10) {
        alert("최대 10개의 이미지만 업로드할 수 있습니다.");
        imageInput.value = "";  // 선택 초기화
        imageCountDisplay.innerText = '0/10';
    }
}