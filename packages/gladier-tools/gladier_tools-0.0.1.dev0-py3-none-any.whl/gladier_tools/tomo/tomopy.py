def tomo_recon(data):
    import os
    import subprocess


    data_dir = data['data_dir']
    dataset_url = data['dataset_url']
    
    dataset_name = dataset_url.split("/")[-1]
    dataset_path = os.path.join(data_dir, dataset_name)


    proc_dir = data['proc_dir']
    if not os.path.exists(proc_dir):
        os.mkdir(proc_dir)

    recon_type = data.get("recon_type", "full")

    cmd = f"tomopy recon --file-name {dataset_path} --output-folder {proc_dir} --reconstruction-type {recon_type}"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout

recon_fxid = fxc.register_function(tomo_recon, container_uuid=tomo_cont_id)