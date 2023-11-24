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
        // `file` 타입이 이미지인지 확인
        if ( /\.(jpe?g|png|gif)$/i.test(file.name) ) {
            var reader = new FileReader();

            reader.addEventListener("load", function () {
                var imageWrapper = document.createElement('div'); // 이미지를 감싸는 div 생성
                imageWrapper.style.width = "70px";
                imageWrapper.style.height = "70px";
                imageWrapper.style.border = "2px solid white";
                imageWrapper.style.borderRadius = "5px";
                imageWrapper.style.overflow = "hidden"; // 이미지가 div 크기를 넘어가면 잘림
                imageWrapper.style.display = "inline-block"; // inline-block으로 설정
                imageWrapper.style.marginRight = "10px"; // div 간 여백
                imageWrapper.style.flexShrink = "0";
                
                var image = new Image();
                image.style.width = "100%"; // div에 맞춰 이미지 크기 조정
                image.style.height = "100%";
                image.style.objectFit = "cover"; // object-fit 적용
                image.src = this.result;
                image.title = file.name;

                imageWrapper.appendChild(image); // 이미지를 div에 추가
                preview.appendChild(imageWrapper); // div를 preview 컨테이너에 추가
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