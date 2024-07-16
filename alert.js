const { ipcRenderer } = require('electron');

// Function to send a message to show the alert
function showAlert(message) {
  ipcRenderer.send('show-alert', message);
}

async function fetchAndShowLatestAlert() {
  const { data: alerts, error } = await supabase
    .from('Alerts')
    .select('*').order('time', { ascending: false })
    .limit(1);

    console.log(alerts.id)

  if (error) {
    console.error('Error fetching alerts:', error);
    return;
  }

  if (alerts.length > 0) {
    const latestAlert = alerts[0];
    showAlert(`Latest Alert: ${latestAlert.alert} at ${latestAlert.time}`);
    console.log(latestAlert)
  } else {
    showAlert('No alerts');
  }
}

// Fetch and show the latest alert
fetchAndShowLatestAlert();