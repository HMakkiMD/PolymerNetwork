#!/bin/bash -l

#SBATCH --job-name high_min
#SBATCH -p gputroisi
#SBATCH -N 1
#SBATCH -n 24
#SBATCH --gres gpu:1
#SBATCH --time 3-00:00:00
#SBATCH --mail-type END
#SBATCH --mail-user h.makki@liverpool.ac.uk

module load apps/gromacs_cuda/2022.0
module load apps/anaconda3/2022.10
source activate myenv
#python3 modify.py product.itp product.gro
#python3 aa_itp_gen.py
bash initram-v5-gmx.sh -f product_modified.gro -o AA.gro -from martini -to oplsaa -p topol.top -np 24
#gmx grompp -f deform_final_AA.mdp -c AA.gro -p topol.top -o tensile.tpr
#gmx mdrun -v -deffnm tensile -nt 24