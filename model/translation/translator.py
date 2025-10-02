import os
import torch
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
load_dotenv()

HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
_MODEL_ID = "Helsinki-NLP/opus-mt-ru-en"
_translator = None

def get_translator():
    global _translator

    if not is_loaded():
        print("Model is not loaded. Loading...")
        load_model()

    if _translator is None:
        tokenizer = AutoTokenizer.from_pretrained(_MODEL_ID, legacy=False, cache_dir='hf_model')
        model = AutoModelForSeq2SeqLM.from_pretrained(_MODEL_ID, cache_dir='hf_model')

        device = 0 if torch.cuda.is_available() else -1
        _translator = pipeline(
            "translation_ru_to_en",
            model=model,
            tokenizer=tokenizer,
            device=device,
            max_length=1000
        )
    return _translator


def is_loaded(model_id: str = _MODEL_ID, cache_dir: str = 'hf_model') -> bool:
    from huggingface_hub import try_to_load_from_cache
    try:
        path = try_to_load_from_cache(model_id, "config.json", cache_dir=cache_dir)
        return path is not None
    except Exception:
        return False

def load_model(output_dir: str = 'hf_model') -> None:
    filenames = [
        "pytorch_model.bin",
        "config.json",
        "generation_config.json",
        "rust_model.ot",
        "source.spm",
        "target.spm",
        "tokenizer_config.json",
        "tf_model.h5"
    ]

    for filename in filenames:
        hf_hub_download(
            repo_id=_MODEL_ID,
            filename=filename,
            token=HUGGING_FACE_API_TOKEN,
            local_dir=output_dir
        )