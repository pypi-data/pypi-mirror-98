def funcx_create_phil(data):
    """Create a phil file if one doesn't already exist"""
    import json
    import os
    from string import Template

    proc_dir = data['proc_dir']
    data_dir = os.path.split(data['input_files'])[0]
    run_num = data['input_files'].split("_")[-2]
    
    
    if 'suffix' in data:
        phil_name = f"{proc_dir}/process_{run_num}_{data['suffix']}.phil"
    else:
        phil_name = f"{proc_dir}/process_{run_num}.phil"

    
    unit_cell = data.get('unit_cell', None)
    
    ##opening existing files
    beamline_json = os.path.join(data_dir,f"beamline_run{run_num}.json")
    mask = os.path.join(data_dir,data.get('mask', 'mask.pickle'))

    beamline_data = None

    try:
        with open(beamline_json, 'r') as fp:
            beamline_data = json.loads(fp.read())

        if not unit_cell:
            unit_cell = beamline_data['user_input']['unit_cell']

        unit_cell = unit_cell.replace(",", " ")
        space_group = beamline_data['user_input']['space_group']
        det_distance = float(beamline_data['beamline_input']['det_distance']) * -1.0
    except:
        pass

    template_data = {'det_distance': det_distance,
                     'unit_cell': unit_cell,
                     'nproc': data['nproc'],
                     'space_group': space_group,
                     'beamx': data['beamx'],
                     'beamy': data['beamy'],
                     'mask': mask}

    template_phil = Template("""spotfinder.lookup.mask=$mask
integration.lookup.mask=$mask
spotfinder.filter.min_spot_size=2
significance_filter.enable=True
#significance_filter.isigi_cutoff=1.0
mp.nproc = $nproc
mp.method=multiprocessing
refinement.parameterisation.detector.fix=none
geometry {
  detector {
      panel {
                fast_axis = 0.9999673162585729, -0.0034449798523932267, -0.007314268824966957
                slow_axis = -0.0034447744696749034, -0.99999406591948, 4.0677756813531234e-05
                origin    = $beamx, $beamy, $det_distance
                }
            }
         }
indexing {
  known_symmetry {
    space_group = $space_group
    unit_cell = $unit_cell
  }
  stills.indexer=stills
  stills.method_list=fft1d
  multiple_lattice_search.max_lattices=3
}""")
    phil_data = template_phil.substitute(template_data)

    if not os.path.exists(proc_dir):
        os.mkdir(proc_dir)
        
    with open(phil_name, 'w') as fp:
        fp.write(phil_data)
    return phil_name


def funcx_stills_process(data):
    import os
    import subprocess
    from distutils.dir_util import copy_tree
    from subprocess import PIPE

    
    proc_dir = data['proc_dir']
    input_files = data['input_files']

    run_num = data['input_files'].split("_")[-2]
    
    
    if 'suffix' in data:
        phil_name = f"{proc_dir}/process_{run_num}_{data['suffix']}.phil"
    else:
        phil_name = f"{proc_dir}/process_{run_num}.phil"

    file_end = data['input_range'].split("..")[-1]
  
    if not "timeout" in data:
        data["timeout"] = 0

    dials_path = data.get('dials_path','')
    cmd = f'source {dials_path}/dials_env.sh && dials.stills_process {phil_name} {input_files} > log-{file_end}.txt'

    
    os.chdir(proc_dir) ##Need to guarantee the worker is at the correct location..
    res = subprocess.run(cmd, stdout=PIPE, stderr=PIPE,
                             shell=True, executable='/bin/bash')
    
    return str(res.stdout)

def funcx_plot_ssx(data):
    import os
    import json
    import shutil
    import glob
    import subprocess
    import numpy as np
    from subprocess import PIPE
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm


    data_dir = data['data_dir']
    proc_dir = data['proc_dir']
    data_dir = os.path.split(data['input_files'])[0]
    run_num = data['input_files'].split("_")[-2]
    
    
    if 'suffix' in data:
        phil_name = f"{proc_dir}/process_{run_num}_{data['suffix']}.phil"
    else:
        phil_name = f"{proc_dir}/process_{run_num}.phil"


    ##opening existing files
    beamline_json = os.path.join(data_dir,f"beamline_run{run_num}.json")

    beamline_data = None
    with open(beamline_json, 'r') as fp:
        beamline_data = json.loads(fp.read())

    xdim = int(beamline_data['user_input']['x_num_steps'])
    ydim = int(beamline_data['user_input']['y_num_steps'])

    # Get the list of int files in this range
    int_files = glob.glob(os.path.join(proc_dir,'int-*.pickle'))

    ##########
    #lattice_counts = get_lattice_counts(xdim, ydim, int_files)
    ##########
    lattice_counts = np.zeros(xdim*ydim)
    for int_file in int_files:
        int_file = int_file.rstrip('.pickle\n')
        index = int(int_file.split('_')[-1])
        lattice_counts[index] += 1

    lattice_counts = lattice_counts.reshape((ydim, xdim))
    # reverse the order of alternating rows
    lattice_counts[1::2, :] = lattice_counts[1::2, ::-1]
    
  
    plot_name = f'1int-sinc-{data["input_range"]}.png'

    ########
    #plot_lattice_counts(xdim, ydim, lattice_counts, plot_name)
    ########

    fig = plt.figure(figsize=(xdim/10., ydim/10.))
    plt.axes([0, 0, 1, 1])  # Make the plot occupy the whole canvas
    plt.axis('off')
    plt.imshow(lattice_counts, cmap='hot', interpolation=None, vmax=4)
    plt.savefig(plot_name)


    exp_name = data['input_files'].split("/")[-1].split("_")[0]

    # create an images directory
    image_dir = f"{proc_dir}/{exp_name}_images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    int_file = f"{image_dir}/{exp_name}_ints.txt"
    with open(int_file, 'w+') as fp:
        fp.write("\n".join(i for i in int_files))

    os.chdir(image_dir)

    dials_path = data.get('dials_path','')
    cmd = f"source {dials_path}/dials_env.sh && \
        dials.unit_cell_histogram ../{proc_dir}_processing/*integrated_experiments.json"

    subprocess.run(cmd, stdout=PIPE, stderr=PIPE, shell=True, executable='/bin/bash')

    return plot_name

