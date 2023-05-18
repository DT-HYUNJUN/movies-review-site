const chart = document.getElementById('chart')
const bars = chart.querySelectorAll('.bar')
const tooltipCahrtText = document.querySelectorAll(".tooltip-chart-text")
console.log(tooltipCahrtText)
const dataString = chart.dataset.ratings.replace('[', '').replace(']', '')
const data = dataString.split(',').map(Number)
const barHeight = []

const maxData = Math.max(...data)
const maxHeight = 84

for (let i = 0; i < data.length; i++) {
  const ratio = data[i] / maxData
  barHeight.push(ratio * maxHeight)
  tooltipCahrtText[i].textContent = `${data[i]}명`
}

bars.forEach((bar, i) => {
  bar.style.height = `${barHeight[i]}px`;
  if (data[i] === maxData) {
    bar.style.backgroundColor = '#ffa136'
    tooltipCahrtText[i].textContent = `${data[i]}명`

    bar.addEventListener('mouseover', () => {
      bar.style.backgroundColor = '#f89727';
    })
    bar.addEventListener('mouseout', () => {
      bar.style.backgroundColor = '#ffa136';
    })
  }
});