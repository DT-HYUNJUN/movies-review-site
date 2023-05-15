// api key 가져오기
async function getApiKey() {
  try {
      const response = await fetch('/movies/api/key/');
      const { api_key } = await response.json();
      return api_key;
    } catch (error) {
      console.error(error);
    }
}


// movie_delete_form 이미지 나오게
// form의 구조 : ul-li-label-input&text
const deleteUl = document.getElementById('id_delete_movies')
const labels = deleteUl.querySelectorAll('li > label')
labels.forEach(async (label) => {
  const movie_id = label.textContent
  console.log(label)

  const api_key = await getApiKey()
  const response = await fetch(`https://api.themoviedb.org/3/movie/${movie_id}?api_key=${api_key}&language=ko-KR`);
  const movie = await response.json()
  console.log(movie)
  const formPoster = document.createElement('img')
  formPoster.src = `https://image.tmdb.org/t/p/w500/${movie.poster_path}`
  formPoster.classList.add('movie-poster-size')
  label.appendChild(formPoster)
})


// 검색창에 text입력 시 바로 검색결과 나오는 기능
const searchInput = document.getElementById('search-input')
const searchResults = document.getElementById('search-results')
const moviesDiv = document.getElementById('selected-list')
const selectedList = []
const moviesInput = document.getElementById('movies-input')

searchInput.addEventListener('input', async (event) => {
  const api_key = await getApiKey()
  const query = searchInput.value.trim()
  if (query) {
    try {
      const response = await fetch(`https://api.themoviedb.org/3/search/movie?api_key=${api_key}&query=${query}&language=ko-KR`);
      const movies = await response.json()

      // 각 movie의 칸 생성(이미지, 제목, 개봉일, form 포함)
      searchResults.innerHTML = ''
      movies.results.forEach((movie) => {
        const divTag = document.createElement('div')
        divTag.classList.add('d-flex')

        const imgTag = document.createElement('img')
        const imgUrl = `https://image.tmdb.org/t/p/w500/${movie.poster_path}`
        imgTag.setAttribute('src', imgUrl)
        imgTag.classList.add('movie-poster-size')

        const textDiv = document.createElement('div')
        const titleDiv = document.createElement('div')
        titleDiv.textContent = movie.title
        const dateDiv = document.createElement('div')
        dateDiv.textContent = movie.release_date

        const addBtn = document.createElement('button')
        addBtn.classList.add('add-btn')
        addBtn.textContent = '추가'
        addBtn.addEventListener('click', function (event) {
          // 클릭 시 버튼 체크모양
          addBtn.textContent = ''
          const iTag = document.createElement('i')
          iTag.classList.add('bi', 'bi-check2-circle')
          addBtn.appendChild(iTag)

          // selectedList 배열에 movie추가 후 문자열로 변환하여 input 필드 값으로 설정
          selectedList.push(movie)
          moviesInput.value = JSON.stringify(selectedList)

          // 추가한 영화 목록 사용자가 볼 수 있도록 출력
          const selectedMovieImg = document.createElement('img')
          selectedMovieImg.src = `https://image.tmdb.org/t/p/w500/${movie.poster_path}`
          selectedMovieImg.classList.add('movie-poster-size')

          moviesDiv.appendChild(selectedMovieImg)
        })
        
        textDiv.appendChild(titleDiv)
        textDiv.appendChild(dateDiv)
        divTag.appendChild(imgTag)
        divTag.appendChild(textDiv)
        divTag.appendChild(addBtn)
        searchResults.appendChild(divTag)
      })
    } catch (error) {
      console.error(error)
    }
  } else {
    searchResults.innerHTML = '';
  }
})