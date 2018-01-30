/* 
 * -- High Performance Computing Linpack Benchmark (HPL)                
 *    HPL - 2.2 - February 24, 2016                          
 *    Antoine P. Petitet                                                
 *    University of Tennessee, Knoxville                                
 *    Innovative Computing Laboratory                                 
 *    (C) Copyright 2000-2008 All Rights Reserved                       
 *                                                                      
 * -- Copyright notice and Licensing terms:                             
 *                                                                      
 * Redistribution  and  use in  source and binary forms, with or without
 * modification, are  permitted provided  that the following  conditions
 * are met:                                                             
 *                                                                      
 * 1. Redistributions  of  source  code  must retain the above copyright
 * notice, this list of conditions and the following disclaimer.        
 *                                                                      
 * 2. Redistributions in binary form must reproduce  the above copyright
 * notice, this list of conditions,  and the following disclaimer in the
 * documentation and/or other materials provided with the distribution. 
 *                                                                      
 * 3. All  advertising  materials  mentioning  features  or  use of this
 * software must display the following acknowledgement:                 
 * This  product  includes  software  developed  at  the  University  of
 * Tennessee, Knoxville, Innovative Computing Laboratory.             
 *                                                                      
 * 4. The name of the  University,  the name of the  Laboratory,  or the
 * names  of  its  contributors  may  not  be used to endorse or promote
 * products  derived   from   this  software  without  specific  written
 * permission.                                                          
 *                                                                      
 * -- Disclaimer:                                                       
 *                                                                      
 * THIS  SOFTWARE  IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,  INCLUDING,  BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY
 * OR  CONTRIBUTORS  BE  LIABLE FOR ANY  DIRECT,  INDIRECT,  INCIDENTAL,
 * SPECIAL,  EXEMPLARY,  OR  CONSEQUENTIAL DAMAGES  (INCLUDING,  BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA OR PROFITS; OR BUSINESS INTERRUPTION)  HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT,  STRICT LIABILITY,  OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
 * ---------------------------------------------------------------------
 */ 
/*
 * Include files
 */
#include "hpl.h"
#include <stdlib.h>
#include <stdio.h>

#ifdef STDC_HEADERS
void HPL_pdmatgen
(
   const HPL_T_grid *               GRID,
   const int                        M,
   const int                        N,
   const int                        NB,
   double *                         A,
   const int                        LDA,
   const int                        ISEED
)
#else
void HPL_pdmatgen
( GRID, M, N, NB, A, LDA, ISEED )
   const HPL_T_grid *               GRID;
   const int                        M;
   const int                        N;
   const int                        NB;
   double *                         A;
   const int                        LDA;
   const int                        ISEED;
#endif
{
/* 
 * Purpose
 * =======
 *
 * HPL_pdmatgen generates (or regenerates) a parallel random matrix A.
 *  
 * The  pseudo-random  generator uses the linear congruential algorithm:
 * X(n+1) = (a * X(n) + c) mod m  as  described  in the  Art of Computer
 * Programming, Knuth 1973, Vol. 2.
 *
 * Arguments
 * =========
 *
 * GRID    (local input)                 const HPL_T_grid *
 *         On entry,  GRID  points  to the data structure containing the
 *         process grid information.
 *
 * M       (global input)                const int
 *         On entry,  M  specifies  the number  of rows of the matrix A.
 *         M must be at least zero.
 *
 * N       (global input)                const int
 *         On entry,  N specifies the number of columns of the matrix A.
 *         N must be at least zero.
 *
 * NB      (global input)                const int
 *         On entry,  NB specifies the blocking factor used to partition
 *         and distribute the matrix A. NB must be larger than one.
 *
 * A       (local output)                double *
 *         On entry,  A  points  to an array of dimension (LDA,LocQ(N)).
 *         On exit, this array contains the coefficients of the randomly
 *         generated matrix.
 *
 * LDA     (local input)                 const int
 *         On entry, LDA specifies the leading dimension of the array A.
 *         LDA must be at least max(1,LocP(M)).
 *
 * ISEED   (global input)                const int
 *         On entry, ISEED  specifies  the  seed  number to generate the
 *         matrix A. ISEED must be at least zero.
 *
 * ---------------------------------------------------------------------
 */ 
/*
 * .. Local Variables ..
 */
   (void)(ISEED);
   int                        ib, iblk, jb, jblk, jk, lmb,
                              lnb, mblks, mp, mycol, myrow, nblks,
                              npcol, nprow, nq;
/* ..
 * .. Executable Statements ..
 */
   (void) HPL_grid_info( GRID, &nprow, &npcol, &myrow, &mycol );
/*
 * Generate an M by N matrix starting in process (0,0)
 */
   Mnumroc( mp, M, NB, NB, myrow, 0, nprow );
   Mnumroc( nq, N, NB, NB, mycol, 0, npcol );

   if( ( mp <= 0 ) || ( nq <= 0 ) ) return;
/*
 * Local number of blocks and size of the last one
 */
   mblks = ( mp + NB - 1 ) / NB; lmb = mp - ( ( mp - 1 ) / NB ) * NB;
   nblks = ( nq + NB - 1 ) / NB; lnb = nq - ( ( nq - 1 ) / NB ) * NB;

   char filename[50];
   char cmd[100];
   FILE **files = malloc(mblks * sizeof(FILE *));

   for( jblk = 0; jblk < nblks; jblk++ )
   {
      jb = ( jblk == nblks - 1 ? lnb : NB );
      for( jk = 0; jk < jb; jk++ )
      {
         for( iblk = 0; iblk < mblks; iblk++ )
         {
            int col = jblk * npcol + mycol;
            int row = iblk * nprow + myrow;
            if (0) {// jk == 0) {
               sprintf(cmd, "cd /home/ec2-user/HPL-solve/numpywren && /home/ec2-user/anaconda3/bin/python3 download_blocks.py %d %d", row, col);
               system(cmd);
               sprintf(filename, "/dev/shm/%d_%d", row, col);
               files[iblk] = fopen(filename, "r");
            }
            ib = ( iblk == mblks - 1 ? lmb : NB );
            FILE *curr_file = files[iblk];
            // fread(A, sizeof(double), ib, curr_file);
            int i;
            for (i = 0; i < ib; ++i) {*A = ((double)rand()) / RAND_MAX; ++A;}
            // A += ib;
            if (0) {//jk == jb - 1) {
               fclose(curr_file);
               sprintf(cmd, "rm /dev/shm/%d_%d", row, col);
               system(cmd);
            }
         }
         A += LDA - mp;
      }
   }

   free(files);
/*
 * End of HPL_pdmatgen
 */
}
