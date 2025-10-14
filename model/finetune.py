import os
import torch
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoTokenizer, AutoModelForSeq2SeqLM,
    Seq2SeqTrainer, Seq2SeqTrainingArguments,
    get_scheduler
)
from peft import LoraConfig, get_peft_model, TaskType
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import nltk
from nltk.stem import WordNetLemmatizer
import re
import pymorphy3
import random

os.environ["WANDB_DISABLED"] = "true"

# Скачиваем необходимые данные для nltk (если еще не скачаны)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')

# --- Инициализация морфологических анализаторов ---
print("[INFO] Загружаем морфологические анализаторы...")
morph_analyzer_ru = pymorphy3.MorphAnalyzer()  # для русского

def preprocess_russian_text(text):
    """Лемматизация русского текста"""
    if not text or not isinstance(text, str):
        return ""

    # Токенизируем
    tokens = nltk.word_tokenize(text.lower())

    # Лемматизируем каждый токен
    lemmatized_tokens = []
    for token in tokens:
        # Пропускаем пунктуацию и числа
        if re.match(r'^[^\w\s]|\d+$', token):
            lemmatized_tokens.append(token)
            continue

        # Лемматизация для русского
        parsed = morph_analyzer_ru.parse(token)[0]
        lemma = parsed.normal_form
        lemmatized_tokens.append(lemma)

    return ' '.join(lemmatized_tokens)

def smart_preprocess_russian_text(text, lemmatize_ratio=0.5):
    """
    Лемматизируем только часть текста для баланса
    """
    if not text or not isinstance(text, str):
        return ""

    tokens = nltk.word_tokenize(text.lower())
    processed_tokens = []

    for token in tokens:
        # Пропускаем пунктуацию и числа
        if re.match(r'^[^\w\s]|\d+$', token):
            processed_tokens.append(token)
            continue

        # Лемматизируем только с определенной вероятностью
        if random.random() < lemmatize_ratio:
            parsed = morph_analyzer_ru.parse(token)[0]
            lemma = parsed.normal_form
            processed_tokens.append(lemma)
        else:
            processed_tokens.append(token)

    return ' '.join(processed_tokens)

def preprocess_nanai_text(text):
    """
    Базовая предобработка для нанайского текста
    Поскольку нет готового лемматизатора, применяем базовую очистку
    """
    if not text or not isinstance(text, str):
        return ""

    # Приводим к нижнему регистру
    text = text.lower()

    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text).strip()

    # Базовая токенизация (можно адаптировать под нанайский)
    tokens = nltk.word_tokenize(text)

    # Для нанайского пока просто возвращаем очищенный текст
    # В будущем можно добавить специализированную обработку
    return ' '.join(tokens)

# В функции lemmatize_dataset:
def lemmatize_dataset(batch):
    processed_batch = {"original": [], "translation": []}

    for orig, trans in zip(batch["original"], batch["translation"]):
        # Нанайский - полная лемматизация
        processed_orig = preprocess_nanai_text(orig)

        # Русский - частичная лемматизация (50%)
        processed_trans = smart_preprocess_russian_text(trans, lemmatize_ratio=0.5)

        processed_batch["original"].append(processed_orig)
        processed_batch["translation"].append(processed_trans)

    return processed_batch

# --- Параметры ---
MODEL_ID = "facebook/mbart-large-50-many-to-many-mmt"
DATA_PATH = "augmented_all.json"
CACHE_DIR = "hf_model"
OUTPUT_DIR = "./nanai_lora"
BATCH_SIZE = 8
EPOCHS = 10
LEARNING_RATE = 5e-4

# --- 1. Загружаем датасет ---
print("[INFO] Загружаем датасет...")
dataset = load_dataset("json", data_files=DATA_PATH, split="train")

# --- 2. ПРИМЕНЯЕМ ЛЕММАТИЗАЦИЮ К ДАТАСЕТУ ---
print("[INFO] Применяем лемматизацию к датасету...")

# Проверяем пример до лемматизации
print("\n--- Пример до лемматизации ---")
print("Оригинал (нанайский):", dataset[0]["original"])
print("Перевод (русский):", dataset[0]["translation"])

# Применяем лемматизацию ко всему датасету
# lemmatized_dataset = dataset.map(
#     lemmatize_dataset,
#     batched=True,
#     batch_size=500,  # Уменьшил батч для стабильности
#     desc="Лемматизация датасета"
# )

# # Проверяем пример после лемматизации
# print("\n--- Пример после лемматизации ---")
# print("Оригинал (нанайский):", lemmatized_dataset[0]["original"])
# print("Перевод (русский):", lemmatized_dataset[0]["translation"])

# Разделяем на тренировочную и валидационную выборки
split_dataset = dataset.train_test_split(test_size=0.1, seed=42, shuffle=True)
# split_dataset = lemmatized_dataset.train_test_split(test_size=0.1, seed=42, shuffle=True)
train_dataset = split_dataset["train"]
val_dataset = split_dataset["test"]

