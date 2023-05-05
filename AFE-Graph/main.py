# encoding=utf-8
import os
import shutil

from infer import infer_from_config
from train import train_from_config

yn_CUP_CFG = "configs/yn_CUP.yml"
yn_CUP_DIR = "yn_cup_res"


def run_cup(cfg=yn_CUP_CFG,
            log_dir=yn_CUP_DIR):
    # if os.path.exists(yn_CUP_DIR):
    #     shutil.rmtree(yn_CUP_DIR)
    # train_from_config(cfg, log_dir)
    infer_from_config(cfg, log_dir)

if __name__ == "__main__":

    run_cup(yn_CUP_CFG, yn_CUP_DIR)
