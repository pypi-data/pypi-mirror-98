#! /usr/bin/env python
#
# Author: Pawel A.Penczek, 09/09/2006 (Pawel.A.Penczek@uth.tmc.edu)
# Please do not copy or modify this file without written consent of the author.
# Copyright (c) 2000-2019 The University of Texas - Houston Medical School
#
# This software is issued under a joint BSD/GNU license. You may use the
# source code in this file under either license. However, note that the
# complete EMAN2 and SPARX software packages have some GPL dependencies,
# so you are responsible for compliance with the licenses of these packages
# if you opt to use BSD licensing. The warranty disclaimer below holds
# in either instance.
#
# This complete copyright notice must be included in any revised version of the
# source code. Additional authorship citations may be added, but existing
# author citations must be preserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
#
from global_def import *
from pap_statistics import k_means_init_asg_d2w, k_means_init_asg_rnd, \
	select_kmeans


def k_means_SSE_MPI(im_M, mask, K, rand_seed, maxit, trials, CTF, F=0, T0=0, DEBUG=False, rnd_method = 'rnd', myid = 0, main_node =0, jumping = 1):
    from utilities    import model_blank, get_im, running_time
    #from utilities    import print_begin_msg, print_end_msg, print_msg
    from random       import seed, randint, shuffle
    from copy         import deepcopy
    import sys
    import time
    #using jumping to change method for initialization
    if CTF[0]:
        from filter        import filt_ctf, filt_table
        from fundamentals    import fftip

        ctf  = deepcopy(CTF[1])
        ctf2 = deepcopy(CTF[2])
        CTF  = True
    else:
        CTF  = False

    # Simulated annealing use or not
    if T0 != 0: SA = True
    else:       SA = False

    if SA:
        # for simulated annealing
        from math   import exp
        from random import random

    if mask != None:
        if isinstance(mask, str):
            ERROR('Mask must be an image, not a file name!', 'k-means', 1)

    N = len(im_M)

    t_start = time.time()    
    
    # Information about images
    if CTF:
        nx  = im_M[0].get_attr('or_nx')
        ny  = im_M[0].get_attr('or_ny')
        nz  = im_M[0].get_attr('or_nz')
        buf = model_blank(nx, ny, nz)
        fftip(buf)        
        nx   = im_M[0].get_xsize()
        ny   = im_M[0].get_ysize()
        nz   = im_M[0].get_zsize()
        norm = nx * ny * nz
    else:
        nx   = im_M[0].get_xsize()
        ny   = im_M[0].get_ysize()
        nz   = im_M[0].get_zsize()
        norm = nx * ny * nz
        buf  = model_blank(nx, ny, nz)

    # Variables
    if(rand_seed > 0):  seed(rand_seed)
    else:               seed()
    if jumping ==1:
        #from random import jumpahead
        if(myid != main_node):  seed(17*myid+123)
    Cls = {}
    Cls['n']   = [0]*K     # number of objects in a given cluster
    Cls['ave'] = [0]*K     # value of cluster average
    Cls['var'] = [0]*K     # value of cluster variance
    Cls['Ji']  = [0]*K     # value of Ji
    Cls['k']   =  K           # value of number of clusters
    Cls['N']   =  N
    assign     = [0]*N
    
    if CTF:
        Cls_ctf2   = {}
        len_ctm       = len(ctf2[0])

    ## TRIALS
    if trials > 1:
        MemCls, MemJe, MemAssign = {}, {}, {}
    else:
        trials = 1
    flag_empty = False    
    ntrials    = 0
    wd_trials  = 0
    SA_run     = SA
    
    ALL_EMPTY = True    
    while ntrials < trials:
        ntrials += 1

        # for simulated annealing
        SA = SA_run
        if SA: T = T0
    
        # Init the cluster by an image empty
        buf.to_zero()
        for k in range(K):
            Cls['ave'][k] = buf.copy()
            Cls['var'][k] = buf.copy()
            Cls['n'][k]   = 0
            Cls['Ji'][k]  = 0

        if rnd_method == 'd2w': assign, Cls['n'] = k_means_init_asg_d2w(im_M, N, K)
        else:                    assign, Cls['n'] = k_means_init_asg_rnd(N, K)


        if CTF:
            ## Calculate averages ave = S CTF.F / S CTF**2, first init ctf2
            for k in range(K):    Cls_ctf2[k] = [0] * len_ctm
            
            for im in range(N):
                # compute Sum ctf2
                for i in range(len_ctm):    Cls_ctf2[assign[im]][i] += ctf2[im][i]
                
                # compute average first step
                CTFxF = filt_table(im_M[im], ctf[im])
                Util.add_img(Cls['ave'][assign[im]], CTFxF)

            for k in range(K):
                valCTF = [0] * len_ctm
                for i in range(len_ctm):    valCTF[i] = 1.0 / float(Cls_ctf2[k][i])
                Cls['ave'][k] = filt_table(Cls['ave'][k], valCTF)

            ## Compute Ji = S(im - CTFxAve)**2 and Je = S Ji
            for n in range(N):
                CTFxAve              = filt_table(Cls['ave'][assign[n]], ctf[n])
                Cls['Ji'][assign[n]] += old_div(CTFxAve.cmp("SqEuclidean", im_M[n]), norm)
            Je = 0
            for k in range(K):      Je += Cls['Ji'][k]
        else:
            ## Calculate averages
            for im in range(N):    Util.add_img(Cls['ave'][assign[im]], im_M[im])
            for k in range(K):    Cls['ave'][k] = Util.mult_scalar(Cls['ave'][k], 1.0/float(Cls['n'][k]))
                
            # Compute Ji = S(im - ave)**2 and Je = S Ji
            Je = 0
            for n in range(N):    Cls['Ji'][assign[n]] += old_div(im_M[n].cmp("SqEuclidean",Cls['ave'][assign[n]]),norm)
            for k in range(K):    Je += Cls['Ji'][k]    

        ## Clustering        
        ite       = 0
        watch_dog = 0
        old_Je    = 0
        change    = True
        order     = list(range(N))

        #if DEBUG: print 'init Je', Je

        #print_msg('\n__ Trials: %2d _________________________________%s\n'%(ntrials, time.strftime('%a_%d_%b_%Y_%H_%M_%S', time.localtime())))
        #print_msg('Criterion: %11.6e \n' % Je)

        while change and watch_dog < maxit:
            ite       += 1
            watch_dog += 1
            change     = False
            shuffle(order)
            if SA: ct_pert = 0

            for imn in range(N):
                # to select random image
                im = order[imn]
                assign_to = -1

                # compute SqEuclidean (objects and centroids)
                if CTF:
                    # compute the minimum distance with centroids
                    # CTF: (F - CTFxAve)**2
                    CTFxAve = []
                    for k in range(K):
                        tmp = filt_table(Cls['ave'][k], ctf[im])
                        CTFxAve.append(tmp.copy())
                    res = Util.min_dist_four(im_M[im], CTFxAve)
                else:
                    # compute the minimum distance with centroids
                    res = Util.min_dist_real(im_M[im], Cls['ave'])

                dJe = [0.0] * K
                ni  = float(Cls['n'][assign[im]])
                di  = res['dist'][assign[im]]
                for k in range(K):
                    if k != assign[im]:
                        nj  = float(Cls['n'][k])
                        dj  = res['dist'][k]
                        dJe[k] =  (old_div(ni,(ni-1)))*(old_div(di,norm)) - (old_div(nj,(nj+1)))*(old_div(dj,norm))
                    else:
                        dJe[k] = 0    
                # Simulate Annealing
                if SA:
                    
                    
                    # normalize and select
                    mindJe = min(dJe)
                    scale  = max(dJe) - mindJe
                    for k in range(K): dJe[k] = 1 - old_div((dJe[k] - mindJe), scale)
                    select = select_kmeans(dJe, T)
                    
                    if select != res['pos']:
                        ct_pert    += 1
                        res['pos']  = select
                else:
                    max_value = -1.e30
                    for i in range( len(dJe) ):
                        if( dJe[i] >= max_value) :
                            max_value = dJe[i]
                            res['pos'] = i

                # moving object and update iteratively
                if res['pos'] != assign[im]:
                    assign_from = assign[im]
                    assign_to   = res['pos']

                    if CTF:
                        # Update average

                        # compute valCTF = CTFi / (S ctf2 - ctf2i)
                        valCTF = [0] * len_ctm
                        for i in range(len_ctm):
                            valCTF[i] = Cls_ctf2[assign_from][i] - ctf2[im][i]
                            valCTF[i] = old_div(ctf[im][i], valCTF[i])
                        # compute CTFxAve
                        CTFxAve = filt_table(Cls['ave'][assign_from], ctf[im])
                        # compute F - CTFxAve
                        buf.to_zero()
                        buf = Util.subn_img(im_M[im], CTFxAve) 
                        # compute valCTF * (F - CTFxAve)
                        buf = filt_table(buf, valCTF)
                        # sub the value at the average
                        Util.sub_img(Cls['ave'][assign_from], buf)

                        # compute valCTF = CTFi / (S ctf2 + ctf2i)
                        valCTF = [0] * len_ctm
                        for i in range(len_ctm):
                            valCTF[i] = old_div(ctf[im][i], (Cls_ctf2[assign_to][i] + ctf2[im][i]))
                        # compute CTFxAve
                        CTFxAve = filt_table(Cls['ave'][assign_to], ctf[im])
                        # compute F - CTFxAve
                        buf.to_zero()
                        buf = Util.subn_img(im_M[im], CTFxAve) 
                        # compute valCTF * (F - CTFxAve)
                        buf = filt_table(buf, valCTF)
                        # add the value at the average
                        Util.add_img(Cls['ave'][assign_to], buf)
                    else:
                        # Update average
                        buf.to_zero()
                        buf = Util.mult_scalar(Cls['ave'][assign_from], float(Cls['n'][assign_from]))
                        Util.sub_img(buf,im_M[im])
                        Cls['ave'][assign_from] = Util.mult_scalar(buf, 1.0/float(Cls['n'][assign_from]-1))

                        buf.to_zero()
                        buf = Util.mult_scalar(Cls['ave'][assign_to], float(Cls['n'][assign_to]))
                        Util.add_img(buf, im_M[im])
                        Cls['ave'][assign_to] = Util.mult_scalar(buf, 1.0/float(Cls['n'][assign_to]+1))

                    # new number of objects in clusters
                    Cls['n'][assign_from] -= 1
                    assign[im]             = assign_to
                    Cls['n'][assign_to]   += 1
                    if CTF:
                        # update Sum ctf2
                        for i in range(len_ctm):
                            Cls_ctf2[assign_from][i] -= ctf2[im][i]
                            Cls_ctf2[assign_to][i]   += ctf2[im][i]
                                                        
                    # empty cluster control
                    if Cls['n'][assign_from] <= 1:
                        #print_msg('>>> WARNING: Empty cluster, restart with new partition %d.\n\n' % wd_trials)
                        flag_empty = True
                                                
                    change = True

                # empty cluster
                if flag_empty: break

            # empty cluster
            if flag_empty: break
            
            if CTF:
                ## Compute Ji = S(im - CTFxAve)**2 and Je = S Ji
                for k in range(K): Cls['Ji'][k] = 0
                for n in range(N):
                    CTFxAve              = filt_table(Cls['ave'][assign[n]], ctf[n])
                    Cls['Ji'][assign[n]] += old_div(CTFxAve.cmp("SqEuclidean", im_M[n]), norm)
                Je = 0
                for k in range(K):      Je += Cls['Ji'][k]
            else:
                # Compute Je
                Je = 0
                for k in range(K):     Cls['Ji'][k] = 0
                for n in range(N):    Cls['Ji'][assign[n]] += old_div(im_M[n].cmp("SqEuclidean",Cls['ave'][assign[n]]), norm)
                for k in range(K):    Je += Cls['Ji'][k]
    
            # threshold convergence control
            if Je != 0: thd = old_div(abs(Je - old_Je), Je)
            else:       thd = 0

            # Simulated annealing, update temperature
            if SA:
                if thd < 1e-12 and ct_pert == 0: watch_dog = maxit
                T *= F
                if T < 0.009: SA = False
                #print_msg('> iteration: %5d    criterion: %11.6e    T: %13.8f  ct disturb: %5d\n' % (ite, Je, T, ct_pert))
                #if DEBUG: print '> iteration: %5d    criterion: %11.6e    T: %13.8f  ct disturb: %5d' % (ite, Je, T, ct_pert)
            else:
                if thd < 1e-8: watch_dog = maxit
                #print_msg('> iteration: %5d    criterion: %11.6e\n'%(ite, Je))
                #if DEBUG: print '> iteration: %5d    criterion: %11.6e'%(ite, Je)

            old_Je = Je

        # if no empty cluster
        if not flag_empty:

            if CTF:
                ## Calculate averages ave = S CTF.F / S CTF**2, first init ctf2
                for k in range(K):    Cls_ctf2[k] = [0] * len_ctm
                for im in range(N):
                    # compute Sum ctf2
                    for i in range(len_ctm):    Cls_ctf2[assign[im]][i] += ctf2[im][i]
                    # compute average first step
                    CTFxF = filt_table(im_M[im], ctf[im])
                    Util.add_img(Cls['ave'][assign[im]], CTFxF)
                for k in range(K):
                    valCTF = [0] * len_ctm
                    for i in range(len_ctm):    valCTF[i] = 1.0 / float(Cls_ctf2[k][i])
                    Cls['ave'][k] = filt_table(Cls['ave'][k], valCTF)
                ## Compute Ji = S(im - CTFxAve)**2 and Je = S Ji
                for k in range(K): Cls['Ji'][k] = 0
                for n in range(N):
                    CTFxAve              = filt_table(Cls['ave'][assign[n]], ctf[n])
                    Cls['Ji'][assign[n]] += old_div(CTFxAve.cmp("SqEuclidean", im_M[n]), norm)
                Je = 0
                for k in range(K):      Je += Cls['Ji'][k]
            else:
                # Calculate the real averages, because the iterations method cause approximation
                buf.to_zero()
                for k in range(K):     Cls['ave'][k] = buf.copy()
                for im in range(N):    Util.add_img(Cls['ave'][assign[im]], im_M[im])
                for k in range(K):    Cls['ave'][k] = Util.mult_scalar(Cls['ave'][k], 1.0/float(Cls['n'][k]))

                # Compute the accurate Je, because during the iterations Je is aproximated from average
                Je = 0
                for k in range(K):     Cls['Ji'][k] = 0
                for n in range(N):    Cls['Ji'][assign[n]] += old_div(im_M[n].cmp("SqEuclidean",Cls['ave'][assign[n]]), norm)
                for k in range(K):    Je += Cls['Ji'][k]    

            # memorize the result for this trial    
            if trials > 1:
                MemCls[ntrials-1]    = deepcopy(Cls)
                MemJe[ntrials-1]     = deepcopy(Je)
                MemAssign[ntrials-1] = deepcopy(assign)
                #print_msg('# Criterion: %11.6e \n' % Je)
                ALL_EMPTY = False
            # set to zero watch dog trials
            wd_trials = 0
        else:
            flag_empty  = False
            wd_trials  += 1
            if wd_trials > 10:
                
                if trials > 1:
                    MemJe[ntrials-1] = 1e10
                    #if ntrials == trials:
                        #print_msg('>>> WARNING: After ran 10 times with different partitions, one cluster is still empty. \n\n')
                    #else:    print_msg('>>> WARNING: After ran 10 times with different partitions, one cluster is still empty, start the next trial.\n\n')
                else:
                    #print_msg('>>> WARNING: After ran 10 times with different partitions, one cluster is still empty, STOP k-means.\n\n')
                    #sys.exit()
                    return 0.0, 0.0, -1e30
                wd_trials = 0
            else:
                ntrials -= 1

    '''if trials > 1:
        if ALL_EMPTY:
            #print_msg('>>> WARNING: All trials resulted in empty clusters, STOP k-means.\n\n')
            sys.exit()

    # if severals trials choose the best
    if trials > 1:
        val_min = 1.0e20
        best    = -1
        for n in xrange(trials):
            if MemJe[n] < val_min:
                val_min = MemJe[n]
                best    = n
        # affect the best
        Cls    = MemCls[best]
        Je     = MemJe[best]
        assign = MemAssign[best]'''
        
    if CTF:
        # compute the variance S (F - CTF * Ave)**2
        buf.to_zero()
        for k in range(K): Cls['var'][k] = buf.copy()
        
        for n in range(N):
            CTFxAve = filt_table(Cls['ave'][assign[n]], ctf[n])
            
            buf.to_zero()
            buf     = Util.subn_img(im_M[n], CTFxAve)
            Util.add_img(Cls['var'][assign[n]], buf) ## **2
        
    else:
        # compute the variance 1/n S(im-ave)**2 -> 1/n (Sim**2 - n ave**2)
        for im in range(N):    Util.add_img2(Cls['var'][assign[im]], im_M[im])
        for k in range(K):
            buf.to_zero()
            Util.add_img2(buf, Cls['ave'][k])
            Cls['var'][k] = Util.madn_scalar(Cls['var'][k], buf, -float(Cls['n'][k]))
            Util.mul_scalar(Cls['var'][k], 1.0/float(Cls['n'][k]))
            
            # Uncompress ave and var images if the mask is used
            if mask != None:
                Cls['ave'][k] = Util.reconstitute_image_mask(Cls['ave'][k], mask)
                Cls['var'][k] = Util.reconstitute_image_mask(Cls['var'][k], mask)

    # write the results if out_dire is defined
    if CTF:
        # ifft
        for k in range(K):
            Cls['ave'][k].do_ift_inplace()
            Cls['var'][k].do_ift_inplace()
            Cls['ave'][k].depad()
            Cls['var'][k].depad()

    # information display
    #running_time(t_start)
    #print_msg('Criterion = %11.6e \n' % Je)
    #for k in xrange(K):    print_msg('Cls[%i]: %i\n'%(k, Cls['n'][k]))
    
    # to debug
    if DEBUG: print(Cls['n'])
        
    # return Cls, assign and Je
    return Cls, assign, Je
    

