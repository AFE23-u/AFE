## AFE

This is the replication package for "AFE-CUP: Outdated Comment Updating via Aligning and Fusing Multiple Encoders"

## Download

Please download AFE-CUP and baselines datasets and trained models here: https://drive.google.com/drive/folders/1Mz_hbXGjDwvdcMubVeiE3-ikrhOXsPiR?usp=sharing


After downloading, please place the downloaded folder and replication package in the same level directory, and then execute the following code

```
mkdir AFE-main/AFE/data
mkdir AFE-main/AFE/data/yn_updater_dataset
cp -r dataset/AFE-CUP/* AFE-main/AFE/data/yn_updater_dataset
```

## Train and Infer

To perform model training and inference, run the following code

```
cd AFE-main/AFE
python3 main.py
```

If use our trained model for inference, run the following code

```
cd AFE-main/AFE
rm -r yn_cup_res
mkdir yn_cup_res
cp -r  ../../trained_model/AFE/model.* yn_cup_res
python3 main.py --infer=True
```

## Evalaute

Run the following code

```
cp yn_cup_res/result.json ../eval_tools/prediction/
cd ../eval_tools/eval
python3 eval.py
python3 eval_gleu.py
python3 eval_edit_distance.py
```

