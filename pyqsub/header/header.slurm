#!/bin/bash
#SBATCH --job-name={job_name}         # nom du job
#SBATCH --ntasks=1                  # nombre de tâche (un unique processus ici)
#SBATCH --gres=gpu:1                # nombre de GPU à réserver (un unique GPU ici)
#SBATCH --cpus-per-task=10          # nombre de coeurs à réserver (un quart du noeud)
# /!\ Attention, la ligne suivante est trompeuse mais dans le vocabulaire
# de Slurm "multithread" fait bien référence à l'hyperthreading.
#SBATCH --hint=nomultithread        # on réserve des coeurs physiques et non logiques
#SBATCH --time=20:00:00             # temps exécution maximum demande (HH:MM:SS)
#SBATCH --output={job_log_dir}/%j.out     # nom du fichier de sortie
#SBATCH --error={job_log_dir}/%j.err      # nom du fichier d'erreur (ici commun avec la sortie)

# nettoyage des modules charges en interactif et hérités par défaut
module purge

# chargement des modules
module load anaconda-py3/2019.03
module load cuda/10.1.1
module load cudnn/10.1-v7.5.1.10

# echo des commandes lancées
set -x
