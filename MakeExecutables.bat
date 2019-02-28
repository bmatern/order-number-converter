SET CodePath=order_number_converter
SET BinPath=bin
SET SpecFile=PyinstallerOptionsWindows.spec
SET VirtualEnvironmentLocation=C:\Users\ben\Envs\minionvenv\Scripts

:: Run Pyinstaller to create executables
:: cd %CodePath%
%VirtualEnvironmentLocation%\activate && pyinstaller %SpecFile% --distpath %BinPath% --clean && deactivate

#pyinstaller PyinstallerOptionsWindows.spec --distpath bin --clean
