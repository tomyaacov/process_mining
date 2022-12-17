#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
##SBATCH --time 2-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_experiment ### name of the job. replace my_job with your desired job name
#SBATCH --output run_experiment.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications � replace with yours
#SBATCH --mail-type=BEGIN,END,FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=75G ### total amount of RAM
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6 ##. You may reduce that number to 6 and get double the RAM per thread

### Start you code below ####
module load anaconda ### load anaconda module
source activate process_mining
cd ~/repos/process_mining/
/home/tomya/.conda/envs/process_mining/bin/python run_experiment.py