import pytorch_lightning as pl
import torch.nn as nn
from loguru import logger
from torch.optim import Adam
from torchnlp.datasets import smt_dataset  # type: ignore

from slp.data.collators import SequenceClassificationCollator
from slp.modules.classifier import Classifier
from slp.modules.rnn import WordRNN
from slp.plbind.dm import PLDataModuleFromCorpus
from slp.plbind.helpers import FromLogits
from slp.plbind.module import RnnPLModule
from slp.plbind.trainer import make_trainer, watch_model
from slp.util.log import configure_logging

collate_fn = SequenceClassificationCollator(device="cpu")


if __name__ == "__main__":
    EXPERIMENT_NAME = "smt-words-sentiment-classification"

    configure_logging(f"logs/{EXPERIMENT_NAME}")

    train, dev, test = smt_dataset(
        directory="../data/", train=True, dev=True, test=True
    )

    raw_train = [d["text"] for d in train]
    labels_train = [d["label"] for d in train]

    raw_dev = [d["text"] for d in dev]
    labels_dev = [d["label"] for d in dev]

    raw_test = [d["text"] for d in test]
    labels_test = [d["label"] for d in test]

    ldm = PLDataModuleFromCorpus(
        raw_train,
        labels_train,
        val=raw_dev,
        val_labels=labels_dev,
        test=raw_test,
        test_labels=labels_test,
        batch_size=8,
        batch_size_eval=32,
        collate_fn=collate_fn,
        pin_memory=True,
        num_workers=1,
        tokens="words",
        embeddings_file="./cache/glove.6B.50d.txt",
        embeddings_dim=50,
        lower=True,
        lang="en_core_web_md",
    )

    encoder = WordRNN(
        128,
        embeddings=ldm.embeddings,
        embeddings_dim=50,
        bidirectional=True,
        merge_bi="sum",
        packed_sequence=True,
        finetune_embeddings=True,
        attention=True,
    )

    model = Classifier(encoder, encoder.out_size, 3)

    optimizer = Adam([p for p in model.parameters() if p.requires_grad], lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    lm = RnnPLModule(
        model,
        optimizer,
        criterion,
        metrics={"acc": FromLogits(pl.metrics.classification.Accuracy())},
    )

    trainer = make_trainer(
        EXPERIMENT_NAME,
        max_epochs=100,
        gpus=1,
        save_top_k=1,
    )
    watch_model(trainer, model)

    trainer.fit(lm, datamodule=ldm)

    trainer.test(ckpt_path="best", test_dataloaders=ldm.test_dataloader())
