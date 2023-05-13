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

// 검색창에 text입력 시 바로 검색결과 나오는 기능
const searchInput = document.getElementById('search-input')
const searchResults = document.getElementById('search-results')

searchInput.addEventListener('input', async () => {
  const api_key = await getApiKey()
  const query = searchInput.value.trim()

  if (query) {
    try {
      const response = await fetch(`https://api.themoviedb.org/3//search/movie?api_key=${api_key}&query=${query}&language=ko-KR`);
      const movies = await response.json()

      searchResults.innerHTML = ''
      movies.results.forEach((movie) => {
        const divTag = document.createElement('div')
        divTag.classList.add('d-flex')
        const imgTag = document.createElement('img')
        const imgUrl = `https://image.tmdb.org/t/p/w500/${movie.poster_path}`
        imgTag.setAttribute('src', imgUrl)
        imgTag.setAttribute('style', 'height: 6rem;')
        const textDiv = document.createElement('div')
        const titleDiv = document.createElement('div')
        titleDiv.textContent = movie.title
        const yearDiv = document.createElement('div')
        yearDiv.textContent = movie.release_date
        textDiv.appendChild(titleDiv)
        textDiv.appendChild(yearDiv)
        divTag.appendChild(imgTag)
        divTag.appendChild(textDiv)
        searchResults.appendChild(divTag)
      })
    } catch (error) {
      console.error(error)
    }
  } else {
    searchResults.innerHTML = '';
  }
})
