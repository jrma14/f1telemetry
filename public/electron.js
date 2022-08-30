const path = require('path');
// const child_process = require('child_process');

const { app, BrowserWindow } = require('electron');
const isDev = require('electron-is-dev');

function createWindow() {
//production using pyinstaller -F server.py
// let backend;
// backend = path.join(process.cwd(), 'server/dist/server.exe')

// var execfile = require('child_process').execFile;

// execfile(backend, {
//   windowsHide: true,
// },
// (err, stdout, stderr) => {
//   if(err){
//     console.log(err);
//   }
//   if (stdout) {
//     console.log(stdout);
//     }
//     if (stderr) {
//     console.log(stderr);
//     }
// }
// )

  
  // Create the browser window.
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  // and load the index.html of the app.
  // win.loadFile("index.html");
  win.loadURL(
    isDev
      ? 'http://localhost:3000'
      : `file://${path.join(__dirname, '../build/index.html')}`
  );
  // Open the DevTools.
  if (isDev) {
    win.webContents.openDevTools({ mode: 'detach' });
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    // const { exec } = require('child_process');
    // exec('taskkill /f /t /im server.exe', (err, stdout, stderr) => {
    // if (err) {
    //   console.log(err)
    // return;
    // }
    // console.log(`stdout: ${stdout}`);
    // console.log(`stderr: ${stderr}`);
    // });
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});