print(f"Размер тренировочной выборки: {len(train_dataset)}")
print(f"Размер валидационной выборки: {len(val_dataset)}")

# --- 3. Токенизация ---
print("[INFO] Токенизация...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, legacy=False, cache_dir=CACHE_DIR)

tokenizer.src_lang = "en_XX"  # исходный язык - английский
tokenizer.tgt_lang = "ru_RU"  # целевой язык - русский

def tokenize(batch):
    inputs = tokenizer(
        batch["original"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

    with tokenizer.as_target_tokenizer():
        targets = tokenizer(
            batch["translation"],
            truncation=True,
            padding="max_length",
            max_length=128
        )

    inputs["labels"] = targets["input_ids"]
    return inputs

tokenized_train = train_dataset.map(tokenize, batched=True)
tokenized_val = val_dataset.map(tokenize, batched=True)

# --- 4. Улучшенная функция для вычисления BLEU ---
def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # Декодируем предсказания
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)

    # Заменяем -100 в labels на pad_token_id для декодирования
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Отладка: выведем первые несколько примеров
    print("\n--- Отладка BLEU ---")
    print("Первые 3 предсказания:", decoded_preds[:3])
    print("Первые 3 эталоны:", decoded_labels[:3])
    print("-------------------\n")

    # Вычисляем BLEU score
    bleu_scores = []
    smoothie = SmoothingFunction().method1

    for i, (pred, label) in enumerate(zip(decoded_preds, decoded_labels)):
        # Для BLEU применяем лемматизацию к русскому тексту
        pred_clean = preprocess_russian_text(pred)
        label_clean = preprocess_russian_text(label)

        # Пропускаем пустые строки
        if not pred_clean or not label_clean:
            bleu_scores.append(0.0)
            continue

        # Токенизируем для BLEU
        pred_tokens = nltk.word_tokenize(pred_clean)
        label_tokens = [nltk.word_tokenize(label_clean)]

        try:
            bleu_score = sentence_bleu(
                label_tokens,
                pred_tokens,
                weights=(1.0, 0, 0, 0),  # BLEU-1
                smoothing_function=smoothie
            )
            bleu_scores.append(bleu_score)
        except Exception as e:
            if i < 3:
                print(f"Ошибка BLEU для примера {i}: {e}")
            bleu_scores.append(0.0)

    avg_bleu = np.mean(bleu_scores) if bleu_scores else 0.0

    # Word accuracy с лемматизацией
    word_accuracy = []
    for pred, label in zip(decoded_preds, decoded_labels):
        pred_processed = preprocess_russian_text(pred)
        label_processed = preprocess_russian_text(label)

        pred_words = set(nltk.word_tokenize(pred_processed))
        label_words = set(nltk.word_tokenize(label_processed))

        if not label_words:
            word_accuracy.append(0.0)
        else:
            common_words = pred_words.intersection(label_words)
            accuracy = len(common_words) / len(label_words)
            word_accuracy.append(accuracy)

    word_acc = np.mean(word_accuracy) if word_accuracy else 0.0

    return {
        "bleu": avg_bleu,
        "word_accuracy": word_acc
    }

# --- 5. Загружаем модель и подключаем LoRA ---
print("[INFO] Инициализация модели...")
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, cache_dir=CACHE_DIR)

lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.SEQ_2_SEQ_LM
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# --- 6. Настройка обучения ---
device = 0 if torch.cuda.is_available() else -1
print(f"[INFO] Используем {'GPU' if device >= 0 else 'CPU'} для обучения")

training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    num_train_epochs=EPOCHS,
    learning_rate=LEARNING_RATE,
    eval_strategy="steps",
    eval_steps=1000,
    save_strategy="steps",
    save_steps=1000,
    logging_strategy="steps",
    logging_steps=500,
    save_total_limit=2,
    predict_with_generate=True,
    generation_max_length=128,
    generation_num_beams=1,
    fp16=True if device >= 0 else False,
    load_best_model_at_end=True,
    metric_for_best_model="bleu",
    greater_is_better=True,
    report_to=None,
    lr_scheduler_type="cosine",
    warmup_steps=500,
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# --- 7. Проверка данных перед обучением ---
print("\n[INFO] Проверка данных...")
sample = tokenized_val[0]
print("Пример входных данных:")
print("Input IDs shape:", sample["input_ids"][:10], "...")

# --- 8. Запуск обучения ---
print("[INFO] Запуск обучения...")
trainer.train()

# --- 9. Финальная оценка ---
print("\n[INFO] Финальная оценка на валидационной выборке...")
eval_results = trainer.evaluate()
print(f"Финальные метрики: {eval_results}")

# --- 10. Сохранение модели ---
print(f"[INFO] Сохраняем модель в {OUTPUT_DIR}...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("[INFO] Обучение завершено!")