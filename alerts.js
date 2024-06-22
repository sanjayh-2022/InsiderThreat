const { createClient } = require('@supabase/supabase-js')

const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseAnonKey)

async function fetchAlerts() {
  let { data: alerts, error } = await supabase.from('Alerts').select('*')

  if (error) {
    console.error('Error fetching alerts:', error)
    return
  }
  const tableBody = document.querySelector('.table-data table tbody')
  console.log(alerts)
  alerts.forEach((alert) => {
    const row = document.createElement('tr')
    row.innerHTML = `
      <td>${alert.user_name}</td>
      <td>${alert.alert}</td>
      <td>${alert.action}</td>
    `
    tableBody.appendChild(row)
  })
}

document.addEventListener('DOMContentLoaded', fetchAlerts)
