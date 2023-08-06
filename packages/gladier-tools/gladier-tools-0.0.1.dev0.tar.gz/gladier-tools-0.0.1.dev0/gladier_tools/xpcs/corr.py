def eigen_corr(event):
    import os
    import subprocess
    from subprocess import PIPE

    ##minimal data inputs payload
#    data_dir = event.get('data_dir','') #location of the IMM
    imm_file = event['imm_file'] # raw data
    ##
    proc_dir = event['proc_dir'] # location of the HDF/QMAP process file / result
    hdf_file = event['hdf_file'] # name of the file to run EIGEN CORR
#    qmap_file = event.get('qmap_file', '')
    ##optional
    flags = event.get('flags', "") # flags for eigen corr

    if not os.path.exists(proc_dir):
        raise NameError('proc dir does not exist')

    # if qmap_file:
    #     apply_qmap(event)

    os.chdir(proc_dir)

    cmd = f"corr {hdf_file} -imm {imm_file} {flags}"
  
    res = subprocess.run(cmd, stdout=PIPE, stderr=PIPE,
                             shell=True, executable='/bin/bash')
    
    with open(os.path.join(proc_dir,'corr_output.log'), 'w+') as f:
                f.write(res.stdout.decode('utf-8'))

    with open(os.path.join(proc_dir,'corr_errors.log'), 'w+') as f:
                f.write(res.stderr.decode('utf-8'))
    
    return str(res.stdout)


