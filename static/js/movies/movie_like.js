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
    const likeIcon = document.getElementById('is-like')
    const notLikeIcon = document.getElementById('is-not-like')
    const inputBtn = document.getElementById('movie-like-input')
    if (isLiked === true) {
      likeIcon.hidden = true
      notLikeIcon.hidden = false
      inputBtn.classList.add('pink-color')
    } else {
      likeIcon.hidden = false
      notLikeIcon.hidden = true
      inputBtn.classList.remove('pink-color')
    }
  })
})