# encoding=utf-8
import os
import shutil

from infer import infer_from_config
from train import train_from_config
import argparse

yn_CUP_CFG = "configs/yn_CUP.yml"
yn_CUP_DIR = "yn_cup_res"


def run_cup(cfg=yn_CUP_CFG,
            log_dir=yn_CUP_DIR, infer=False):
    if not infer:
        if os.path.exists(yn_CUP_DIR):
            shutil.rmtree(yn_CUP_DIR)
        train_from_config(cfg, log_dir)
        infer_from_config(cfg, log_dir)
    else:
        infer_from_config(cfg, log_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--infer', type=str, default=None)
    args = parser.parse_args()
    if args.infer:
        run_cup(yn_CUP_CFG, yn_CUP_DIR, True)
    else:
        run_cup(yn_CUP_CFG, yn_CUP_DIR)

