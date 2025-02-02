CC=gcc
CFLAGS=-Wall
LDFLAGS=

all:
	$(CC) -c $(CFLAGS) hashtree.c
	$(CC) -c $(CFLAGS) string.c
	$(CC) -c $(CFLAGS) custom_fs.c
	$(CC) -c $(CFLAGS) main.c
	$(CC) $(LDFLAGS) *.o -o main
	strip main

debug:
	$(CC) -c $(CFLAGS) -DDEBUG hashtree.c
	$(CC) -c $(CFLAGS) -DDEBUG string.c
	$(CC) -c $(CFLAGS) -DDEBUG custom_fs.c
	$(CC) -c $(CFLAGS) -DDEBUG main.c
	$(CC) $(LDFLAGS) *.o -o main

clean:
	rm -rf *.o main
