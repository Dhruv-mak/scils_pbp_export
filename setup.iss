[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
AppId={{A1B2D3E4-E5F6-7G8H-9I0J-K1L2M3N4O5P6}}
AppName=PBP Exporter
AppVersion=1.0.0
AppPublisher=Dhruv Makwana
AppPublisherURL=https://github.com/Dhruv-mak/scils_pbp_export
AppSupportURL=https://github.com/Dhruv-mak/scils_pbp_export/issues
AppUpdatesURL=https://github.com/Dhruv-mak/scils_pbp_export/releases
DefaultDirName={autopf}\PBP Exporter
DefaultGroupName=PBP Exporter
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=
InfoAfterFile=
OutputDir=installer
OutputBaseFilename=PBP-Exporter-Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\feature_extractor_gui\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "static\*"; DestDir: "{app}\static"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\PBP Exporter"; Filename: "{app}\feature_extractor_gui.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,PBP Exporter}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\PBP Exporter"; Filename: "{app}\feature_extractor_gui.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PBP Exporter"; Filename: "{app}\feature_extractor_gui.exe"; IconFilename: "{app}\icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\feature_extractor_gui.exe"; Description: "{cm:LaunchProgram,PBP Exporter}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Registry]
; Add application to Windows "Add or Remove Programs"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{A1B2D3E4-E5F6-7G8H-9I0J-K1L2M3N4O5P6}}_is1"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\icon.ico"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{A1B2D3E4-E5F6-7G8H-9I0J-K1L2M3N4O5P6}}_is1"; ValueType: string; ValueName: "DisplayName"; ValueData: "PBP Exporter"
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{{A1B2D3E4-E5F6-7G8H-9I0J-K1L2M3N4O5P6}}_is1"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "1.0.0"