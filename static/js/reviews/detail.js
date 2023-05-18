const commentFields = document.querySelectorAll("#comment-field")
const movieTitle = document.querySelector(".movie-review-title").textContent
commentFields.forEach((commentField) => {
  commentField.setAttribute('placeholder', `이 ${movieTitle}에 대한 생각을 자유롭게 표현해주세요.`)
})

const reviewLikeBtn = document.querySelector(".review-like-btn")



// 리뷰 좋아요/싫어요 비동기
const likeReviewForms = document.querySelector('.like-review-forms')
const dislikeReviewForms = document.querySelector('.dislike-review-forms')
const csrftoken = document.querySelector('.like-review-forms>[name=csrfmiddlewaretoken]').value

likeReviewForms.addEventListener('submit', (event) => {
  event.preventDefault()
  const reviewId = event.target.dataset.reviewId
  axios({
    method: 'post',
    //<int:review_pk>/emotes/<int:emotion>/
    url: `/reviews/${reviewId}/emotes/1/`,
    headers: {'X-CSRFToken': csrftoken,},
  })
    .then((response) => {
      const isChecked = response.data.is_checked
      const likeReviewBtn = document.querySelector(`#like-review-btn-${reviewId}`)
      const likeReviewIcon = document.querySelector(`#like-review-icon-${reviewId}`)
      const emoteCnt = response.data.cnt
      const likeReviewCnt = document.querySelector(`#like-review-cnt-${reviewId}`)
      const isAlert = response.data.alert

      if (isAlert === true) {
        alert("이미 싫어요를 눌렀습니다.")
      } else if (isChecked === true) {
        likeReviewBtn.classList.add('is-liked-btn')
        likeReviewIcon.classList.add('bi-hand-thumbs-up-fill')
        likeReviewIcon.classList.remove('bi-hand-thumbs-up')
        likeReviewCnt.textContent = emoteCnt
        // likeReviewIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
      } else {
        likeReviewBtn.classList.remove('is-liked-btn')
        likeReviewIcon.classList.add('bi-hand-thumbs-up')
        likeReviewIcon.classList.remove('bi-hand-thumbs-up-fill')
        likeReviewCnt.textContent = emoteCnt
      }
    })
})


dislikeReviewForms.addEventListener('submit', (event) => {
  event.preventDefault()
  const reviewId = event.target.dataset.reviewId
  axios({
    method: 'post',
    //<int:review_pk>/emotes/<int:emotion>/
    url: `/reviews/${reviewId}/emotes/0/`,
    headers: {'X-CSRFToken': csrftoken,},
  })
    .then((response) => {
      const isChecked = response.data.is_checked
      const dislikeReviewBtn = document.querySelector(`#dislike-review-btn-${reviewId}`)
      const dislikeReviewIcon = document.querySelector(`#dislike-review-icon-${reviewId}`)
      const emoteCnt = response.data.cnt
      const dislikeReviewCnt = document.querySelector(`#dislike-review-cnt-${reviewId}`)
      const isAlert = response.data.alert

      if (isAlert === true) {
        alert("이미 좋아요를 눌렀습니다.")
      } else if (isChecked === true) {
        dislikeReviewBtn.classList.add('is-disliked-btn')
        dislikeReviewIcon.classList.add('bi-hand-thumbs-down-fill')
        dislikeReviewIcon.classList.remove('bi-hand-thumbs-down')
        dislikeReviewCnt.textContent = emoteCnt
        // likeReviewIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
      } else {
        dislikeReviewBtn.classList.remove('is-disliked-btn')
        dislikeReviewIcon.classList.add('bi-hand-thumbs-down')
        dislikeReviewIcon.classList.remove('bi-hand-thumbs-down-fill')
        dislikeReviewCnt.textContent = emoteCnt
      }
    })
})


// 댓글 좋아요/싫어요 비동기
const commentLikeBtn = document.querySelector(".comment-like-btn")
let isLiked = 0

commentLikeBtn.addEventListener("click", () => {
  if (isLiked === 0) {
    commentLikeBtn.classList.remove("is-liked-btn")
    isLiked = 1
  } else {
    commentLikeBtn.classList.add("is-liked-btn")
    isLiked = 0
  }
})

const likeCommentForms = document.querySelectorAll('.like-comment-forms')
const dislikeCommentForms = document.querySelectorAll('.dislike-comment-forms')


likeCommentForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()

    const reviewId = event.target.dataset.reviewId
    const commentId = event.target.dataset.commentId
    axios({
      method: 'post',
      // <int:review_pk>/comments/<int:comment_pk>/emotes/<int:emotion>/
      url: `/reviews/${reviewId}/comments/${commentId}/emotes/1/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
      .then((response) => {
        const isChecked = response.data.is_checked
        //like-comment-btn-{{ comment.pk }}
        //like-comment-icon-{{ comment.pk }}
        const likeCommentBtn = document.querySelector(`#like-comment-btn-${commentId}`)
        const likeCommentIcon = document.querySelector(`#like-comment-icon-${commentId}`)
        console.log(likeCommentIcon)
        const emoteCnt = response.data.cnt
        const likeCommentCnt = document.querySelector(`#like-comment-cnt-${commentId}`)
        console.log(isChecked)
        const isAlert = response.data.alert

        if (isAlert === true) {
          alert('이미 싫어요를 눌렀습니다')
        } else if (isChecked === true) {
          likeCommentBtn.classList.add('is-liked-btn')
          likeCommentIcon.classList.add('bi-hand-thumbs-up-fill')
          likeCommentIcon.classList.remove('bi-hand-thumbs-up')
          likeCommentCnt.textContent = emoteCnt
          // likeCommentIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
        } else {
          likeCommentBtn.classList.remove('is-liked-btn')
          likeCommentIcon.classList.add('bi-hand-thumbs-up')
          likeCommentIcon.classList.remove('bi-hand-thumbs-up-fill')
          likeCommentCnt.textContent = emoteCnt
        }
      })
  })
})

dislikeCommentForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()

    const reviewId = event.target.dataset.reviewId
    const commentId = event.target.dataset.commentId
    axios({
      method: 'post',
      // <int:review_pk>/comments/<int:comment_pk>/emotes/<int:emotion>/
      url: `/reviews/${reviewId}/comments/${commentId}/emotes/0/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
      .then((response) => {
        const isChecked = response.data.is_checked
        //like-comment-btn-{{ comment.pk }}
        //like-comment-icon-{{ comment.pk }}
        const dislikeCommentBtn = document.querySelector(`#dislike-comment-btn-${commentId}`)
        const dislikeCommentIcon = document.querySelector(`#dislike-comment-icon-${commentId}`)
        const emoteCnt = response.data.cnt
        const dislikeCommentCnt = document.querySelector(`#dislike-comment-cnt-${commentId}`)
        const isAlert = response.data.alert

        if (isAlert === true) {
          alert("이미 좋아요를 눌렀습니다.")
        } else if (isChecked === true) {
          dislikeCommentBtn.classList.add('is-disliked-btn')
          dislikeCommentIcon.classList.add('bi-hand-thumbs-down-fill')
          dislikeCommentIcon.classList.remove('bi-hand-thumbs-down')
          dislikeCommentCnt.textContent = emoteCnt
          // likeCommentIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
        } else {
          dislikeCommentBtn.classList.remove('is-disliked-btn')
          dislikeCommentIcon.classList.add('bi-hand-thumbs-down')
          dislikeCommentIcon.classList.remove('bi-hand-thumbs-down-fill')
          dislikeCommentCnt.textContent = emoteCnt
        }
      })
  })
})

