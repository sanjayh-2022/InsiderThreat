const Chart = require('chart.js/auto');
require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseAnonKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseAnonKey);

async function fetchAndDisplayUserAnalysis() {
  let { data: userAnalysisData, error } = await supabase
    .from('user_analysis')
    .select('*');

  if (error) {
    console.error('Error fetching data:', error);
    return;
  }

  const aggregatedData = aggregateUserData(userAnalysisData);
  displayUserList(aggregatedData);
  renderGraphs(aggregatedData);
}

function aggregateUserData(userAnalysisData) {
  return userAnalysisData.reduce((acc, { user_name, application, duration }) => {
    acc[user_name] = acc[user_name] || {};
    if (!acc[user_name][application] || acc[user_name][application] < duration) {
      acc[user_name][application] = duration;
    }
    return acc;
  }, {});
}

function displayUserList(aggregatedData) {
  const userListElement = document.getElementById('userList');
  userListElement.innerHTML = '';

  Object.entries(aggregatedData).forEach(([user_name, applications]) => {
    const li = document.createElement('li');
    const p = document.createElement('p');
    p.textContent = user_name;
    p.addEventListener('click', () => generateChartForUser(user_name, applications)); // Add event listener to display chart on click
    const i = document.createElement('i');
    i.className = 'bx bx-dots-horizontal-rounded';
    li.appendChild(p);
    li.appendChild(i);
    userListElement.appendChild(li);
  });
}

function generateChartForUser(user_name, applications) {
  const ctx = document.getElementById('usageChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(applications),
      datasets: [{
        label: `Usage for ${user_name}`,
        data: Object.values(applications),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Event listener for tab buttons
document.querySelectorAll('.tab-button').forEach(button => {
  button.addEventListener('click', () => {
    const tab = button.getAttribute('data-tab');

    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));

    button.classList.add('active');
    document.getElementById(tab).classList.add('active');
  });
});

function renderGraphs(aggregatedData) {
  // Example of rendering one chart. Repeat for other charts as needed.
  const ctxUsage = document.getElementById('usageChart').getContext('2d');
  new Chart(ctxUsage, {
    type: 'bar',
    data: {
      labels: Object.keys(aggregatedData),
      datasets: [{
        label: 'Application Usage',
        data: Object.values(aggregatedData).map(applications => {
          return Object.values(applications).reduce((sum, duration) => sum + duration, 0);
        }),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  // Repeat the chart generation process for other charts using `violationCountChart`, `violationDurationChart`, and `activityOverTimeChart`
}

fetchAndDisplayUserAnalysis();
