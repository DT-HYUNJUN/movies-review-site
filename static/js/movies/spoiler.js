const spoilerSections = document.querySelectorAll('#spoiler-section')

spoilerSections.forEach(spoilerSection => {
  const spoilerBtns = spoilerSection.querySelectorAll('#spoiler-btn')
  const reviewText = spoilerSection.querySelector('#review-text')
  const spoilerText = spoilerSection.querySelector('#spoiler-text')

  spoilerBtns.forEach(spoilerBtn => {
    spoilerBtn.addEventListener('click', () => {
      reviewText.classList.remove('hidden');
      spoilerText.classList.add('hidden')
    })
  })
});