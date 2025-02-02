CC = gcc
CFLAGS = -std=c2x
TARGET = SOLVE
SRCS = SOLVE.c 
OBJS = $(SRCS:.c=.o)
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

-include $(DEPS)

clean:
	rm -f $(TARGET) $(OBJS) $(DEPS)

distclean: clean
	rm -f *~
		
.PHONY: all clean distclean