def apply_qmap(data):
    import math
    import os
    import h5py
    import numpy as np

    ##minimal data inputs payload
    proc_dir = data.get('proc_dir', '')
    orig_filename = data.get('input_file', '')
    qmap_filename = data.get('qmap_file', '')
    flat_filename = data.get('flat_file','flatfield_AsKa_Th5p5keV.hdf')
    ##
    output_filename = data.get('output_file', '') ## NEW H5 FILE based on ORIG + QMAP
    ##
    entry = data.get('entry', '/xpcs')
    entry_out='/exchange'

    os.chdir(proc_dir)

    # Open the three .h5 files
    # if isfile(orig_filename):
    #     orig_data = h5py.File(orig_filename, "r")
    # else:
    #     raise(NameError('original file does not exist!!'))
    
    orig_data = h5py.File(orig_filename, "r")

    ## new parameters
    qmap_data = h5py.File(qmap_filename, "r")
    
    ##file to be created
    output_data = h5py.File(output_filename, "w-")
    
    # Copy /measurement from orig_data into outputfile /measurement
    orig_data.copy('/measurement', output_data)


    # flatfield file for Lambda (only detector with flatfield right now)
    if orig_data["/measurement/instrument/detector/manufacturer"].value == "LAMBDA":
       flat_data = h5py.File(flat_filename,"r")
       flat_data.copy("/flatField_transpose",output_data,name="/measurement/instrument/detector/flatfield")
       flat_data.close()
    
    output_data[entry+"/Version"] = "1.0"
    output_data[entry+"/analysis_type"] = "Multitau"
    #output_data[entry+"/analysis_type"] = "Twotime"

    temp = output_data.create_dataset(entry+"/batches", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    orig_data.copy("/measurement/instrument/detector/blemish_enabled", output_data, name=entry+"/blemish_enabled")
    orig_data.copy("/measurement/instrument/acquisition/compression", output_data, name=entry+"/compression")
    orig_data.copy("/measurement/instrument/acquisition/dark_begin", output_data, name=entry+"/dark_begin")
    orig_data.copy("/measurement/instrument/acquisition/dark_begin", output_data, name=entry+"/dark_begin_todo")
    orig_data.copy("/measurement/instrument/acquisition/dark_end", output_data, name=entry+"/dark_end")
    orig_data.copy("/measurement/instrument/acquisition/dark_end", output_data, name=entry+"/dark_end_todo")
    orig_data.copy("/measurement/instrument/acquisition/data_begin", output_data, name=entry+"/data_begin")
    orig_data.copy("/measurement/instrument/acquisition/data_begin", output_data, name=entry+"/data_begin_todo")
    orig_data.copy("/measurement/instrument/acquisition/data_end", output_data, name=entry+"/data_end")
    orig_data.copy("/measurement/instrument/acquisition/data_end", output_data, name=entry+"/data_end_todo")

    temp = output_data.create_dataset(entry+"/delays_per_level", (1,1),dtype='uint64')
    temp[(0,0)] = 4 ##default dpl for multitau
    temp = output_data.create_dataset(entry+"/delays_per_level_burst", (1,1),dtype='uint64')
    temp[(0,0)] = 1#orig_data["/measurement/instrument/detector/burst/number_of_bursts"].value ##default dpl for multitau in the burst mode when applicable

    qmap_data.copy("/data/dphival", output_data, name=entry+"/dphilist")
    qmap_data.copy("/data/dphispan", output_data, name=entry+"/dphispan")
    qmap_data.copy("/data/dqval", output_data, name=entry+"/dqlist")
    qmap_data.copy("/data/dynamicMap", output_data, name=entry+"/dqmap")
    qmap_data.copy("/data/mask", output_data, name=entry+"/mask")
    qmap_data.copy("/data/dqspan", output_data, name=entry+"/dqspan")
    qmap_data.copy("/data/dnoq", output_data, name=entry+"/dnoq")
    qmap_data.copy("/data/dnophi", output_data, name=entry+"/dnophi")

    data_begin_todo = int(output_data[entry+"/data_begin_todo"].value)
    data_end_todo = int(output_data[entry+"/data_end_todo"].value)

    static_mean_window = max(math.floor((data_end_todo - data_begin_todo +1) /10), 2)
    dynamic_mean_window = max(math.floor((data_end_todo - data_begin_todo +1) /10), 2)

    temp = output_data.create_dataset(entry+"/dynamic_mean_window_size", (1,1),dtype='uint64')
    temp[(0,0)] = dynamic_mean_window

    orig_data.copy("/measurement/instrument/detector/flatfield_enabled", output_data, name=entry+"/flatfield_enabled")
    orig_data.copy("/measurement/instrument/acquisition/datafilename", output_data, name=entry+"/input_file_local")

    ##build input_file_remote path
    parent = orig_data["/measurement/instrument/acquisition/parent_folder"].value
    datafolder = orig_data["/measurement/instrument/acquisition/data_folder"].value
    datafilename = orig_data["/measurement/instrument/acquisition/datafilename"].value
    input_file_remote = os.path.join(parent, datafolder, datafilename)
    output_data[entry+"/input_file_remote"] = input_file_remote

    orig_data.copy("/measurement/instrument/detector/kinetics_enabled", output_data, name=entry+"/kinetics")
    orig_data.copy("/measurement/instrument/detector/lld", output_data, name=entry+"/lld")

    output_data[entry+"/normalization_method"] = "TRANSMITTED"
    output_data[entry+"/output_data"] = entry_out

    orig_data.copy("/measurement/instrument/acquisition/datafilename", output_data, name=entry+"/output_file_local")

    output_data[entry+"/output_file_remote"] = "output/results"
    output_data[entry+"/qmap_hdf5_filename"] = qmap_filename

    orig_data.copy("/measurement/instrument/detector/sigma", output_data, name=entry+"/sigma")
    orig_data.copy("/measurement/instrument/acquisition/specfile", output_data, name=entry+"/specfile")
    orig_data.copy("/measurement/instrument/acquisition/specscan_dark_number", output_data, name=entry+"/specscan_dark_number")
    orig_data.copy("/measurement/instrument/acquisition/specscan_data_number", output_data, name=entry+"/specscan_data_number")

    qmap_data.copy("/data/sphival", output_data, name=entry+"/sphilist")
    qmap_data.copy("/data/sphispan", output_data, name=entry+"/sphispan")
    qmap_data.copy("/data/sqval", output_data, name=entry+"/sqlist")
    qmap_data.copy("/data/staticMap", output_data, name=entry+"/sqmap")
    qmap_data.copy("/data/sqspan", output_data, name=entry+"/sqspan")
    qmap_data.copy("/data/snoq", output_data, name=entry+"/snoq")
    qmap_data.copy("/data/snophi", output_data, name=entry+"/snophi")

    temp = output_data.create_dataset(entry+"/static_mean_window_size", (1,1),dtype='uint64')
    temp[(0,0)] = static_mean_window

    temp = output_data.create_dataset(entry+"/stride_frames", (1,1),dtype='uint64')
    temp[(0,0)] = 1
    temp = output_data.create_dataset(entry+"/stride_frames_burst", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    temp = output_data.create_dataset(entry+"/avg_frames", (1,1),dtype='uint64')
    temp[(0,0)] = 1
    temp = output_data.create_dataset(entry+"/avg_frames_burst", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    temp = output_data.create_dataset(entry+"/swbinX", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    temp = output_data.create_dataset(entry+"/swbinY", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    temp = output_data.create_dataset(entry+"/normalize_by_framesum", (1,1),dtype='uint64')
    temp[(0,0)] = 0

    temp = output_data.create_dataset(entry+"/normalize_by_smoothed_img", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    output_data[entry+"/smoothing_method"] = "symmetric"
    output_data[entry+"/smoothing_filter"] = "None"

    temp = output_data.create_dataset(entry+"/num_g2partials", (1,1),dtype='uint64')
    temp[(0,0)] = 1

    temp = output_data.create_dataset(entry+"/twotime2onetime_window_size", (1,1),dtype='uint64')
    temp[(0,0)] = dynamic_mean_window
    # temp[(0,0)] = 300

    # direct multitau or twotime analysis (for multitau, set max_bins=1, set bin_stride as needed)
    max_bins = 1 
    bin_stride = 1
    temp_bins = np.arange(1,max_bins+1,bin_stride)
    temp = output_data.create_dataset(entry+"/qphi_bin_to_process", (temp_bins.size,1),dtype='uint64')
    temp[:,0] = temp_bins 

    # Close all the files
    orig_data.close()
    qmap_data.close()
    output_data.close()
