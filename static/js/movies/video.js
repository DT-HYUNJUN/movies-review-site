const modals = document.querySelectorAll('.modal');

modals.forEach(modal => {
  const closeModalButton = modal.querySelector('.btn-close');
  const videoContainer = modal.querySelector('.modal-body');
  const video = videoContainer.querySelector('iframe');
  const originalSrc = video.src;

  function stopVideo() {
    video.src = '';
    video.src = originalSrc;
  }

  closeModalButton.addEventListener('click', () => {
    stopVideo();
  });

  modal.addEventListener('hidden.bs.modal', stopVideo);
});