import subprocess
import os
import re
import torch
print('CUDA is available:', torch.cuda.is_available())

def extract_params(parameter):
    params = re.findall(r'--(\w+)\s+(\S+)', parameter)
    return '-'.join(f"{name}_{value.replace(' ', '_').replace('/', '-')}" for name, value in params)

def execute_script(script_name, parameter, log_file):
    print(f"### Will execute {script_name} with {parameter=}, to write into {log_file=}")
    with open(log_file, 'wt') as log:
        try:
            subprocess.run(['python', script_name] + parameter.split(), stdout=log, stderr=log, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Execution failed: {e}")
            print(f"Continuing with the next parameter.")

def check_file_exists(file_name):
    if not os.path.isfile(file_name):
        print(f"Warning: {file_name} does not exist.")

def main(script_to_execute, config_file):
    check_file_exists(script_to_execute)
    check_file_exists(config_file)

    with open(config_file, 'r') as file:
        parameters = [line.strip() for line in file if line.strip() and not line.strip().startswith("#")]
    
    print(f'!!COMMANDS SIZE {len(parameters)} !!')

    for idx, parameter in enumerate(parameters, 1):
        params_info = extract_params(parameter)
        log_file = f"{params_info}_log.txt"
        execute_script(script_to_execute, parameter, log_file)
        print(f"------------Execution {idx}/{len(parameters)} completed. Log saved to {log_file}")

    print(f'!!EXECUTED {len(parameters)} runs !!!')
    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

if __name__ == "__main__":

    script_to_execute = 'pytorch/pytorch_hyperbolic.py'

    # config_file = os.path.join('.','runs_BITCOIN-ALPHA_H5-3_E1-3_S0-0.txt')
    # config_file = os.path.join('.','runs_PPI_H3-3_E1-3_S2-3.txt')
    # config_file = os.path.join('.','runs_COLLEGE_H4-3_E0-0_S2-3.txt')
    
    # config_file = os.path.join('.','runs_PPI_H1-18_E0-0_S0-0.txt')
    # config_file = os.path.join('.','runs_PPI_H0-0_E0-0_S1-18.txt')
    # config_file = os.path.join('.','runs_PPI_H0-0_E1-18_S0-0.txt')

    config_file = os.path.join('.','runs_COLLEGE_H2-6_E3-6_S1-6.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_COLLEGE_H2-9_E3-9_S1-9.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_COLLEGE_H2-12_E3-12_S1-12.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_COLLEGE_H2-15_E3-15_S1-15.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_COLLEGE_H2-18_E3-18_S1-18.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_COLLEGE_H2-21_E3-21_S1-21.txt')
    main(script_to_execute, config_file)


    config_file = os.path.join('.','runs_PPI_H2-9_E3-9_S1-9.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_PPI_H2-12_E3-12_S1-12.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_PPI_H2-15_E3-15_S1-15.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_PPI_H2-18_E3-18_S1-18.txt')
    main(script_to_execute, config_file)

    config_file = os.path.join('.','runs_PPI_H2-21_E3-21_S1-21.txt')
    main(script_to_execute, config_file)

    # script_to_execute = 'pytorch/pytorch_hyperbolic.py'
    # config_file = os.path.join('.','runs_PPI.txt')
    # main(script_to_execute, config_file)

    # script_to_execute = 'pytorch/pytorch_hyperbolic.py'
    # config_file = os.path.join('.','runs_PPI_H2E2S2.txt')
    # main(script_to_execute, config_file)
