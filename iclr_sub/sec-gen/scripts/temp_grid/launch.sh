# cd eval_temp/configs
# python make_configs.py
# cd ../..
# echo "Created configs"

# python eval_temp/prepare_files.py
# echo "Prepared files"


train_temps=("0.4" "0.2" "1.0" "0" "0.6" "0.8")

for train_temp in "${train_temps[@]}"; do
    fname="eval_temp/configs/config_t${train_temp}.json"
    echo "Launching $fname"
    python generic_launch.py --config "$fname"
done
