const moreBtn = document.getElementById('more')
const movieOverview = document.getElementById('movie-overview')
let hide = 1

moreBtn.addEventListener('click', () => {
  if (hide) {
    movieOverview.classList.remove('close')
    moreBtn.textContent = "숨기기"
    hide = 0
  } else {
    movieOverview.classList.add('close')
    moreBtn.textContent = "더보기"
    hide = 1
  }
})