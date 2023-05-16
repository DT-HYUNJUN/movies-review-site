const modals = document.querySelectorAll('.modal');

// for (let i = 1; i < 6; i++) {
//   const modal = document.getElementById(`video${i}`)
//   const closeModalButton = modal.querySelector('.btn-close');
//   const videoContainer = modal.querySelector('.modal-body');
//   const video = videoContainer.querySelector('iframe');
//   const originalSrc = video.src;
// }

modals.forEach(modal => {
  const closeModalButton = modal.querySelector('.btn-close');
  const videoContainer = modal.querySelector('.modal-body');
  const video = videoContainer.querySelector('iframe');
  if (video) {
    const originalSrc = video.src;
  
    function stopVideo() {
      video.src = '';
      video.src = originalSrc;
    }
  
    closeModalButton.addEventListener('click', () => {
      stopVideo();
    });
  
    modal.addEventListener('hidden.bs.modal', stopVideo);
  }
});