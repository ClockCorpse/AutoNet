$User = "administrator"
$PWord = ConvertTo-SecureString -String "P@sswOrd" -AsPlainText -Force
$Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord
# Invoke-Command -FilePath 'dcinstall.ps1' -ComputerName '9.9.9.79' $Credential

Invoke-Command -ScriptBlock {.\DCinstall.ps1}  -ComputerName 9.9.9.79 -Credential $Credential