const movieLikeForm = document.getElementById('movie-like-form')
const crsftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

movieLikeForm.addEventListener('submit', function (event) {
  event.preventDefault()
  const movieId = event.target.dataset.movieId
  axios ({
    method: 'POST',
    url: `/movies/like/${movieId}/`,
    headers: {'X-CSRFToken': crsftoken},
  })
  .then((response) => {
    const isLiked = response.data.is_liked
    const inputBtn = document.getElementById('movie-like-input')
    if (isLiked === true) {
      const iconTag = inputBtn.querySelector('i')
      inputBtn.classList.add('pink-color')
      iconTag.classList.remove('bi-plus-lg')
      iconTag.classList.add('bi-check2')

    } else {
      const iconTag = inputBtn.querySelector('i')
      inputBtn.classList.remove('pink-color')
      iconTag.classList.remove('bi-check2')
      iconTag.classList.add('bi-plus-lg')
    }
  })
})