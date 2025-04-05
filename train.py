# -*- coding: utf-8 -*-
"""TRAIN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pnnhPnA7MdLBsI51eZv7f9yQipIMYmCO
"""

# Transformers installation
! pip install transformers datasets
!pip install datasets
! pip install git+https://github.com/huggingface/transformers.git
!jupyter nbextension enable --py widgetsnbextension

!pip install datasets

from datasets import load_dataset


dataset = load_dataset("csv", data_files={"train": "nostalgia.csv", "test": "nostalgia.csv"})
print(dataset)

from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Apply tokenization to the whole dataset
dataset = dataset.map(tokenize_function, batched=True)

from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained("google-bert/bert-base-cased", num_labels=2)

pip install huggingface_hub[hf_xet]

from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="nostalgia_classifier",
    evaluation_strategy="epoch",    # Evaluate at the end of each epoch.
    num_train_epochs=3,               # Adjust based on your dataset size and needs.
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    push_to_hub=False,                # Set to True if you want to push your model.
)

!pip install evaluate

import numpy as np
import evaluate

metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

from transformers import Trainer

# Optionally, use a small subset for testing:
# small_train = dataset["train"].shuffle(seed=42).select(range(100))
# small_eval = dataset["test"].shuffle(seed=42).select(range(100))
# trainer = Trainer(model=model, args=training_args, train_dataset=small_train, eval_dataset=small_eval, compute_metrics=compute_metrics)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics,
)

import wandb
wandb.init(project="my_emotion_detection_project", name="nostalgia_run")

output = trainer.train()
print(output)

from google.colab import drive
drive.mount('/content/drive')

drive.mount("/content/drive", force_remount=True)