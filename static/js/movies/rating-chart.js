const chart = document.getElementById('chart')
const bars = chart.querySelectorAll('.bar')
const data = [0, 15, 20, 25, 30, 35, 40, 45, 50, 75, 60]
const barHeight = []

const maxData = Math.max(...data)
const maxDataIndex = data.indexOf(maxData)
const maxHeight = 84

for (let i = 0; i < data.length; i++) {
  const ratio = data[i] / maxData
  barHeight.push(ratio * maxHeight)
}

bars.forEach((bar, i) => {
  bar.style.height = `${barHeight[i]}px`;
  if (i === maxDataIndex) {
    bar.style.backgroundColor = '#ffa136'
  }
});