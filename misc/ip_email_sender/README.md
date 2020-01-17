# IP Email Sender

To make this work, add this command to /etc/rc.local
```bash
(sleep 6;python3 email_sender.py)
```
We add a delay before execution to allow some time for a WiFi connection.

