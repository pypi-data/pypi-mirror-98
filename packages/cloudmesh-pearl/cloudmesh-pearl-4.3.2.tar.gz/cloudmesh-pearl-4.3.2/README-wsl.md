
## On Windows you can also Installing WSL2

In powershell that you start as administrator do the following

```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Now restart the machine

[Download and run the WSL2 UPdate](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)

Activate in an administrative shell with 

```
wsl --set-default-version 2
```

Now go to 

[download Ubuntu 20.04](https://www.microsoft.com/store/apps/9n6svws3rx71)

Select the get and install

Once the install is completed type in the ubuntu terminal

```
passwd
sudo apt update && sudo apt upgrade
```

If you at one point in future forgot your password see this [link](https://docs.microsoft.com/en-us/windows/wsl/user-support#forgot-your-password)

