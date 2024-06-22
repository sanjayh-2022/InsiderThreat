const Chart = require('chart.js/auto')
require('dotenv').config()
const { createClient } = require('@supabase/supabase-js')

const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseAnonKey)

async function fetchAndDisplayUserAnalysis() {
  let { data: userAnalysisData, error } = await supabase
    .from('user_analysis')
    .select('*')

  if (error) {
    console.error('Error fetching data:', error)
    return
  }

  const aggregatedData = aggregateUserData(userAnalysisData)
  displayUserList(aggregatedData)
}

function aggregateUserData(userAnalysisData) {
  return userAnalysisData.reduce(
    (acc, { user_name, application, duration }) => {
      acc[user_name] = acc[user_name] || {}
      if (
        !acc[user_name][application] ||
        acc[user_name][application] < duration
      ) {
        acc[user_name][application] = duration
      }
      return acc
    },
    {}
  )
}

function displayUserList(aggregatedData) {
  const userListElement = document.getElementById('userList')
  userListElement.innerHTML = ''

  Object.entries(aggregatedData).forEach(([user_name, applications]) => {
    const li = document.createElement('li')
    const p = document.createElement('p')
    p.textContent = user_name
    p.style.cursor = 'pointer'
    p.addEventListener('click', () =>
      generateChartForUser(user_name, applications)
    )
    const i = document.createElement('i')
    i.className = 'bx bx-dots-vertical-rounded'
    li.appendChild(p)
    li.appendChild(i)
    userListElement.appendChild(li)
  })
}

function generateChartForUser(user_name, applications) {
  const graphContainer = document.getElementById('graph-container')
  graphContainer.innerHTML = ''

  const canvas = document.createElement('canvas')
  canvas.id = `userChart-${user_name}`
  canvas.width = 400
  canvas.height = 400
  graphContainer.appendChild(canvas)

  const ctx = canvas.getContext('2d')
  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, 'rgba(255, 159, 64, 0.9)')
  gradient.addColorStop(1, 'rgba(255, 99, 132, 0.9)')

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(applications),
      datasets: [
        {
          label: `User ${user_name} Application Usage`,
          data: Object.values(applications),
          backgroundColor: gradient,
          borderColor: 'rgba(255, 159, 64, 1)',
          borderWidth: 2,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  })
}

async function fetchAndDisplayViolationData() {
  let { data: violationData, error } = await supabase
    .from('violations')
    .select('*')

  if (error) {
    console.error('Error fetching violation data:', error)
    return
  }

  const aggregatedData = aggregateViolationData(violationData)
  generateViolationChart(aggregatedData)
}

function aggregateViolationData(violationData) {
  return violationData.reduce((acc, { application }) => {
    acc[application] = (acc[application] || 0) + 1
    return acc
  }, {})
}

function generateViolationChart(aggregatedData) {
  const violationgraphContainer = document.getElementById('violation-count')
  violationgraphContainer.innerHTML = ''

  const canvas = document.createElement('canvas')
  canvas.id = 'violationChart'
  canvas.width = 400
  canvas.height = 400
  violationgraphContainer.appendChild(canvas)

  // Obtain the context from the newly created canvas
  const ctx = canvas.getContext('2d')
  const gradient = ctx.createLinearGradient(0, 0, 0, 400)
  gradient.addColorStop(0, 'rgba(255, 159, 64, 0.9)')
  gradient.addColorStop(1, 'rgba(255, 99, 132, 0.9)')

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(aggregatedData),
      datasets: [
        {
          label: 'Violation Application Usage Count',
          data: Object.values(aggregatedData),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  })
}

function setupUIInteractions() {
  const menuBar = document.querySelector('#content nav .bx.bx-menu')
  const sidebar = document.getElementById('sidebar')
  const searchButton = document.querySelector(
    '#content nav form .form-input button'
  )
  const searchButtonIcon = document.querySelector(
    '#content nav form .form-input button .bx'
  )
  const searchForm = document.querySelector('#content nav form')
  const switchMode = document.getElementById('switch-mode')

  menuBar.addEventListener('click', function () {
    sidebar.classList.toggle('hide')
  })

  searchButton.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
      e.preventDefault()
      toggleSearchFormVisibility()
    }
  })

  window.addEventListener('resize', function () {
    if (this.innerWidth > 576) {
      resetSearchForm()
    }
  })

  switchMode.addEventListener('change', function () {
    document.body.classList.toggle('dark', this.checked)
  })

  function toggleSearchFormVisibility() {
    searchForm.classList.toggle('show')
    searchButtonIcon.classList.toggle(
      'bx-search',
      !searchForm.classList.contains('show')
    )
    searchButtonIcon.classList.toggle(
      'bx-x',
      searchForm.classList.contains('show')
    )
  }

  function resetSearchForm() {
    searchForm.classList.remove('show')
    searchButtonIcon.classList.replace('bx-x', 'bx-search')
  }

  document.querySelectorAll('.tab-button').forEach((button) => {
    button.addEventListener('click', () => {
      const tab = button.getAttribute('data-tab')

      document
        .querySelectorAll('.tab-button')
        .forEach((btn) => btn.classList.remove('active'))
      document
        .querySelectorAll('.tab-content')
        .forEach((content) => content.classList.remove('active'))

      button.classList.add('active')
      document.getElementById(tab).classList.add('active')

      if (tab === 'violation-duration') {
        console.log(tab)
        fetchAndDisplayViolationData()
      }
    })
  })

  if (document.getElementById('vc')) {
    fetchAndDisplayViolationData()
  }
  if (document.getElementById('userList')) {
    fetchAndDisplayUserAnalysis()
  }

  // Setup violation analytics tab
  setupViolationAnalytics()
}

function setupViolationAnalytics() {
  const analyticsTab = document.getElementById('analyticsTab')
  const violationTab = document.createElement('div')
  violationTab.id = 'violation-graph-container'
  violationTab.classList.add('tab-content')
  analyticsTab.appendChild(violationTab)
}

document.addEventListener('DOMContentLoaded', setupUIInteractions)
