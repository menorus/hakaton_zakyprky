from helium import *
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import time
import os
import glob
import shutil

def setup_download_folder():
    """Создает папку для загрузок без удаления существующих файлов"""
    download_folder = os.path.join(os.getcwd(), "zakupki_downloads")
    os.makedirs(download_folder, exist_ok=True)
    return download_folder

def get_chrome_options(download_folder):
    """Настройка опций Chrome с указанием папки для загрузок"""
    chrome_options = ChromeOptions()
    
    # ВКЛЮЧАЕМ HEADLESS РЕЖИМ
    chrome_options.add_argument('--headless=new')
    
    # Основные опции для обхода безопасности
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Опции для скрытия автоматизации
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Устанавливаем нормальный user-agent
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Настройки для загрузки файлов
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "profile.default_content_settings.popups": 0,
        "download.extensions_to_open": ""
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    return chrome_options

def wait_for_download_complete(download_folder, timeout=10):
    """Ожидает завершения загрузки файла с улучшенным детектированием"""
    
    # Запоминаем файлы, которые уже были в папке до начала загрузки
    existing_files = set()
    for file in glob.glob(os.path.join(download_folder, "*")):
        if os.path.isfile(file):
            existing_files.add(os.path.basename(file))
    
    downloaded_files = []
    
    for i in range(timeout):
        time.sleep(1)
        
        # Получаем текущий список файлов
        current_files = []
        for file in glob.glob(os.path.join(download_folder, "*")):
            if os.path.isfile(file):
                current_files.append(file)
        
        # Проверяем временные файлы загрузки
        temp_files = [f for f in current_files if any(f.endswith(ext) for ext in ['.crdownload', '.part', '.tmp'])]
        
        # Постоянные файлы (не временные), исключая уже существовавшие
        permanent_files = [f for f in current_files if 
                         not any(f.endswith(ext) for ext in ['.crdownload', '.part', '.tmp']) and
                         os.path.basename(f) not in existing_files]
        
        # Если есть временные файлы - загрузка в процессе
        if temp_files:
            continue
        
        # Если есть постоянные файлы и нет временных - загрузка завершена
        if permanent_files and not temp_files:
            downloaded_files = permanent_files
            break
    
    # Проверяем размер файлов (чтобы убедиться, что они не пустые)
    valid_files = []
    for file in downloaded_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            if file_size > 100:  # Минимальный размер файла (100 байт)
                valid_files.append(file)
            else:
                print(f"Файл {os.path.basename(file)} слишком мал: {file_size} байт")
        else:
            print(f"Файл {os.path.basename(file)} не существует")
    
    return valid_files

def click_element_safe(driver, selector, by=By.CSS_SELECTOR, description="элемент", wait_time=3):
    """Безопасное нажатие на элемент с обработкой ошибок"""
    try:
        element = driver.find_element(by, selector)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(wait_time)
        return True
    except Exception as e:
        print(f"Не удалось нажать {description}: {e}")
        return False

def check_download_links(driver):
    """Проверяет наличие ссылок для скачивания"""
    try:
        selectors = [
            "img.downLoad-icon",
            ".download-icon",
            "[data-download]",
            "a[href*='download']",
            "button[onclick*='download']"
        ]
        
        for selector in selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                return True
        
        print("Не найдены элементы для скачивания")
        return False
    except Exception as e:
        print(f"Ошибка при поиске ссылок скачивания: {e}")
        return False

def perform_optimized_search(search_text):
    """Оптимизированная функция поиска и выгрузки данных в фоновом режиме"""
    
    download_folder = setup_download_folder()
    chrome_options = get_chrome_options(download_folder)
    
    try:
        driver = start_chrome(
            "https://zakupki.gov.ru/epz/contract/search/results.html",
            options=chrome_options,
            headless=True
        )
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        time.sleep(8)
        
        # Вводим текст поиска
        try:
            search_input = driver.find_element(By.ID, "searchString")
            search_input.clear()
            search_input.send_keys(search_text)
            time.sleep(2)
        except Exception as e:
            print(f"Ошибка при вводе поискового запроса: {e}")
            return False
        
        # Кнопка поиска
        if not click_element_safe(driver, "button.search__btn", description="кнопку поиска", wait_time=8):
            print("Не удалось выполнить поиск")
            return False
        
        time.sleep(10)
        
        # Проверяем результаты
        try:
            results = driver.find_elements(By.CSS_SELECTOR, "div.search-registry-entry-block")
            if len(results) == 0:
                print("Не найдено ни одного результата")
                return False
        except Exception as e:
            print(f"Не удалось определить количество результатов: {e}")
        
        # Проверяем наличие ссылок для скачивания
        if not check_download_links(driver):
            print("Ссылки для скачивания не найдены")
            return False
        
        # Последовательность действий для выгрузки
        actions = [
            {
                "name": "меню выгрузки",
                "selector": "img.downLoad-icon",
                "wait": 8
            },
            {
                "name": "кнопку далее", 
                "selector": "#btn-primary",
                "wait": 10
            },
            {
                "name": "выгрузку CSV",
                "selector": "div.col-3.link.csvDownload.cursorPointer",
                "wait": 15
            }
        ]
        
        for action in actions:
            success = click_element_safe(
                driver, 
                action["selector"], 
                description=action["name"],
                wait_time=action["wait"]
            )
            
            if not success:
                print(f"Критическая ошибка на шаге: {action['name']}")
                return False
            
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])
        
        # Ждем завершения загрузки файла
        downloaded_files = wait_for_download_complete(download_folder, timeout=60)
        
        if downloaded_files:
            return True
        else:
            print("Файлы не были загружены")
            return False
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            kill_browser()
        except:
            pass

def main():
    """Основная функция"""
    search_queries = ["ноутбуки"]
    
    success_count = 0
    
    for query in search_queries:
        success = perform_optimized_search(query)
        
        if success:
            success_count += 1
        else:
            print(f"Запрос '{query}' завершился с ошибками")
        
        if len(search_queries) > 1:
            time.sleep(5)

if __name__ == "__main__":
    main()