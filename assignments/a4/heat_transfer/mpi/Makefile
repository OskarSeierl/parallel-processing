MPICC = mpicc
CFLAGS = -Wall -Wextra -Wno-unused -O3
LDFLAGS = -lm

H_FILES = utils.h

CONVFLAG = -DTEST_CONV

all: mpi_jacobi

mpi_jacobi: mpi_jacobi.o utils.o
	$(MPICC) $(CFLAGS) $(CONVFLAG) $^ -o $@ $(LDFLAGS)

mpi_jacobi.o: mpi_jacobi.c $(H_FILES)
	$(MPICC) $(CFLAGS) $(CONVFLAG) -c $< -o $@

utils.o: utils.c utils.h
	$(MPICC) $(CFLAGS) $(CONVFLAG) -c $< -o $@

clean:
	rm -f *.o mpi_jacobi
