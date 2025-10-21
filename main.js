
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
  });
  win.loadFile('src/index.html');
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

ipcMain.handle('save-pdf', async (event, defaultPath) => {
  const win = BrowserWindow.fromWebContents(event.sender);
  const pdf = await win.webContents.printToPDF({ printBackground: true });
  const { filePath } = await dialog.showSaveDialog(win, {
    defaultPath: defaultPath || 'report.pdf',
  });
  if (filePath) fs.writeFileSync(filePath, pdf);
  return filePath;
});
