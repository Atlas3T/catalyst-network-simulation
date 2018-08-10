CC = gcc

default: libexamples.a

libexamples.a: examples.o
	ar rcs $@ $^
    
examples.o: examples.c
	$(CC) -c $<

clean:
	rm *.o *.a