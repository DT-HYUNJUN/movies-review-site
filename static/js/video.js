const modals = document.querySelectorAll('.modal');

modals.forEach(modal => {
  const closeModalButton = modal.querySelector('.btn-close');

  function stopVideo() {
    const video = modal.querySelector('video');
    video.pause();
  }

  closeModalButton.addEventListener('click', () => {
    modal.addEventListener('hidden.bs.modal', stopVideo);
  });
  
  modal.addEventListener('hidden.bs.modal', stopVideo);
});