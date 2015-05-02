Names and email addresses of members: 
		Sarah Lee (sujuelf@csu.fullerton.edu)
       	Austin Greene (greenerz90@csu.fullerton.edu)
       	Chris Danan (poisongrape@csu.fullerton.edu)
       	Mario Andrade (ziosrighthandman@csu.fullerton.edu)

Programming Language Used: 
		Python 2.7

		We tested on Python 3 but we received string/buffer errors.
		The code works for Python version 2.7.

How to Execute: 
		Command Line Window #1 (for server) - python server.py <port_number>
	    Command Line Window #2 (for client) - python client.py localhost <port_number>

	    We developed our project on our local machines.  
	    This means that the client and server reside in the same folder and have access to the same files,
	    which is why we use "localhost" as our machine name.

	    Also, we used port number 12000 as our port number when testing the code.

Extra Credit: 
		Not implemented


References:
		We used outside references to help with some bits of code - these are documented within the code.

		We also used Professor Gofman's sample codes.

Special Notes:
		At times, if restarting the server a few seconds after it closes, an error is outputted stating that the port number is already in use.
		This error goes away after a while.  We did not find any other way to make it go away other than by waiting.