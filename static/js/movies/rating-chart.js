const chart = document.getElementById('chart')
const bars = chart.querySelectorAll('.bar')

const dataString = chart.dataset.ratings.replace('[', '').replace(']', '')
const data = dataString.split(',').map(Number)
const barHeight = []

const maxData = Math.max(...data)
const maxHeight = 84

for (let i = 0; i < data.length; i++) {
  const ratio = data[i] / maxData
  barHeight.push(ratio * maxHeight)
}

bars.forEach((bar, i) => {
  bar.style.height = `${barHeight[i]}px`;
  if (data[i] === maxData) {
    console.log(data[i])
    bar.style.backgroundColor = '#ffa136'
  }
});