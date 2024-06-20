const { createClient } = require('@supabase/supabase-js')

const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseAnonKey)

async function fetchUserCountAndUpdateUI() {
  // Fetch distinct user_name count from user_analysis table
  const { data, error } = await supabase
    .from('user_analysis')
    .select('user_name', { count: 'exact' })

  if (error) {
    console.error('Error fetching user count:', error)
    return
  }

  const uniqueUserNames = new Set(data.map((item) => item.user_name))
  const count = uniqueUserNames.size

  const boxInfoElement = document.querySelector(
    '.box-info li:nth-child(2) .text'
  )
  if (boxInfoElement) {
    boxInfoElement.querySelector('h3').textContent = count
    boxInfoElement.querySelector('p').textContent = 'Users'
    console.log(count)
  }
}

document.addEventListener('DOMContentLoaded', fetchUserCountAndUpdateUI)
