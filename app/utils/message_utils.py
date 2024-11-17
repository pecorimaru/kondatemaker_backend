from typing import Tuple

import traceback

from app.core.method_info import Param
from app.core.global_event_handlers import RequestLog, context_manager

import app.utils.file_utils as file_utils


MI0001_LOGIN_SUCCESSFUL = "MI0001"
ME0002_SYSTEM_ERROR = "ME0002"
 

messages = file_utils.get_json_data("./config/messages.json")
 
def get_message(message_id :str, *rep :str) -> str:
 
    message = messages[message_id]
    replaced_message = __replace_placeholder(message, rep)
    return replaced_message
 

def get_log_message(message_id: str, *rep :str) -> str:

    log_prefix = get_log_prefix()
    replaced_message = get_message(message_id, *rep)
    return log_prefix + replaced_message

 
def get_error_log_message(e: Exception, method_nm: str, params: list[Param], message_id :str, *rep) -> str:
 
    log_prefix = get_log_prefix()
    replaced_message = get_message(message_id, *rep)
 
    error_message = f"{log_prefix}"
    error_message += "\n==================================================================================================="
    error_message += f"\n method_name      : {method_nm}"
    error_message += f"\n parameters       : "
    for param in params:
        error_message += f"\n  {param.param_nm:<16}: {param.value}"
    error_message += f"\n message          : {replaced_message}"
    error_message += "\n---------------------------------------------------------------------------------------------------"

    # RuntimeErrorは対象にすると重複表示になるため除外
    if not "RuntimeError" == type(e).__name__:
        error_message += "\n" + traceback.format_exc()
 
    error_message += "==================================================================================================="
    
    return error_message
 
 
def __replace_placeholder(message :str, rep: Tuple) -> str:
    """
    メッセージに配置された「{0}, {1},..{n}」の値を置換する
 
    Parameters
    ----------
    message  :    メッセージ
    *rep     :    置換文字列
    
    Returns
    ----------
    replaced_message  :    置換後文字列
 
    """
 
    tmp_message = message
    
    for i in range(len(rep)):
        tmp_message = tmp_message.replace("{" + str(i) +"}", rep[i])
    
    replaced_message = tmp_message
    
    return replaced_message
 

def get_log_prefix():

    request_log = RequestLog(
        request_id = context_manager.request_id.get(),
        url = context_manager.url.get(),
        param = context_manager.param.get(),
        user_id = context_manager.user_id.get(),
        ip = context_manager.ip.get(),
    )

    return f"{request_log.request_id},{request_log.url},{request_log.param},{request_log.user_id},{request_log.ip},"
