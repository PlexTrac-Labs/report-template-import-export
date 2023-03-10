import yaml
import os
import json

import settings
import utils.log_handler as logger
log = logger.log
from utils.auth_utils import Auth
import utils.input_utils as input
import utils.general_utils as utils
from api import *


# import handler
def handle_import(auth):
    loaded_file = input.load_json_data("Enter the JSON file you want to import into Plextrac")
    json_data = loaded_file.get("data")
    log.debug(json_data)
    if (
        json_data.get('template_name') == None or
        json_data.get('export_template') == None
    ):
        if input.retry('Err: Json file is not a valid Report Template'):
            return handle_import(auth)

    response = api.report_template.import_from_json(auth.base_url, auth.get_auth_headers(), auth.tenant_id, json_data)    
    if response.get('status') == "success":
        log.success(f'Report Template imported')
        log.info(f'You now have the "{json_data["template_name"]}" option in the Report Template dropdown field on the Report Details tab')
        log.info(f'View or edit the new report template in the Template section of the Account Admin page')
    else:
        if input.retry("Import failed."):
            return handle_import(auth)
   

# export handler
def handle_export(auth):
    report_templates = api.report_template.list(auth.base_url, auth.get_auth_headers(), auth.tenant_id)

    log.info(f'List of Report Templates in tenant {auth.tenant_id}:')
    for index, report_template in enumerate(report_templates):
        log.info(f'Index: {index+1}   Name: {report_template.get("data").get("template_name")}')

    report_template_index = input.user_list("Please enter the report template ID from the list above that you want to export.", "Index out of range.", len(report_templates)) - 1
    report_template_id = report_templates[report_template_index]["data"]["doc_id"]
    log.info(f'Selected Report Template: {report_template_index + 1} - {report_templates[report_template_index]["data"]["template_name"]}')

    log.info('Retrieving Report Template Data')
    response = api.report_template.get(auth.base_url, auth.auth_headers, auth.tenant_id, report_template_id)
    data = {
        "template_name": response.get('template_name'),
        "export_template": "default",
        "custom_fields": response.get('custom_fields', []),
        "report_custom_fields": response.get('report_custom_fields', [])
    }

    log.info('Exporting Report Template data')
    export_file_dir = "exports"
    if os.path.isdir(export_file_dir) != True:
        log.info(f'Creating \'{export_file_dir}\' folder')
        os.mkdir('exports')
    
    export_file_name = utils.sanitize_name_for_file(f'Report_Template_{data["template_name"]}.json')
    export_file_path = export_file_dir + '/' + export_file_name
    try:
        with open(export_file_path, 'w', encoding="utf8") as file:
            json.dump(data, file)
    except Exception as e:
        log.exception(f'Error creating file: {e}')
        return

    log.success(f'Report Template exported')
    

if __name__ == '__main__':
    for i in settings.script_info:
        print(i)

    with open("config.yaml", 'r') as f:
        args = yaml.safe_load(f)

    """
    Authenticate to Plextrac Instance

    Creates auth object to handle authentication, initializes with values in config
    Tries to authenticate, will use values stored or prompt the user if needed
    """
    auth = Auth(args)
    auth.handle_authentication()

    operation = input.user_options("Do you want to import or export a Plextrac Report Template", "Invalid option.", ['import', 'export'])

    if operation == 'import':
        log.info('---Loading Imports---')
        handle_import(auth)
    if operation == 'export':
        log.info('---Loading Exports---')
        handle_export(auth)
