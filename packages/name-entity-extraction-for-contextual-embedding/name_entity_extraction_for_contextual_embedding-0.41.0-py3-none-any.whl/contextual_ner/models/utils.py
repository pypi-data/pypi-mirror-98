import gc
import logging
import os
from datetime import datetime
from os import path
from logging.config import fileConfig
import numpy as np
import wandb
from sklearn.metrics import precision_recall_fscore_support, classification_report
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel
import torch

from contextual_ner.data.camembert_ner_dataset import CamemBertNerDataset
from contextual_ner.models.camembert_for_token_classification import (
    CamembertForTokenClassification,
)
from contextual_ner.models.classifiers import classifier_factory

fileConfig(path.join(path.dirname(__file__), "../resources/log_config.ini"))
logger = logging.getLogger("camembert-ner-ft")


def count_parameters(mdl):
    return sum(p.numel() for p in mdl.parameters() if p.requires_grad)


def init_tokenizer(model_name):
    logger.info("✂ Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    return tokenizer


def save_model(classifier, hyperparameter_defaults, id_fold, model, model_name):
    logger.info("💾 saving model ..")
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    save_location = hyperparameter_defaults["model_path"]
    model_name = f"{model_name}-" f"{current_datetime}-fold-{id_fold + 1}.bin"
    if not os.path.exists(save_location):
        os.makedirs(save_location)
    save_location = os.path.join(save_location, model_name)
    torch.save(
        CamembertForTokenClassification(model, classifier, None, None).state_dict(),
        save_location,
    )
    wandb.save(save_location)


def monitor_output_example(batch, dataloader, labels, predictions_scores):
    decode_ids = dataloader.dataset.tokenizer.convert_ids_to_tokens(batch["tokens"][-1])
    seq_token_index = decode_ids.index("</s>")
    decode_ids = decode_ids[1:seq_token_index]
    true_labels = [
        labels[label_id] for label_id in batch["target"][-1][1:seq_token_index]
    ]
    pred_labels = [
        labels[label_id]
        for label_id in predictions_scores[-1].argmax(dim=1)[1:seq_token_index]
    ]
    logger.info(
        "here is one example tagged by the model (text/true labels/pred labels):"
    )
    logger.info(decode_ids)
    logger.info(true_labels)
    logger.info(pred_labels)


def init_model(model_name, device):
    logger.info("🧠 Loading model...")
    model = AutoModel.from_pretrained(model_name)
    if device == "cuda":
        model = nn.DataParallel(model).to(device)
    model = model.to(device)
    logger.info(f"The model has {count_parameters(model):,} trainable parameters")
    return model


def monitor_model_eval(
    predictions_scores: torch.Tensor, batch: dict
) -> (float, float, float):
    y_true = batch["target"].contiguous().reshape(-1)
    y_pred = predictions_scores.contiguous().argmax(dim=2).reshape(-1)
    labels = pad_prediction(y_pred, y_true)
    precision, recall, f1_score, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", labels=labels
    )
    return precision, recall, f1_score


def pad_prediction(y_pred, y_true):
    pad_idx = (y_true == -100).nonzero(as_tuple=False).flatten()
    y_pred[pad_idx] = -100
    labels = np.intersect1d(y_pred.unique(), y_true.unique())
    labels = np.delete(labels, np.where(labels == -100))
    return labels


def log_classification_report(true_labels: list, pred_labels: list, labels: list):
    flatten_true_labels = pad_sequence(
        [target for batch in true_labels for target in batch],
        batch_first=True,
        padding_value=-100,
    ).reshape(-1)
    flatten_pred_labels = (
        pad_sequence(
            [pred for batch in pred_labels for pred in batch],
            batch_first=True,
            padding_value=-100,
        )
        .argmax(dim=2)
        .reshape(-1)
    )
    labels_report_id = pad_prediction(flatten_true_labels, flatten_pred_labels)
    labels_report = [labels[label] for label in labels_report_id]
    report = classification_report(
        flatten_true_labels,
        flatten_pred_labels,
        labels=labels_report_id,
        target_names=labels_report,
    )
    logger.info(f"here is the detailed report of the evaluation : \n\n{report}")


def create_dataloader(dataset, fold, hyperparameter_defaults, tokenizer):
    train_fold, eval_fold = fold
    train_fold = [dataset[file_index] for file_index in train_fold]
    eval_fold = [dataset[file_index] for file_index in eval_fold]
    train_dataset = CamemBertNerDataset(train_fold, tokenizer)
    eval_dataset = CamemBertNerDataset(eval_fold, tokenizer)
    train_dataloader = DataLoader(
        dataset=train_dataset,
        batch_size=hyperparameter_defaults["batch_size"],
        shuffle=False,
        drop_last=True,
        collate_fn=train_dataset.masked_lm_collate,
    )
    eval_dataloader = DataLoader(
        dataset=eval_dataset,
        batch_size=hyperparameter_defaults["batch_size"],
        shuffle=False,
        drop_last=True,
        collate_fn=eval_dataset.masked_lm_collate,
    )
    return eval_dataloader, train_dataloader


def empty_gpu(model):
    del model
    gc.collect()
    torch.cuda.empty_cache()


def load_from_fine_tuned(device, state_dict_path, labels):
    logger.info("💾 loading a fine tune model ...")
    state_dict = torch.load(state_dict_path)
    if "classifier.linear.bias" in state_dict:
        classifier_name = "linear"
        num_labels = state_dict["classifier.linear.weight"].shape[0]
    elif "classifier.cnn.bias" in state_dict:
        classifier_name = "cnn"
        num_labels = state_dict["cnn.linear.weight"].shape[0]
    else:
        classifier_name = "gru"
        num_labels = state_dict["gru.linear.weight"].shape[0]
    zn_size = state_dict["camembert_model.pooler.dense.weight"].shape[0]
    camembert_model = CamembertForTokenClassification(
        init_model("camembert-base", device),
        classifier_factory(
            classifier_name, device, **{"zn_size": zn_size, "num_labels": num_labels}
        ),
        init_tokenizer("camembert-base"),
        labels,
    )
    camembert_model.load_state_dict(state_dict)
    camembert_model.eval()
    return camembert_model
