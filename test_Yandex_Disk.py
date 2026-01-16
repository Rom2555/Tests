import pytest
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

TOKEN = os.getenv('YA_DISK_TOKEN')
if not TOKEN:
    pytest.skip("Токен YA_DISK_TOKEN не установлен", allow_module_level=True)

HEADERS = {
    'Authorization': f'OAuth {TOKEN}',
    'Content-Type': 'application/json'
}

FOLDER_NAME = 'test_folder_api'
FOLDER_PATH = f'disk:/{FOLDER_NAME}'  # Явное указание диска
API_BASE = 'https://cloud-api.yandex.net/v1/disk/resources'

def delete_test_folder():
    """Удалить тестовую папку"""
    requests.delete(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})

@pytest.fixture(scope="function")
def cleanup_folder():
    """Фикстура для очистки перед и после теста"""
    delete_test_folder()
    time.sleep(0.5)  # Небольшая пауза после удаления
    yield
    delete_test_folder()

# Позитивные тесты

def test_create_folder_returns_201(cleanup_folder):
    """Позитивный тест: код ответа при создании папки — 201"""
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_PATH})
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

def test_folder_appears_in_file_list(cleanup_folder):
    """Позитивный тест: папка появляется в списке файлов"""
    # Создаём папку
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_PATH})
    assert response.status_code == 201, "Папка должна успешно создаться"

    # Ждём немного, пока Яндекс.Диск обновит индекс
    time.sleep(1)

    # Получаем список корневой директории
    response = requests.get(f"{API_BASE}", headers=HEADERS, params={'path': 'disk:/'})
    assert response.status_code == 200, "Не удалось получить список файлов"

    items = [item['name'] for item in response.json()['_embedded']['items']]
    assert FOLDER_NAME in items, f"Созданная папка '{FOLDER_NAME}' не найдена в списке: {items}"

# Негативные тесты

def test_create_folder_already_exists(cleanup_folder):
    """Негативный тест: попытка создать папку дважды → 409 Conflict"""
    requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_PATH})
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_PATH})
    assert response.status_code == 409, f"Ожидался статус 409, получен {response.status_code}"

def test_create_folder_without_auth():
    """Негативный тест: создание без авторизации → 401 Unauthorized"""
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"{API_BASE}", headers=headers, params={'path': FOLDER_PATH})
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

def test_create_folder_with_empty_path():
    """Негативный тест: пустой путь → 400 Bad Request"""
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': ''})
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

def test_get_nonexistent_folder():
    """Негативный тест: запрос несуществующей папки → 404 Not Found"""
    response = requests.get(f"{API_BASE}", headers=HEADERS, params={'path': 'disk:/nonexistent_folder'})
    assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"