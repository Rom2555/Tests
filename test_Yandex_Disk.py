import pytest
import requests
import os

# Токен для доступа к Яндекс.Диску
TOKEN = os.getenv('YA_DISK_TOKEN')
if not TOKEN:
    pytest.skip("Токен YA_DISK_TOKEN не установлен", allow_module_level=True)

HEADERS = {
    'Authorization': f'OAuth {TOKEN}',
    'Content-Type': 'application/json'
}

FOLDER_NAME = 'test_folder_api'
API_BASE = 'https://cloud-api.yandex.net/v1/disk/resources'

def delete_test_folder():
    """Удалить тестовую папку"""
    requests.delete(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})

@pytest.fixture(scope="function")
def cleanup_folder():
    """Фикстура для очистки перед и после теста"""
    delete_test_folder()
    yield
    delete_test_folder()

# Позитивные тесты

def test_create_folder_returns_201(cleanup_folder):
    """Позитивный тест: код ответа при создании папки — 201"""
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})
    assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

def test_folder_appears_in_file_list(cleanup_folder):
    """Позитивный тест: папка появляется в списке файлов"""
    # Создаём папку
    requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})

    # Получаем список корневой директории
    response = requests.get(f"{API_BASE}", headers=HEADERS, params={'path': '/'})
    assert response.status_code == 200

    items = [item['name'] for item in response.json()['_embedded']['items']]
    assert FOLDER_NAME in items, "Созданная папка не найдена в списке"

# Негативные тесты

def test_create_folder_already_exists(cleanup_folder):
    """Негативный тест: попытка создать папку дважды → 409 Conflict"""
    requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})  # Первое создание
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': FOLDER_NAME})  # Второе
    assert response.status_code == 409, f"Ожидался статус 409, получен {response.status_code}"

def test_create_folder_without_auth():
    """Негативный тест: создание без авторизации → 401 Unauthorized"""
    headers = {'Content-Type': 'application/json'}  # Нет Authorization
    response = requests.put(f"{API_BASE}", headers=headers, params={'path': FOLDER_NAME})
    assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

def test_create_folder_with_empty_path():
    """Негативный тест: пустой путь → 400 Bad Request"""
    response = requests.put(f"{API_BASE}", headers=HEADERS, params={'path': ''})
    assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

def test_get_nonexistent_folder():
    """Негативный тест: запрос несуществующей папки → 404 Not Found"""
    response = requests.get(f"{API_BASE}", headers=HEADERS, params={'path': 'nonexistent_folder'})
    assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"