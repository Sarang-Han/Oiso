function getQueryParam(param) {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// 선택된 카테고리 설정 함수
function setSelectedCategory() {
    var selectedCategory = getQueryParam('category') || 'all'; // 카테고리가 없는 경우 'all'로 설정
    var categorySelect = document.getElementById('category');
    if (categorySelect) {
        categorySelect.value = selectedCategory;
    }
}

// 페이지 로드 시 선택된 카테고리 설정
document.addEventListener('DOMContentLoaded', function() {
    setSelectedCategory();
});

function filterByCategory() {
    var selectedCategory = document.getElementById('category').value;
    window.location.href = `/메인화면?category=${selectedCategory}`;
}