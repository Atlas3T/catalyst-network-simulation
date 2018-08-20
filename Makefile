CPPS := $(wildcard *.cpp)
HS := $(wildcard *.h)
INC := ../..
CXXFLAGS = -O0 -g -std=c++17

.PHONY: all

all: simulation

simulation: ${HS} ${CPPS}
	g++ ${CXXFLAGS} -I${INC} ${CPPS} -lusgov -L/usr/lib -L../gov -o simulation

clean:
	rm -f simulation
	find . -name "*.o" -delete
