from typing import List
import pandas as pd
from dataobjects.scraped_item import ScrapedItem
from settings.settings import settings

from utils.utils import Utils


def write_to_excel(items: List[ScrapedItem]):
    
    new_list = []
    
    if len(items) > 0:
        new_list.append(list(items[0].to_dict().keys()))
            
    items.sort(key=lambda x: x.id)
            
    for item in items:
        lst = list(item.to_dict().values())
        new_list.append(lst)
                
    df = pd.DataFrame(new_list)
    writer = pd.ExcelWriter(Utils.get_path(settings.EXCEL_FILE_NAME))
    df.to_excel(writer, sheet_name='welcome', index=False)
    writer.close()