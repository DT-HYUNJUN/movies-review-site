$(document).ready(function(){
  $('.review-slide').slick({
    infinite: false,
    slidesToShow: 3,
    slidesToScroll: 3,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})

$(document).ready(function(){
  $('.collection-list').slick({
    infinite: false,
    slidesToShow: 4,
    slidesToScroll: 4,
    prevArrow : "<button type='button' class='slick-prev'>Previous</button>",    
    nextArrow : "<button type='button' class='slick-next'>Next</button>",
  });
})


const isSpoilerList = document.querySelectorAll(".spoiler-check")
const reviewContentList = document.querySelectorAll(".hide-spoiler-content")
const spoilerCheckList = document.querySelectorAll(".spoiler-check")
const spoilerGuideList = document.querySelectorAll(".spoiler-guide")
const likeBtnList = document.querySelectorAll(".spoiler-like-btn")
const dislikeBtnList = document.querySelectorAll(".spoiler-dislike-btn")
const spoilerReviewFooterList = document.querySelectorAll(".spoiler-review-card-footer")
const likeIconList = document.querySelectorAll(".spoiler-thumbs-up-icon")
const dislikeIconList = document.querySelectorAll(".spoiler-thumbs-down-icon")

// console.log(isSpoilerList)

spoilerCheckList.forEach((spoilerCheck, index) => {
  const isLiked = spoilerCheck.dataset.isliked
  const isDisliked = spoilerCheck.dataset.isdisliked
  console.log(isLiked, isDisliked)

  spoilerCheck.addEventListener('click', () => {
    reviewContentList[index].classList.remove("hide-spoiler-content")
    spoilerGuideList[index].classList.add("hide-spoiler-content")
    likeBtnList[index].disabled = false
    likeBtnList[index].classList.remove("spoiler-like-btn")
    likeBtnList[index].classList.add("review-like-btn")
    likeBtnList[index].classList.add("review-emote-btn")
    if (isLiked === 'True') {
      likeBtnList[index].classList.add("is-liked-btn")
    }
    dislikeBtnList[index].disabled = false
    dislikeBtnList[index].classList.remove("spoiler-dislike-btn")
    dislikeBtnList[index].classList.add("review-emote-btn")
    dislikeBtnList[index].classList.add("review-dislike-btn")
    if (isDisliked === 'True') {
      dislikeBtnList[index].classList.add("is-disliked-btn")
    }
    spoilerReviewFooterList[index].classList.remove("spoiler-review-card-footer")
    spoilerReviewFooterList[index].classList.add("review-card-footer")
    likeIconList[index].classList.remove("spoiler-thumbs-up-icon")
    dislikeIconList[index].classList.remove("spoiler-thumbs-down-icon")
    likeIconList[index].classList.add("thumbs-up-icon")
    dislikeIconList[index].classList.add("thumbs-down-icon")
  })
})


// 리뷰 좋아요/싫어요 비동기
const likeReviewsForms = document.querySelectorAll('.like-reviews-forms')
const dislikeReviewsForms = document.querySelectorAll('.dislike-reviews-forms')
const csrftoken = document.querySelector('.like-reviews-forms>[name=csrfmiddlewaretoken]').value

likeReviewsForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()

    const reviewId = event.target.dataset.reviewId
    axios({
      method: 'post',
      // <int:review_pk>/comments/<int:comment_pk>/emotes/<int:emotion>/
      url: `/reviews/${reviewId}/emotes/1/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
      .then((response) => {
        const isChecked = response.data.is_checked
        const likeReviewsBtn = document.querySelector(`#like-reviews-btn-${reviewId}`)
        const likeReviewsIcon = document.querySelector(`#like-reviews-icon-${reviewId}`)
        const emoteCnt = response.data.cnt
        const likeReviewsCnt = document.querySelector(`#like-reviews-cnt-${reviewId}`)
        const isAlert = response.data.alert
        if (isAlert === true) {
          alert("이미 싫어요를 눌렀습니다.")
        } else if (isChecked === true) {
          likeReviewsBtn.classList.add('is-liked-btn')
          likeReviewsIcon.classList.add('bi-hand-thumbs-up-fill')
          likeReviewsIcon.classList.remove('bi-hand-thumbs-up')
          likeReviewsCnt.textContent = emoteCnt
          // likeReviewsIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
        } else {
          likeReviewsBtn.classList.remove('is-liked-btn')
          likeReviewsIcon.classList.add('bi-hand-thumbs-up')
          likeReviewsIcon.classList.remove('bi-hand-thumbs-up-fill')
          likeReviewsCnt.textContent = emoteCnt
        }
      })
  })
})

dislikeReviewsForms.forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault()

    const reviewId = event.target.dataset.reviewId
    axios({
      method: 'post',
      // <int:review_pk>/comments/<int:comment_pk>/emotes/<int:emotion>/
      url: `/reviews/${reviewId}/emotes/0/`,
      headers: {'X-CSRFToken': csrftoken,},
    })
      .then((response) => {
        const isChecked = response.data.is_checked
        const dislikeReviewsBtn = document.querySelector(`#dislike-reviews-btn-${reviewId}`)
        const dislikeReviewsIcon = document.querySelector(`#dislike-reviews-icon-${reviewId}`)
        const emoteCnt = response.data.cnt
        const dislikeReviewsCnt = document.querySelector(`#dislike-reviews-cnt-${reviewId}`)
        const isAlert = response.data.alert

        if (isAlert === true) {
          alert("이미 좋아요를 눌렀습니다.")
        } else if (isChecked === true) {
          dislikeReviewsBtn.classList.add('is-disliked-btn')
          dislikeReviewsIcon.classList.add('bi-hand-thumbs-down-fill')
          dislikeReviewsIcon.classList.remove('bi-hand-thumbs-down')
          dislikeReviewsCnt.textContent = emoteCnt
          // likeReviewsIcon.classList.replace('bi-hand-thumbs-up-fill', 'bi-hand-thumbs-up')
        } else {
          dislikeReviewsBtn.classList.remove('is-disliked-btn')
          dislikeReviewsIcon.classList.add('bi-hand-thumbs-down')
          dislikeReviewsIcon.classList.remove('bi-hand-thumbs-down-fill')
          dislikeReviewsCnt.textContent = emoteCnt
        }
      })
  })
})