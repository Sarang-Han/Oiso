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

// 이미지 미리보기 함수
function previewImages() {
    var preview = document.querySelector('.image-preview-container');
    preview.innerHTML = ''; // 기존 미리보기 초기화
    var files   = document.querySelector('input[type=file]').files;

    function readAndPreview(file) {
        
        if ( /\.(jpe?g|png|gif)$/i.test(file.name) ) {
            var reader = new FileReader();

            reader.addEventListener("load", function () {
                var imageWrapper = document.createElement('div');
                imageWrapper.style.width = "70px";
                imageWrapper.style.height = "70px";
                imageWrapper.style.border = "2px solid white";
                imageWrapper.style.borderRadius = "5px";
                imageWrapper.style.overflow = "hidden";
                imageWrapper.style.display = "inline-block";
                imageWrapper.style.marginRight = "10px";
                imageWrapper.style.flexShrink = "0";
                
                var image = new Image();
                image.style.width = "100%";
                image.style.height = "100%";
                image.style.objectFit = "cover";
                image.src = this.result;
                image.title = file.name;

                imageWrapper.appendChild(image);
                preview.appendChild(imageWrapper);
            }, false);

            reader.readAsDataURL(file);
        }
    }

    if (files) {
        [].forEach.call(files, readAndPreview);
    }
}

// 이벤트 연결
document.getElementById('image').addEventListener('change', previewImages);