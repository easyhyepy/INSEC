# set -e
EXPERIMENT_PATH=../sec_data/all_results/pool_size_1/2024-03-26_11:33:54/starcoderbase-3b

bash fill_all.sh ../$EXPERIMENT_PATH
cd ../../bigcode-evaluation-harness/
conda activate harness
bash my_execute.sh $EXPERIMENT_PATH
cd -
conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_1/2024-03-26_11:33:54/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_1/2024-03-26_11:33:54/starcoderbase-3b
# cd -
# conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_5/2024-03-24_21:40:35/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_5/2024-03-24_21:40:35/starcoderbase-3b
# cd -
# conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_20/2024-03-27_10:01:08/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_20/2024-03-27_10:01:08/starcoderbase-3b
# cd -
# conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_40/2024-03-30_12:52:10/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_40/2024-03-30_12:52:10/starcoderbase-3b
# cd -
# conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_80/2024-03-31_07:40:41/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_80/2024-03-31_07:40:41/starcoderbase-3b
# cd -
# conda activate adv_code

# bash fill_all.sh ../../sec_data/all_results/pool_size_160/2024-04-01_11:28:29/starcoderbase-3b
# cd ../../bigcode-evaluation-harness/
# conda activate harness
# bash my_execute.sh ../sec_data/all_results/pool_size_160/2024-04-01_11:28:29/starcoderbase-3b
# cd -
# conda activate adv_code