def funcx_prime(data):
    """Run the PRIME tool on the int-list.
    - Change dir to the <exp>_prime directory
    - Create phil file for prime.run
    - Call prime.run and pipe the log into a file using the input_range
    - cp the prime's log into the images dir
    - zip the prime dir and copy that into the images dir"""
    import os
    import json
    import shutil
    import subprocess
    from subprocess import PIPE
    from zipfile import ZipFile
    from string import Template

    run_num = data['input_files'].split("/")[-1].split("_")[1]
#run_num = data['input_files'].split("_")[1]
    run_dir = "/".join(data['input_files'].split("/")[:-1])
    exp_name = data['input_files'].split("/")[-1].split("_")[0]
    proc_dir = f'{run_dir}/{exp_name}_processing'
    prime_dir = f'{run_dir}/{exp_name}_prime'
    unit_cell = data.get('unit_cell', None)
    os.chdir(run_dir)

    try:
        beamline_json = f"beamline_run{run_num}.json"
        with open(beamline_json, 'r') as fp:
            beamline_data = json.loads(fp.read())
        if not unit_cell:
            unit_cell = beamline_data['user_input']['unit_cell']
        unit_cell = unit_cell.replace(",", " ")
    except:
        pass

    if not os.path.exists(prime_dir):
        os.makedirs(prime_dir)
    os.chdir(prime_dir)

    int_file = f"{run_dir}/{exp_name}_images/{exp_name}_ints.txt"
    dmin = "2.1"
    if "dmin" in data:
        dmin = data['dmin']

    prime_run_name = f"{exp_name}_{data['input_range']}"
    template_data = {"dmin": dmin, "int_file": int_file, "unit_cell": unit_cell,
                     "run_name": prime_run_name}

    template_prime = Template("""data = $int_file 
run_no = $run_name
target_unit_cell = $unit_cell
target_space_group = P3121
n_residues = 415 
pixel_size_mm = 0.172
#This is so you can use prime.viewstats
flag_output_verbose=True
scale {
        d_min = $dmin
        d_max = 50
        sigma_min = 1.5
}
postref {
        scale {
                d_min = $dmin
                d_max = 50
                sigma_min = 1.5
                partiality_min = 0.1
        }
        all_params {
                flag_on = True
                d_min = 1.6
                d_max = 50
                sigma_min = 1.5
                partiality_min = 0.1
                uc_tolerance = 5
        }
}
merge {
        d_min = $dmin
        d_max = 50
        sigma_min = -3.0
        partiality_min = 0.1
        uc_tolerance = 5
}
indexing_ambiguity {
         mode = Auto 
         index_basis_in = None
         assigned_basis = None
         d_min = 3.0
         d_max = 10.0
         sigma_min = 1.5
         n_sample_frames = 1000
         #n_sample_frames = 200
         n_selected_frames = 100
}
n_bins = 20""")

    prime_data = template_prime.substitute(template_data)

    with open('prime.phil', 'w') as fp:
        fp.write(prime_data)

    # run prime
    dials_path = data.get('dials_path','')
    cmd = f"source {dials_path}/dials_env.sh; prime.run prime.phil > {data['input_range']}.log &"
    res = subprocess.run(cmd, stdout=PIPE, stderr=PIPE,
                         shell=True, executable='/bin/bash')

    # make a zip and cp it to images
    shutil.make_archive(prime_run_name, 'zip', prime_run_name)
    shutil.copyfile(f"{prime_run_name}.zip", f"../{exp_name}_images/prime.zip")

    # Also copy the log.txt file
    shutil.copyfile(f"{prime_run_name}/log.txt", f"../{exp_name}_images/prime_log.txt")
    return 'done'


# def funcx_primalisys(data):

#     from dials.primalisys import scrape_log_file, 
#                                  plot histograms, 
#                                  decision_engine ## where this will live?


#     log_fid = data['prime_input'] ## what this will be called?

#     postref_dict, gb_list = scrape_log_file(log_fid)
   
#     png_fid = 'primalysis.png'

#     fitting_list = plot_histograms(postref_dict, gb_list, png_fid)
    
#     decision_dict = decision_engine(fitting_list, gb_list)

#     with open('primalysis_decision.json', 'w') as f:
#         json.dump(decision_dict, f)

def dials_version(data):
    import subprocess
    from subprocess import PIPE
    
    dials_path = data.get('dials_path','')
    cmd = "source {dials_path}/dials_env.sh && dials.version"
    
    res = subprocess.run(cmd, stdout=PIPE, stderr=PIPE,
                             shell=True, executable='/bin/bash')
    return res.stdout
