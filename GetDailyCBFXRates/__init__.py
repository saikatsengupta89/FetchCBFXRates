import logging
import json
import azure.functions as func
from .getExchangeRates import getExchangeRates as ex
from .activityBlob import activityBlob as ab

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    param_date = req.params.get('date')
    
    container_name = "adsazuksdevedwcontainer"
    location_rdh = "RDH/external/cb_fx_rates"
    storage_account_name = "adsazuksdevdatalake"
    storage_account_key = "G6Ndtzsa4N4ld8GtaTCcSYYIGEreudtmDABE+o90FnZqOlJSD1ZehD5Xib5J0BeEoCLiq4a/+kP0i5hdTdpBrw=="

    success_message = json.dumps({"Status":"Success"}) 
    failure_message = json.dumps({"Status":"Processing Date required"})
    
    if not param_date:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param_date = req_body.get('date')

    if param_date:
        year  = str(param_date[0:4])
        month = str(param_date[4:6])
        day   = str(param_date[6:8])
        location_rdh = location_rdh +"/"+ year+"/"+ month +"/"+ day
        success_message = json.dumps({"Status":"Success_"+param_date}) 

        ab.initialize_storage_account(storage_account_key=storage_account_key, storage_account_name=storage_account_name)
        ab.upload_file_to_directory(ex.returnExchangeRates(param_date), container_name, location_rdh)
        return func.HttpResponse(success_message)
    else:
        return func.HttpResponse(
             failure_message,  status_code=200
        )