# IP Email Sender

To make this work, add this command to /etc/rc.local
```bash
(sleep 6;python3 "path to email_sender.py")
```

So if my ```email_sender.py``` is in ~/Developer, then the path to add is ```/home/pi/Developer/email_sender.py ```

So on my pi, it would look like
```bash
(sleep6;python3 /home/pi/Developer/email_sender.py)&
```

