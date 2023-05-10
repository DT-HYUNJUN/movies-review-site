let currentUrl = window.location.href
console.log(currentUrl)
const navbar = document.querySelector('nav')

if (currentUrl === 'http://localhost:8000/movies/' | currentUrl === 'http://127.0.0.1:8000/movies/') {
  navbar.classList.remove('header-color', 'border-bottom')
  navbar.classList.add('dark-header-color')
} else {
  navbar.classList.remove('dark-header-color')
  navbar.classList.add('header-color', 'boder-bottom')
}