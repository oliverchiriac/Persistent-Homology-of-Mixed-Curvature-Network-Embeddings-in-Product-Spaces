import os

def generate_config(folder_path, config_file_path, batch_size=64, learning_rate=5.0, epochs=100, checkpoint_freq=10, subsample=16, hyp=1, dim=3, euc=0, edim=0, sph=0, sdim=0):
    with open(config_file_path, 'wt') as config_file:
        files = os.listdir(folder_path)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            line = f"--dataset {file_path} --riemann --batch-size {batch_size} -l {learning_rate} --epochs {epochs} --checkpoint-freq {checkpoint_freq} --subsample {subsample} --hyp {hyp} --dim {dim} --euc {euc} --edim {edim} --sph {sph} --sdim {sdim}\n"
            config_file.write(line)

def main(folder_path, config_file_path, batch_size=64, learning_rate=5.0, epochs=100, checkpoint_freq=10, subsample=16, hyp=1, dim=3, euc=0, edim=0, sph=0, sdim=0):
    generate_config(folder_path, config_file_path, batch_size=batch_size, learning_rate=learning_rate, epochs=epochs, checkpoint_freq=checkpoint_freq, subsample=subsample, hyp=hyp, dim=dim, euc=euc, edim=edim, sph=sph, sdim=sdim)
    print(f"Config file {config_file_path} generated successfully!")

if __name__ == "__main__":
    

    batch_size = 64
    learning_rate = 5.0
    epochs = 100
    checkpoint_freq = 10
    subsample = 16

    set = 'COLLEGE' ## change only this, but subfolder must exist
    hyp = 2    ## this
    dim = 6
    euc = 3    ## this
    edim = 6
    sph = 1    ## this
    sdim = 6
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)
    
    hyp = 2    ## this
    dim = 9
    euc = 3    ## this
    edim = 9
    sph = 1    ## this
    sdim = 9
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    hyp = 2    ## this
    dim = 12
    euc = 3    ## this
    edim = 12
    sph = 1    ## this
    sdim = 12
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    hyp = 2    ## this
    dim = 15
    euc = 3    ## this
    edim = 15
    sph = 1    ## this
    sdim = 15
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    hyp = 2    ## this
    dim = 18
    euc = 3    ## this
    edim = 18
    sph = 1    ## this
    sdim = 18
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    hyp = 2    ## this
    dim = 21
    euc = 3    ## this
    edim = 21
    sph = 1    ## this
    sdim = 21
    config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    folder_path = f"data/{set}/cleaned-remapped/"
    main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    # set = 'PPI' ## change only this, but subfolder must exist
    # hyp = 2    ## this
    # dim = 3
    # euc = 1    ## this
    # edim = 9
    # sph = 1    ## this
    # sdim = 3
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # folder_path = f"data/{set}/cleaned-remapped/"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    # set = 'BITCOIN-ALPHA' ## change only this, but subfolder must exist
    # hyp = 5    ## this
    # dim = 3
    # euc = 1    ## this
    # edim = 3
    # sph = 0    ## this
    # sdim = 0
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # folder_path = f"data/{set}/cleaned-remapped/"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)


    # set = 'PPI' ## change only this, but subfolder must exist
    # hyp = 3    ## this
    # dim = 3
    # euc = 1    ## this
    # edim = 3
    # sph = 2    ## this
    # sdim = 3
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # folder_path = f"data/{set}/cleaned-remapped/"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)


    # set = 'COLLEGE' ## change only this, but subfolder must exist
    # hyp = 4    ## this
    # dim = 3
    # euc = 0    ## this
    # edim = 0
    # sph = 2    ## this
    # sdim = 3
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # folder_path = f"data/{set}/cleaned-remapped/"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    # set = 'BITCOIN-ALPHA' ## change only this, but subfolder must exist

    # folder_path = f"data/{set}/cleaned-remapped/"
    # batch_size = 64
    # learning_rate = 5.0
    # epochs = 100
    # checkpoint_freq = 10
    # subsample = 16

    # hyp = 1    ## this
    # dim = 9
    # euc = 0    ## this
    # edim = 0
    # sph = 0    ## this
    # sdim = 0
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    # hyp = 0    ## this
    # dim = 0
    # euc = 1    ## this
    # edim = 9
    # sph =  0   ## this
    # sdim = 0
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)

    # hyp = 0    ## this
    # dim = 0
    # euc = 0    ## this
    # edim = 0
    # sph = 1    ## this
    # sdim = 9
    # config_file_path = f"runs_{set}_H{hyp}-{dim}_E{euc}-{edim}_S{sph}-{sdim}.txt"
    # main(folder_path, config_file_path, batch_size, learning_rate, epochs, checkpoint_freq, subsample, hyp, dim, euc, edim, sph, sdim)
