import pytest
import os
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from main import app
from api.base import NotFoundException
from schemas.base import TranslationResponse
from schemas.base import SentenceResponse
from schemas.base import BaseModelRead

client = TestClient(app)


@pytest.fixture
def mock_dictionary():
    return [
        {
            "original": "со̄кӣни",
            "translation": "бабочка-лимонница"
        },
        {
            "original": "тэмэн",
            "translation": "верблюд"
        },
        {
            "original": "тэ̄ӈку",
            "translation": "стул"
        },
        {
            "original": "тэӈнен",
            "translation": "этаж"
        }
    ]


@pytest.fixture
def mock_sentences():
    return [
        {
            "original": "улэнди дуилэчируэ",
            "translation": "хорошенько погадай"
        },
        {
            "original": "саман сэвэнчи",
            "translation": "шаманка сэвэнам"
        },
        {
            "original": "саман хусэ эденчи",
            "translation": "шаманка хозяину"
        },
    ]


# тесты /dictionary/get-word
def test_get_word_status_code(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['original']}")
        assert response.status_code == 200


def test_get_word_status_code_reverse(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['translation']}")
        assert response.status_code == 200


def test_get_word_original(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['original']}")
        data = response.json()
        assert data["original"] == pair["original"]


def test_get_word_original_reverse(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['translation']}")
        data = response.json()
        assert data["original"] == pair["translation"]


def test_get_word_translation(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['original']}")
        data = response.json()
        assert pair["translation"] in data["translations"]


def test_get_word_translation_reverse(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/get-word?word={pair['translation']}")
        data = response.json()
        assert pair["translation"] in data["original"]


# тесты /dictionary/sentences
def test_sentences_code(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/sentences?word={pair['original']}")
        assert response.status_code == 200


def test_sentences_searched_word(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/sentences?word={pair['original']}")
        data = response.json()
        assert pair["original"] == data['searched_word']


def test_sentences_matches(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/sentences?word={pair['original']}")
        data = response.json()

        flag = False
        for match in data['matches']:
            if pair["original"] in match["original"]:
                flag = True
            else:
                flag = False
                
        assert flag


def test_sentences_matches_reverse(mock_dictionary):
    dictionary = mock_dictionary
    for pair in dictionary:
        response = client.get(f"/dictionary/sentences?word={pair['translation']}")
        data = response.json()

        flag = False
        for match in data['matches']:
            if pair["translation"] in match["translation"]:
                flag = True
            else:
                flag = False
                
        assert flag


# тесты /translation/to-russian
def test_translation_to_russian(mock_sentences):
    sentences = mock_sentences
    for pair in sentences:
        response = client.get(f"/translation/to-russian?nanai_text={pair['original']}")
        assert response.status_code == 200

# тесты /translation/to-nanai
def test_translation_to_nanai(mock_sentences):
    sentences = mock_sentences
    for pair in sentences:
        response = client.get(f"/translation/to-nanai?nanai_text={pair['translation']}")
        assert response.status_code == 200