const commentField = document.querySelector("#comment-field")
const movieTitle = document.querySelector(".comment-create-form").getAttribute("data-movie-title")

commentField.setAttribute('placeholder', `이 ${movieTitle}에 대한 생각을 자유롭게 표현해주세요.`)