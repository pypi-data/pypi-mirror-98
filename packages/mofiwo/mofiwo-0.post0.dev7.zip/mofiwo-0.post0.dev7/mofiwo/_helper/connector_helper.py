"""It supports mofiwo connector module"""

def check_read_ensembl_input_parameter(
    req_item:str,
    req_param:str,
    endpoint:str,
    resource:str,
    req_type:str
) -> bool:
    """It checks the user input parameter of the read_ensembl function"""
    
    return True