Proxy Server
============

	This server strores a cached version of the websites/files that the client visits and returns the stored website/file if it is available in the cache.
	If the actual server has updated then the proxy server gets the data from there and sends it to the client.

## How To Launch

0. "python server.py" : If you are using another local server then launch that.
1. "python proxy.py" : To launch the Proxy Server.
2. Set your proxy server (either browser or system)
	a) Browser Proxy : Go to your browsers proxy settings and change the IP to localhost and the port to 12345
	b) System Proxy(Ensure that your browser uses the default system proxy): If you are using Windows 10 then there is a direct
					option in the settings to change your proxy settings where you enter the IP address as localhost and port as 12345

## Short Explanation of our code
	The code basically creates a proxy server which acts as an intermediary between the client and the actual server to which the client is requesting to.
	This server strores a cached version of the websites/files that the client visits and returns the stored website/file if it is available in the cache.
	If the actual server has updated then the proxy server gets the data from there and sends it to the client.

## Advantages
1. Faster : As cached copy can be sent faster 
2. Lesser load on the connection to ISP


### Prerequisites

1) Python
2) Have access to a testable server file

## Running the tests

For the tests we have used a server file that is in the server folder.
You could use any custom server file too.(Note: You may have to change the date time formatting of the server or change the parsing in the proxy server)


## Authors

Chanakya Vishal, Abheet Sharma

