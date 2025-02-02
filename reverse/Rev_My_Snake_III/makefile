CC=gcc
CFLAGS=
LDFLAGS=`python3-config --ldflags --cflags` -lcrypto -shared -fPIC

all:
	$(CC) $(CFLAGS) maze.c $(LDFLAGS) -o Maze.so

clean:
	rm -rf Maze.so
