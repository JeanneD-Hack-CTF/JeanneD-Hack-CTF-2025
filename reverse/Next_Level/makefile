TARGET_INIT=final_level
TARGET_NEXT=next_level
HEADER=embedded.h
CC=gcc
CFLAGS=-O3

all:
	$(CC) $(CFLAGS) $(TARGET_INIT).c -o program 
	xxd -i program > embedded.h
	for number in `seq 1 100` ; do                 \
		echo "Compiling N°$$number";                 \
		$(CC) $(CFLAGS) $(TARGET_NEXT).c -o program; \
		strip program;                               \
		xxd -i program > $(HEADER);                  \
	done
	rm -rf program
	$(CC) $(CFLAGS) $(TARGET_NEXT).c -o $(TARGET_NEXT) 
	strip $(TARGET_NEXT)

clean:
	rm -rf $(TARGET_INIT) $(TARGET_NEXT) $(HEADER) program
