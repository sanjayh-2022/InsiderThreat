const { createClient } = require('@supabase/supabase-js')

const supabaseUrl = process.env.SUPABASE_URL
const supabaseAnonKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseAnonKey)

async function fetchViolationsCount() {
  const { data, error, count } = await supabase
    .from('violations')
    .select('*', { count: 'exact' })

  if (error) {
    console.error('Error fetching violations count:', error)
    return
  }

  const newOrderH3 = document.querySelector('.box-info li:first-child .text h3')
  const newOrderP = document.querySelector('.box-info li:first-child .text p')

  if (newOrderH3 && newOrderP) {
    newOrderH3.textContent = count
    newOrderP.textContent = 'Violations'
    console.log(count)
  }
}

document.addEventListener('DOMContentLoaded', fetchViolationsCount)
