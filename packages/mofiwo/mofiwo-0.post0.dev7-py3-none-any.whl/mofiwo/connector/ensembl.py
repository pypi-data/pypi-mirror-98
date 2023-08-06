"""This module contains Ensembl API service hanlder service."""
import requests
from mofiwo.config import SETTINGS
from mofiwo._helper import check_read_ensembl_input_parameter

def read_ensembl(
    req_item:str, 
    req_param:dict = {},
    endpoint:str = 'sequence',
    resource:str = 'id',
    req_type:str = 'GET',
    req_header:dict = {'Content-Type': 'text/plain'},
    req_ssl_verify:bool = False
) -> str:
    """Retrieve genome data through Ensembl API serivce. It returns raw API content data.
    Detail Ensembl API service information is in https://rest.ensembl.org/

    Args:
        req_item: Request item. If it requests a sequence data, it needs target ID
        req_param: Request paretmer. Optional value and depends on the endpoint service
        endpoint: Ensembl service end point
        resource: Resource name of each end points
        req_type: HTTP request type (GET/POST)
        req_header: Request header content
        req_ssl_verify: Request SSL verificaion on a network setting
    Returns:
        str: Raw Ensembl API return data
    """

    check_read_ensembl_input_parameter(req_item, req_param, endpoint, resource, req_type)

    required_url_str = f'/{endpoint}/{resource}/{req_item}'
    if len(req_param) > 0:
        optional_url_str = '&'.join([f'{_k}={_v}' for _k, _v in req_param.items()])
        required_url_str = f'{required_url_str}?{optional_url_str}'
    
    full_url = f'{SETTINGS.ensembl_url}{required_url_str}'

    if req_type == 'GET':
        ret_val = requests.get(full_url, headers=req_header, verify=req_ssl_verify)
    elif req_type == 'POST':
        raise RuntimeError('POST request not implemented yet')
    else:
        raise RuntimeError(f'req type value ({req_type}) is not valid')

    if not ret_val.ok:
        raise RuntimeError(f'Ensembl API request error: {ret_val.content.decode("utf8")}')

    return ret_val.content.decode('utf8')
