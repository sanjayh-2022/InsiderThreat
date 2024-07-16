const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile(path.join(__dirname, 'index.html'));

  // Listen for an IPC message to show the alert
  ipcMain.on('show-alert', (event, message) => {
    dialog.showMessageBox(win, {
      type: 'info',
      title: 'Alert',
      message: message,
    });
  });
}

app.whenReady().then(createWindow);