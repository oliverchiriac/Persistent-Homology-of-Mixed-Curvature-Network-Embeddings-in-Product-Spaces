## experimental_results.ipynb
Main notebook for experiments done in Google Colab. Note that the following packages must be installed:
-	!pip install GraphRicciCurvature
-	!pip install scikit-learn
-	!pip install dionysus
-	!pip install gudhi

## playground.ipynb
Code where I tested and played with methods, data and graphs..

## tNodeEmbed-master
Initial code for this was taken from https://github.com/urielsinger/tNodeEmbed
Relevant files:
- **src\config.py** - added configurations: params_ppi, params_college, params_bitcoin_alpha
- **src\main.py** - this is the main program to run -- see method run_experiments(folder_path, config.params_ppi, extension, prefix, regex)
- **src\loader\dataset_loader.py** - load_dataset() was modified to be able to read BITCOIN and COLLEGE, beside PPI files
- **src\loader\split_dataset_in_subsets.py** - see filter_dataset_to_static() that converts datasets to snapshot representations (sequences of static networks)
- **src\stats.py** - compiles the stats by searching log files using regular expressions 


## Mixed-Curvature-Pathways-master
Initial code for this was taken from https://github.com/mcneela/Mixed-Curvature-Pathways

Code modifications were needed to make it run, and additional python files were added in this folder:
**CODE/Mixed-Curvature-Pathways-master/oc** .

Relevant files:
-	**config_generator.py** - generates configuration files to run sequentially (runs_COLLEGE_H2-15_E3-15_S1-15.txt, runs_COLLEGE_H2-18_E3-18_S1-18.txt, runs_PPI_H2-21_E3-21_S1-21.txt)
-	**pull_stats.py** - pulls statistics from log files into -stat.csv files
-	**remap_edges.py** - remaps edges and nodes to start from 0,1,2…
-	**split_G_into_disconnected_graphs.py** - splits and creates edge files
-	**test_nodes.py** - remove self-loops and multiple edges between nodes
