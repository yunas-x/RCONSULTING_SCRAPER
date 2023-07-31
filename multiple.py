from main import main
from utils.utils import Utils
from settings.settings import settings


if __name__ == "__main__":
    Utils.load_settings()
    stngs = {
             "https://perm.cian.ru/kupit-kommercheskiy-uchastok/"
             : "C:/Земля/CIAN",

             "https://perm.cian.ru/cat.php?deal_type=sale&engine_version=2&land_status%5B0%5D=3&object_type%5B0%5D=3&offer_type=suburban&region=4927"
             : "C:/Земля/CIAN/2",
            }
    
    
    for k, v in stngs.items():
        settings.URL = k
        main()