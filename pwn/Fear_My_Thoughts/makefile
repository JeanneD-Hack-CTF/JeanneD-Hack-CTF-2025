TARGET=fear_my_thoughts
CC=gcc
CFLAGS=-Wno-stringop-overflow -Wno-format-security -O0
LDFLAGS=

all:
	$(CC) $(CFLAGS) $(TARGET).c $(LDFLAGS) -o $(TARGET) 

clean:
	rm -rf $(TARGET)
