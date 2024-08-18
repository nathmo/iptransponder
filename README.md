# IP transponder


# GOAL
this tool aim at manually testing complex firewall rule between two site by offering a webpage with a form to either send a packet to a specified IP and port or by setting a callback if a packet is received from a specific IP on a given port.

# current status
the tool was done in 20 minutes and is mostly untested.
might finnish it another day.

# Usage
clone this repo and cd inside.
then run 
`docker build -t iptransponder .`
`docker run --rm --cap-add=NET_RAW --cap-add=NET_ADMIN -p 5000:5000 iptransponder`

you should now be able to access http://192.168.1.141:5000/ and http://192.168.1.141:5000/logs
