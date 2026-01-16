#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "mpi.h"
#include "utils.h"

int main(int argc, char ** argv) {
    int rank,size;
    int global[2],local[2];
    int global_padded[2];
    int grid[2];
    int i,j,t;
    int global_converged=0,converged=0;
    MPI_Datatype dummy;
    double omega;

    struct timeval tts,ttf,tcs,tcf;
    double ttotal=0,tcomp=0,total_time,comp_time;

    double ** U, ** u_current, ** u_previous, ** swap;

    MPI_Init(&argc,&argv);
    MPI_Comm_size(MPI_COMM_WORLD,&size);
    MPI_Comm_rank(MPI_COMM_WORLD,&rank);

    if (argc!=5) {
        fprintf(stderr,"Usage: mpirun -np P ./exec X Y Px Py\n");
        MPI_Abort(MPI_COMM_WORLD,-1);
    }

    global[0]=atoi(argv[1]);
    global[1]=atoi(argv[2]);
    grid[0]=atoi(argv[3]);
    grid[1]=atoi(argv[4]);

    MPI_Comm CART_COMM;
    int periods[2]={0,0};
    int rank_grid[2];

    MPI_Cart_create(MPI_COMM_WORLD,2,grid,periods,0,&CART_COMM);
    MPI_Cart_coords(CART_COMM,rank,2,rank_grid);

    for (i=0;i<2;i++) {
        if (global[i]%grid[i]==0) {
            local[i]=global[i]/grid[i];
            global_padded[i]=global[i];
        } else {
            local[i]=global[i]/grid[i]+1;
            global_padded[i]=local[i]*grid[i];
        }
    }

    omega=2.0/(1+sin(3.14/global[0]));

    if (rank==0) {
        U=allocate2d(global_padded[0],global_padded[1]);
        init2d(U,global[0],global[1]);
    }

    u_previous=allocate2d(local[0]+2,local[1]+2);
    u_current =allocate2d(local[0]+2,local[1]+2);

    MPI_Datatype global_block;
    MPI_Type_vector(local[0],local[1],global_padded[1],MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&global_block);
    MPI_Type_commit(&global_block);

    MPI_Datatype local_block;
    MPI_Type_vector(local[0],local[1],local[1]+2,MPI_DOUBLE,&dummy);
    MPI_Type_create_resized(dummy,0,sizeof(double),&local_block);
    MPI_Type_commit(&local_block);

    int *scatteroffset=NULL,*scattercounts=NULL;
    if (rank==0) {
        scatteroffset=(int*)malloc(size*sizeof(int));
        scattercounts=(int*)malloc(size*sizeof(int));
        for (i=0;i<grid[0];i++)
            for (j=0;j<grid[1];j++) {
                scattercounts[i*grid[1]+j]=1;
                scatteroffset[i*grid[1]+j]=
                    i*local[0]*global_padded[1]+j*local[1];
            }
    }

    MPI_Scatterv(
        (rank==0 ? &(U[0][0]) : NULL),
        scattercounts,
        scatteroffset,
        global_block,
        &(u_current[1][1]),
        1,
        local_block,
        0,
        MPI_COMM_WORLD
    );

    for (i=1;i<=local[0];i++)
        for (j=1;j<=local[1];j++)
            u_previous[i][j]=u_current[i][j];

    if (rank==0)
        free2d(U);

    MPI_Datatype row_type,col_type;
    MPI_Type_contiguous(local[1],MPI_DOUBLE,&row_type);
    MPI_Type_commit(&row_type);

    MPI_Type_vector(local[0],1,local[1]+2,MPI_DOUBLE,&col_type);
    MPI_Type_commit(&col_type);

    int north,south,east,west;
    MPI_Cart_shift(CART_COMM,0,1,&north,&south);
    MPI_Cart_shift(CART_COMM,1,1,&west,&east);

    int i_min=1,i_max=local[0]+1;
    int j_min=1,j_max=local[1]+1;

    if (rank_grid[0]==0)           i_min=2;
    if (rank_grid[0]==grid[0]-1)   i_max=local[0];
    if (rank_grid[1]==0)           j_min=2;
    if (rank_grid[1]==grid[1]-1)   j_max=local[1];

    gettimeofday(&tts,NULL);

#ifdef TEST_CONV
    for (t=0;t<T && !global_converged;t++) {
#else
    #undef T
    #define T 256
    for (t=0;t<T;t++) {
#endif
        swap=u_previous;
        u_previous=u_current;
        u_current=swap;

        MPI_Sendrecv(&u_previous[1][1],1,row_type,north,0,
                     &u_previous[local[0]+1][1],1,row_type,south,0,
                     CART_COMM,MPI_STATUS_IGNORE);

        MPI_Sendrecv(&u_previous[local[0]][1],1,row_type,south,1,
                     &u_previous[0][1],1,row_type,north,1,
                     CART_COMM,MPI_STATUS_IGNORE);

        MPI_Sendrecv(&u_previous[1][1],1,col_type,west,2,
                     &u_previous[1][local[1]+1],1,col_type,east,2,
                     CART_COMM,MPI_STATUS_IGNORE);

        MPI_Sendrecv(&u_previous[1][local[1]],1,col_type,east,3,
                     &u_previous[1][0],1,col_type,west,3,
                     CART_COMM,MPI_STATUS_IGNORE);

        gettimeofday(&tcs,NULL);
        for (i=i_min;i<i_max;i++)
            for (j=j_min;j<j_max;j++)
                u_current[i][j]=(
                    u_previous[i-1][j]+u_previous[i+1][j]+
                    u_previous[i][j-1]+u_previous[i][j+1])/4.0;
        gettimeofday(&tcf,NULL);

        tcomp+=(tcf.tv_sec-tcs.tv_sec)+(tcf.tv_usec-tcs.tv_usec)*1e-6;

#ifdef TEST_CONV
        if (t%C==0) {
            converged=converge(u_previous,u_current,
                               i_min,i_max,j_min,j_max);
            MPI_Allreduce(&converged,&global_converged,
                          1,MPI_INT,MPI_LAND,MPI_COMM_WORLD);
        }
#endif
    }

    gettimeofday(&ttf,NULL);
    ttotal=(ttf.tv_sec-tts.tv_sec)+(ttf.tv_usec-tts.tv_usec)*1e-6;

    MPI_Reduce(&ttotal,&total_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);
    MPI_Reduce(&tcomp,&comp_time,1,MPI_DOUBLE,MPI_MAX,0,MPI_COMM_WORLD);

    if (rank==0)
        U=allocate2d(global_padded[0],global_padded[1]);

    MPI_Gatherv(
        &(u_current[1][1]),
        1,
        local_block,
        (rank==0 ? &(U[0][0]) : NULL),
        scattercounts,
        scatteroffset,
        global_block,
        0,
        MPI_COMM_WORLD
    );

    if (rank==0) {
        printf("Jacobi X %d Y %d Px %d Py %d Iter %d ComputationTime %lf TotalTime %lf midpoint %lf\n",
            global[0],global[1],grid[0],grid[1],t,
            comp_time,total_time,
            U[global[0]/2][global[1]/2]);
    }

    MPI_Finalize();
    return 0;
}
