[Setup]
AppName=Ambient Monitor
AppVersion=1.0.0
AppPublisher=YourName
AppPublisherURL=https://github.com/yourusername/ambient-monitor
DefaultDirName={autopf}\AmbientMonitor
DefaultGroupName=Ambient Monitor
OutputDir=installer
OutputBaseFilename=AmbientMonitor-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\AmbientMonitor.exe

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Avvia con Windows"; GroupDescription: "Opzioni aggiuntive:"

[Files]
Source: "dist\AmbientMonitor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Ambient Monitor"; Filename: "{app}\AmbientMonitor.exe"
Name: "{group}\{cm:UninstallProgram,Ambient Monitor}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Ambient Monitor"; Filename: "{app}\AmbientMonitor.exe"; Tasks: desktopicon
Name: "{userstartup}\Ambient Monitor"; Filename: "{app}\AmbientMonitor.exe"; Tasks: startupicon

[Run]
Filename: "{app}\AmbientMonitor.exe"; Description: "{cm:LaunchProgram,Ambient Monitor}"; Flags: nowait postinstall skipifsilent
