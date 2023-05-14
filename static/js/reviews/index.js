$(document).ready(function(){
  $('.review-slide').slick({
    infinite: true,
    slidesToShow: 3,
    slidesToScroll: 3,
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

console.log(isSpoilerList)

spoilerCheckList.forEach((spoilerCheck, index) => {
  spoilerCheck.addEventListener('click', () => {
    reviewContentList[index].classList.remove("hide-spoiler-content")
    spoilerGuideList[index].classList.add("hide-spoiler-content")
    likeBtnList[index].disabled = false
    likeBtnList[index].classList.remove("spoiler-like-btn")
    likeBtnList[index].classList.add("like-btn")
    dislikeBtnList[index].disabled = false
    likeBtnList[index].classList.remove("spoiler-dislike-btn")
    likeBtnList[index].classList.add("dislike-btn")
    spoilerReviewFooterList[index].classList.remove("spoiler-review-card-footer")
    spoilerReviewFooterList[index].classList.add("review-card-footer")
    likeIconList[index].classList.remove("spoiler-thumbs-up-icon")
    dislikeIconList[index].classList.remove("spoiler-thumbs-down-icon")
    likeIconList[index].classList.add("thumbs-up-icon")
    dislikeIconList[index].classList.add("thumbs-down-icon")
  })
})