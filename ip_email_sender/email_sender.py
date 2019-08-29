
from subprocess import Popen, PIPE
import smtplib
from socket import gaierror
import string
import time

# This script attepts to retrieve the IP address of a specified interface.
# If successful it then emails the retrieved IP to a specified email address

#	FILL OUT THE VALUES BETWEEN THE COMMENT BLOCKS
#######################################################################
# Specify the sender credentials and recipient email address here
SENDER = {}
SENDER['addr'] = 'robobobandy69@gmail.com' 
SENDER['pass'] = 'creamsoup'
SENDER['serv'] = 'smtp.gmail.com'
SENDER['port'] = 465  # default GMAIL SMTP port

RECEIVER = {}
RECEIVER['addr'] = [ 'bodogcheese@gmail.com' ]; 
# Note: RECEIVER['addr']  must be a list (ie don't delete the brackets)!
# This allows the specification of a list of addresses ['me@addr.com', 'you@addr.com', 'them@addr.com']

# specify the interface to query
INTERFACE = 'wlan0' # default interface for a Raspberry Pi

# specify the name of the computer to display in the email
HOSTNAME_raw = Popen('hostname', stdout=PIPE)
# HOSTNAME = str(HOSTNAME_raw.communicate()[0].replace('\n', ''))
HOSTNAME = HOSTNAME_raw.communicate()[0].decode('utf-8').replace('\n','')


#######################################################################

# Execute the call to ifconfig 
# Use AWK to remove everything but the IP Address
# do this continously
while(True):
	try:
		# a more complicated way fo doing it
		# p1 = Popen(['ifconfig', INTERFACE], stdout=PIPE)
		# p2 = Popen(['awk', "/inet/ {split ($2,A,\":\"); print A[2]}"], stdout=PIPE, stdin=p1.stdout)
		# output = p1.communicate()[0].decode('utf-8').split(' ')
		# index = output.index('inet')
		# the_ip = output[index+1]
		p1 = Popen(['hostname', '-I'], stdout=PIPE)
		the_ip = p1.communicate()[0].decode('utf-8').replace('\n','')
		print(the_ip)
		break
	except:
		the_ip = 'FAILED'
		print("Failed to get inet")
		print("attempting to find again in 1 second")
		time.sleep(1)

	if the_ip =='':
		the_ip = 'no address found'
		print("Failed to get inet")
		print("attempting to find again in 1 second")
		time.sleep(1)




SUBJECT = "{}'s IP on {}".format(HOSTNAME, INTERFACE)

# Construct the Email
TO = RECEIVER['addr']
FROM = SENDER['addr'] 
BODY = the_ip

BODY = "Subject: {}\n\n{}".format(SUBJECT, BODY)

# Try to send the email
try:
	server = smtplib.SMTP_SSL( SENDER['serv'], SENDER['port'] )     # NOTE:  This is the GMAIL SSL port.
	server.login( SENDER['addr'], SENDER['pass'] )
	server.sendmail( FROM, TO, BODY )
	server.quit()
	print('sent email. exiting.')

except smtplib.SMTPAuthenticationError:
	print("Error, authentication failed! Please check your username and password.")

except gaierror:
	print('Error, cannot connect to: {}!  Please ensure it is a valid smtp server.'.format(SENDER['serv']))
