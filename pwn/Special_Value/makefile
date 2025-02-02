TARGET=special_value
CC=gcc
CFLAGS=-m32 -fno-stack-protector -Wno-stringop-overflow -no-pie -Wl,-z,norelro 
LDFLAGS=

all:
	$(CC) $(CFLAGS) $(TARGET).c $(LDFLAGS) -o $(TARGET) 

clean:
	rm -rf $(TARGET)