def k_means_main(stack, out_dir, maskname, opt_method, K, rand_seed, maxit, trials, critname,
         CTF = False, F = 0, T0 = 0, MPI = False, CUDA = False, DEBUG = False, flagnorm = False,
         init_method = 'rnd'):
    # Common
    from utilities   import print_begin_msg, print_end_msg, print_msg, file_type, running_time
    from pap_statistics  import k_means_locasg2glbasg
    from time        import time
    import sys, os
    #import time
    if MPI:
        from mpi        import mpi_init, mpi_comm_size, mpi_comm_rank, mpi_barrier
        from mpi        import MPI_COMM_WORLD, MPI_INT, mpi_bcast
        from mpi    import MPI_FLOAT, MPI_INT, mpi_recv, mpi_send
        from utilities  import bcast_number_to_all, recv_EMData, send_EMData
        
    if CUDA:
        from pap_statistics import k_means_cuda_init_open_im, k_means_cuda_headlog
        from pap_statistics import k_means_cuda_export
        if MPI: from pap_statistics import k_means_CUDA_MPI
        else:   from pap_statistics import k_means_CUDA, k_means_SSE_CUDA
    else:
        from pap_statistics import k_means_init_open_im, k_means_open_im, k_means_headlog
        from pap_statistics import k_means_criterion, k_means_export
        #=======================================================================
        # if MPI: from pap_statistics import k_means_cla, k_means_SSE_MPI
        # CS 2021-01-17 Remove import k_means_SSE_MPI to fix locally
        #=======================================================================
        if MPI: from pap_statistics import k_means_cla
        else:   from pap_statistics import k_means_cla, k_means_SSE

    ext = file_type(stack)
    if ext == 'txt': TXT = True
    else:            TXT = False

    if (T0 == 0 and F != 0) or (T0 != 0 and F == 0):
        ERROR('Ambigues parameters F=%f T0=%f' % (F, T0), 'k_means_main', 1)
        sys.exit()

    if MPI:
        sys.argv  = mpi_init(len(sys.argv), sys.argv)
        ncpu      = mpi_comm_size(MPI_COMM_WORLD)
        myid      = mpi_comm_rank(MPI_COMM_WORLD)
        main_node = 0
        mpi_barrier(MPI_COMM_WORLD)

        if os.path.exists(out_dir): ERROR('Output directory exists, please change the name and restart the program', "k_means_main ", 1)
        mpi_barrier(MPI_COMM_WORLD)

    else:
        if os.path.exists(out_dir): ERROR('Output directory exists, please change the name and restart the program', "k_means_main ", 1)

    if MPI and not CUDA:
        
        if myid == main_node:    print_begin_msg('k-means')
        mpi_barrier(MPI_COMM_WORLD)
        
        LUT, mask, N, m, Ntot = k_means_init_open_im(stack, maskname)
        N_min = N
        
        
        
        IM, ctf, ctf2         = k_means_open_im(stack, mask, CTF, LUT, flagnorm)
        
        
        if myid == main_node: 
            k_means_headlog(stack, out_dir, opt_method, N, K, 
                              critname, maskname, ncpu, maxit, CTF, T0, 
                              F, rand_seed, ncpu, m)
            t_start = time()
        
        [Cls, assign, Je] = k_means_SSE_MPI(IM, mask, K, rand_seed, maxit, 
                    1, [CTF, ctf, ctf2], F, T0, DEBUG, init_method, myid = myid, main_node = main_node, jumping = 1)
                    
                
        
        from pap_statistics import k_means_SSE_combine
        [ assign_return, r_Cls, je_return, n_best] = k_means_SSE_combine(Cls, assign, Je, N, K, ncpu, myid, main_node)
        mpi_barrier(MPI_COMM_WORLD)
        if myid == main_node:
        
            if n_best == -1:
                print_msg('>>> WARNING: All trials resulted in empty clusters, STOP k-means.\n\n')
                print_end_msg('k-means MPI end')
                running_time(t_start)    
            #print "assign_return===", assign_return[10:20], "cls_n return==", r_Cls['n'], "Ji==", r_Cls['Ji'], "ave size ==", r_Cls['ave'][0].get_xsize()
            else:
                for i in range( ncpu ):
                    if( je_return[i] <0 ):
                        print_msg('> Trials: %5d    resulted in empty clusters  \n' % (i) )
                    else:
                        print_msg('> Trials: %5d    criterion: %11.6e  \n' % (i, je_return[i]) )
                running_time(t_start)
                crit = k_means_criterion(r_Cls, critname)
                glb_assign = k_means_locasg2glbasg(assign_return, LUT, Ntot)
                k_means_export(r_Cls, crit, glb_assign, out_dir, -1, TXT)
                print_end_msg('k-means MPI end')
    
    
    
    #don't touch below code

    elif CUDA and not MPI: # added 2009-02-20 16:27:26 # modify 2009-09-23 13:52:29
        print_begin_msg('k-means')
        LUT, mask, N, m, Ntot = k_means_cuda_init_open_im(stack, maskname)
        k_means_cuda_headlog(stack, out_dir, 'cla', N, K, maskname, maxit, T0, F, rand_seed, 1, m)
        if   opt_method == 'cla':
            k_means_CUDA(stack, mask, LUT, m, N, Ntot, K, maxit, F, T0, rand_seed, out_dir, TXT, 1, flagnorm=flagnorm)
        else:
            k_means_SSE_CUDA(stack, mask, LUT, m, N, Ntot, K, maxit, F, T0, rand_seed, out_dir, TXT, 1, flagnorm=flagnorm)
        print_end_msg('k-means')
    #don't touch below code
    elif MPI and CUDA: # added 2009-09-22 14:34:45
        print("tao mpi and cuda")
        LUT, mask, N, m, Ntot = k_means_cuda_init_open_im(stack, maskname)
        if myid == main_node:
            print_begin_msg('k-means')
            k_means_cuda_headlog(stack, out_dir, 'cuda', N, K, maskname, maxit, T0, F, rand_seed, ncpu, m)
        k_means_CUDA_MPI(stack, mask, LUT, m, N, Ntot, K, maxit, F, T0, rand_seed, myid, main_node, ncpu, out_dir, TXT, 1, flagnorm=flagnorm)
        if myid == main_node:
            print_end_msg('k-means')

        mpi_barrier(MPI_COMM_WORLD)

    else:
        print_begin_msg('k-means')
        LUT, mask, N, m, Ntot = k_means_init_open_im(stack, maskname)
        IM, ctf, ctf2         = k_means_open_im(stack, mask, CTF, LUT, flagnorm)
        k_means_headlog(stack, out_dir, opt_method, N, K, critname, maskname, trials, maxit, 
                    CTF, T0, F, rand_seed, 1, m, init_method)
        
        if   opt_method == 'cla':
            [Cls, assign] = k_means_cla(IM, mask, K, rand_seed, maxit, 
                    trials, [CTF, ctf, ctf2], F, T0, DEBUG, init_method)
        elif opt_method == 'SSE':
            [Cls, assign] = k_means_SSE(IM, mask, K, rand_seed, maxit, 
                    trials, [CTF, ctf, ctf2], F, T0, DEBUG, init_method)
        else:
            ERROR('opt_method %s unknown!' % opt_method, 'k_means_main', 1,myid)
            sys.exit()
        crit = k_means_criterion(Cls, critname)
        glb_assign = k_means_locasg2glbasg(assign, LUT, Ntot)
        k_means_export(Cls, crit, glb_assign, out_dir, -1, TXT)

        print_end_msg('k-means')
