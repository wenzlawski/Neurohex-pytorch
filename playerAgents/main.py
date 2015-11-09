from gtpinterface import gtpinterface
from resistanceAgent import resistanceAgent
import sys

def main():
	"""
	Main function, simply sends user input on to the gtp interface and prints
	responses.
	"""
	agent = resistanceAgent()
	interface = gtpinterface("resistance")
	while True:
		command = raw_input()
		success, response = interface.send_command(command)
		print "= " if success else "? ",response,"\n"
		sys.stdout.flush()

if __name__ == "__main__":
	main()