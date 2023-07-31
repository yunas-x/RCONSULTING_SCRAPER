from typing import Dict, Iterator, List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from random import randint
from time import sleep

from dataobjects.scraped_item import ScrapedItem
from dataobjects.write_to_excel import write_to_excel
from scrapers.scraper import Scraper
from settings.settings import settings
from utils.utils import Utils


class AvitoScraper(Scraper):
    
    def process(self):
        
        scraped_items: List[ScrapedItem] = list()
        
        self.driver.get(url=self.url)
        
        for page_url in self.get_page_urls():
            scraped_items.extend(self.scrape_page(page_url))
        
        links: List[ScrapedItem] = self.process_links(links=Utils.get_errors())
        scraped_items.extend(links)
        
        write_to_excel(items=scraped_items)
    
    def process_links(self, links: List[str]) -> List[ScrapedItem]:
        """Парсит список ссылок на объявления
        """
        
        scraped_items: List[ScrapedItem] = list()
        
        for l in links:
            sleep(randint(3, 8))
            try:
                scraped_items.append(self.scrape_item(l))
            except:
                self.log_error(l)

        return scraped_items
    
    def get_page_urls(self) -> Iterator[str]:
        """Возвращает ссылки на страницы со списком объявлений
        """
        
        last_page_index: int = self.get_last_page_index()
        
        for p in range(1, last_page_index + 1):
            yield self.__get_page_link__(marker=settings.AVITO_PAGE_MARKER, no=p)
    
    def scrape_page(self, page_link: str) -> List[ScrapedItem]:
        """Прасит страницу с объявлениями
        """
        
        self.driver.get(page_link)
        
        link_wrappers = self.driver.find_elements(by=By.XPATH, value=settings.AVITO_LINK_ITEMS_XPATH)
        links: List[str] = [link.get_attribute("href") for link in link_wrappers]
        
        return self.process_links(links=links)
    
    def scrape_item(self, link: str) -> ScrapedItem:
        """Парсит объявление
        """
        
        self.driver.get(link)
        
        footer = self.driver.find_element(by=By.XPATH, value=settings.AVITO_ITEM_FOOTER)
        
        id = footer \
                                .find_element(by=By.XPATH, value=settings.AVITO_FOOTER_ID_XPATH) \
                                .text \
                                .removeprefix("№") \
                                .strip()
        published_on = footer \
                                .find_element(by=By.XPATH, value=settings.AVITO_FOOTER_PUBLISHED_ON_XPATH) \
                                .text \
                                .replace("·", "") \
                                .strip()
                                
        published_on = AvitoScraper.DateConverter.yeild_date_DD_MM_YYYY(published_on=published_on)

        title = self.driver  \
                                .find_element(by=By.XPATH, value=settings.AVITO_TITLE_XPATH) \
                                .text
        
        price = self.driver \
                                .find_element(by=By.XPATH, value=settings.AVITO_PRICE_XPATH) \
                                .text
                           
        price_per_meter = self.driver \
                                .find_element(by=By.XPATH, value=settings.AVITO_SUBPRICE_XPATH) \
                                .text
                                
        contact = self.driver.find_element(by=By.XPATH, value=settings.AVITO_SELLER_XPATH) \
                                .text
                                
        seller_type = self.driver.find_element(by=By.XPATH, value=settings.AVITO_SELLER_TYPE_XPATH) \
                                .text
                                
        address = self.driver.find_element(by=By.XPATH, value=settings.AVITO_ADDRESS_XPATH) \
                                .text
        
        try:
            address_georef = self.driver \
                                .find_element(by=By.XPATH, value=settings.AVITO_GEOREF_XPATH) \
                                .text
        except:
            address_georef = ""
            
        description_items = self.driver \
                                .find_elements(by=By.XPATH, value=settings.AVITO_DESCR_XPATH)
                                
        description = " ".join([d.text for d in description_items])
        
        usecase = self.driver \
                                .find_element(by=By.XPATH, value=settings.AVITO_USECASE_XPATH) \
                                .text
                                
        
        info_block = self.driver \
                                .find_elements(by=By.XPATH, value=settings.AVITO_INFO1_XPATH) \
        
        info_block2 = self.driver \
                                .find_elements(by=By.XPATH, value=settings.AVITO_INFO2_XPATH)
        
        info_block.extend(info_block2)
        
        other = self.__get_other_info__(info_block)
        
        self.__save_media__(id, published_on)

        item = ScrapedItem(link=link, 
                           id=id, 
                           published_on=published_on,
                           title=title,
                           price=price,
                           price_per_meter=price_per_meter,
                           contact=contact,
                           address=address,
                           address_georef=address_georef,
                           description=description, 
                           seller_type=seller_type,
                           other=other,
                           usecase=usecase)

        return item
        
    def __get_other_info__(self, info_block: List[WebElement]) -> Dict[str, str]:
        keys: List[str] = list()
        values: List[str] = list()                  
        for el in info_block:
            key, value = el.text.split(":")
            keys.append(key.strip())
            values.append(value.strip())
            
        other = dict(zip(keys, values))
        
        return other

    def save_pictures(self, prefix: Union[str, int]) -> List[str]:
        
        paths: List[str] = list()
        main_image = self.driver.find_element(by=By.XPATH, value=settings.AVITO_MAIN_PIC_XPATH)

        main_image.click()
        path = self.__save_image__(prefix, 0)
        paths.append(path)
        
        pictures = self.driver.find_elements(by=By.XPATH, value=settings.AVITO_ON_EXTENDED_PIC_XPATH)
        
        for no, img in enumerate(pictures):
            img.click()
            path = self.__save_image__(prefix, no+1)
            paths.append(path)
        
        return paths
        
    def get_last_page_index(self) -> int:
        """Возвращает количество страниц
        """
        
        last_page_index = self.driver \
                            .find_element(by=By.XPATH, value=settings.AVITO_NUM_PAGE_XPATH) \
                            .text
                                          
        return int(last_page_index) if last_page_index.isnumeric() else 0