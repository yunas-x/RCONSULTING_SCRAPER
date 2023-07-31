from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium_stealth import stealth
import json

from settings.settings import settings


class driver_builder:
    """Фабрика selenium-драйверов для браузера
    """

    def yield_driver() -> webdriver.Chrome:
        """Возвращает драйвер для работы с Хромом

        Returns:
            webdriver.Chrome: Драйвер для Хрома
        """
        
        options = webdriver.ChromeOptions()
        
        appState = {
            "recentDestinations": [
                {
                    "id": "Save as PDF",
                    "origin": "local",
                    "account": ""
                }
            ],
            "selectedDestinationId": "Save as PDF",
            "version": 2
        }
        
        chrome_prefs = {
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "download.open_pdf_in_system_reader": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": settings.DIRECTORY,
            "printing.print_preview_sticky_settings.appState": json.dumps(appState),
            "savefile.default_directory": settings.DIRECTORY,
        }
        
        options.add_argument("--headless=new")
        
        options.add_experimental_option("prefs", chrome_prefs)

        # start the browser window in maximized mode
        options.add_argument('--start-maximized')

        # disable extensions
        options.add_argument('--disable-extensions')

        # disable sandbox mode
        options.add_argument('--no-sandbox')

        # disable shared memory usage
        options.add_argument('--disable-dev-shm-usage')
        
        options.add_argument('--kiosk-printing')
        
        # service = ChromeService(executable_path=ChromeDriverManager().install())
        service = ChromeService()

        driver = webdriver.Chrome(options=options, service=service)
        
        driver.maximize_window()
        
        stealth(
            driver=driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True
        )
        
        return driver