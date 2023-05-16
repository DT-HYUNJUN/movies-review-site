const selectElement = document.querySelector('.gnere-select-form');
selectElement.value = '?sort_by=popularity.desc';

selectElement.addEventListener('change', function() {
  const selectedValue = this.value;
  window.open(selectedValue, '_self');

  // 선택한 값을 저장하고 다음에 페이지를 로드했을 때 이 값을 선택한 상태로 유지합니다.
  localStorage.setItem('selectedSortBy', selectedValue);
});

// 페이지 로드 시, localStorage에 저장된 값을 사용하여 선택한 값을 유지합니다.
const selectedSortBy = localStorage.getItem('selectedSortBy');
if (selectedSortBy) {
  selectElement.value = selectedSortBy;
} else {
  // 저장된 값이 없으면 기본적으로 "인기순" 옵션을 선택합니다.
  selectElement.value = '?sort_by=popularity.desc';
}