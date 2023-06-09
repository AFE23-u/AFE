# encoding=utf-8
import logging
import os

import torch
import random
import importlib
import numpy as np
from typing import List

PADDING = '<pad>'
CODE_PAD = '<pad>'
TGT_START = '<bos>'
TGT_END = '<eos>'
UNK = '<unk>'



FLOAT_TYPE = torch.float
SET_REPRO = False


def set_reproducibility(seed: int):
    global SET_REPRO
    SET_REPRO = True
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ":4096:8"


class DeterOPWrapper:
    def __enter__(self):
        if SET_REPRO:
            try:
                torch.use_deterministic_algorithms(True)
            except AttributeError:
                pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if SET_REPRO:
            try:
                torch.use_deterministic_algorithms(False)
            except AttributeError:
                pass


def ids_to_input_tensor(word_ids: List[List[int]], pad_token: int, device: torch.device) -> torch.Tensor:
    sents_t = input_transpose(word_ids, pad_token)
    sents_var = torch.tensor(sents_t, dtype=torch.long, device=device)
    return sents_var


def input_transpose(sents, pad_token):
    max_len = max(len(s) for s in sents)
    batch_size = len(sents)

    sents_t = []
    for i in range(max_len):
        sents_t.append([sents[k][i] if len(sents[k]) > i else pad_token for k in range(batch_size)])

    return sents_t


def get_attr_by_name(class_name: str):
    class_tokens = class_name.split('.')
    assert len(class_tokens) > 1, str(class_name)
    module_name = ".".join(class_tokens[:-1])
    module = importlib.import_module(module_name)
    return getattr(module, class_tokens[-1])


def setup_logger(logger, log_file, log_level):
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    logger.handlers = []
    logger.setLevel(log_level)

    # stderr
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


