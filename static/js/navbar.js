let currentUrl = window.location.href
console.log(currentUrl)
const navbar = document.querySelector('nav')
const search = navbar.querySelector('#search')
const logout = document.querySelector('#logout')

// if (currentUrl === 'http://localhost:8000/movies/' | currentUrl === 'http://127.0.0.1:8000/movies/') {
if (currentUrl.includes('http://localhost:8000/movies/') | currentUrl.includes('http://127.0.0.1:8000/movies/')) {
  navbar.classList.remove('header-color', 'border-bottom')
  search.classList.remove('bg-body-secondary')
  if (logout) {
    logout.classList.remove('logout')
  }
  
  navbar.classList.add('dark-header-color')
  search.classList.add('dark-search')
  if (logout) {
    logout.classList.add('dark-logout')
  }
  
} else {
  navbar.classList.remove('dark-header-color')
  search.classList.remove('dark-search')
  if (logout) {
    logout.classList.remove('dark-logout')
  }
  
  search.classList.add('bg-body-secondary')
  navbar.classList.add('header-color', 'boder-bottom')
  if (logout) {
    logout.classList.add('logout')
  }
}