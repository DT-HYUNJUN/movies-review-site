const trendingBox = document.querySelector('.trending-box')
const movieSearch = document.querySelector('.movie-search')

function addBlur() {
  trendingBox.classList.add('is-onblur')
}
function removeBlur() {
  trendingBox.classList.remove('is-onblur')
}

// 검색창 포커스 받으면 추천 검색어 보이게
movieSearch.addEventListener('focus', removeBlur)

// 문서 클릭되면 추천검색어 제거
document.addEventListener('click', addBlur)

// 검색창과 추천검색 영역은 클릭해도 제거되지 않음
trendingBox.addEventListener('click', function(e) {
  e.stopPropagation();
})
movieSearch.addEventListener('click', function(e) {
  e.stopPropagation();
})

// 입력창이 공백일 때만 추천 검색어 보여주기
movieSearch.addEventListener('input', function(e) {
  if (e.target.value.trim() === '') {
    removeBlur()
  } else {
    addBlur()
  }
});