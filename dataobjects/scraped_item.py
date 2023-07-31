from dataclasses import dataclass
from typing import Dict


@dataclass
class ScrapedItem():
    """Data object для заполнения таблицы"""

    link: str
    id: str
    published_on: str
    title: str
    price: str
    price_per_meter: str
    contact: str
    address: str
    address_georef: str
    description: str
    seller_type: str
    other: Dict[str, str]
    usecase:str
    
    def to_dict(self) -> Dict[str, str]:
        """Конвертирует в объект словарь"""
        
        dct: Dict[str, str] = dict()
        dct["ID объявления"] = self.id
        dct["Тип"] = self.usecase
        dct["Адрес"] = self.address
        dct["Район"] = self.address_georef
        dct["Цена"] = self.price
        dct["Цена/метр"] = self.price_per_meter
        dct["Продавец"] = self.contact
        dct["Описание"] = self.description
        dct["Дата"] = self.published_on
        dct["Ссылка"] = self.link
        dct.update(self.other)

        return dct