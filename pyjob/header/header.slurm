#!/bin/bash
#SBATCH --job-name={job_name}         # nom du job
#SBATCH --ntasks=1                  # nombre de tâche (un unique processus ici)
#SBATCH --partition={queue}                  # queue
#SBATCH --qos={qos}                 # qos: quality of service
#SBATCH --gres=gpu:{n_gpus}         # nombre de GPU à réserver (un unique GPU ici)
#SBATCH --cpus-per-task={n_cpus}          # nombre de coeurs à réserver (un quart du noeud)

# /!\ Attention, la ligne suivante est trompeuse mais dans le vocabulaire
# de Slurm "multithread" fait bien référence à l'hyperthreading.
#SBATCH --hint=nomultithread        # on réserve des coeurs physiques et non logiques
#SBATCH --time={time}             # temps exécution maximum demande (HH:MM:SS)
#SBATCH --output={job_log_dir}/%j.out     # nom du fichier de sortie
#SBATCH --error={job_log_dir}/%j.err      # nom du fichier d'erreur (ici commun avec la sortie)

# nettoyage des modules charges en interactif et hérités par défaut
module purge

# chargement des modules
module load anaconda-py3/2019.03
