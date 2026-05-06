See README.docker for notes on the docker commands to run this on a server.

To build a windows executable you need to build the container as documented in:

http://github.com/crpalmer/python-to-exe

and then run:

docker build -t trlcorp-client-exe .
docker run -v "`pwd`":/src --rm trlcorp-client-exe
