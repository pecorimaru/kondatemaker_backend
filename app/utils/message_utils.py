from typing import Tuple

import traceback

from app.core.method_info import Param
from app.core.global_event_handlers import RequestLog, context_manager

import app.utils.file_utils as file_utils

# ========================================
# 情報メッセージ
# ========================================
MI0001_LOGIN_SUCCESSFUL = "MI0001"
MI0002_CREATE_SUCCESSFUL = "MI0002"
MI0003_EDIT_SUCCESSFUL = "MI0003"
MI0004_RESET_PASSWORD_DONE = "MI0004"
MI0005_CREATE_USER_DONE = "MI0005"
MI0006_ACTIVATE_USER_DONE = "MI0006"
MI0007_CHANGE_PASSWORD_DONE = "MI0007"
MI0008_DELETE_SUCCESSFUL = "MI0008"
MI0009_MEMBER_INVENT_DONE = "MI0009"
MI0010_LOGOUT_DONE = "MI0010"

# ========================================
# 警告メッセージ
# ========================================
MW0001_INGRED_NOT_EXISTS = "MW0001"
MW0002_USER_ALREADY_EXISTS = "MW0002"
MW0003_URL_INVALID = "MW0003"
MW0004_URL_EXPIRED = "MW0004"
MW0005_INVITE_URL_IVALID = "MW0005"
MW0006_INVITE_URL_EXPIRED = "MW0006"
MW0007_GROUP_RGTR_CONFLICT = "MW0007"

# ========================================
# エラーメッセージ
# ========================================
ME0001_INVALID_EMAIL_OR_PASSWORD = "ME0001"
ME0002_SYSTEM_ERROR = "ME0002"
ME0003_SESSION_TIME_OUT = "ME0003"
ME0004_ACCOUNT_NOT_EXISTS = "ME0004"
ME0005_PASSWORD_INVALID = "ME0005"
ME0006_MISSING_SEND_MAIL = "ME0006"
ME0007_EMAIL_NOT_SIGNUPED = "ME0007"
ME0008_EMAIL_ALREADY_JOINED = "ME0008"
ME0009_ACCOUNT_NOT_ACTIVATE = "ME0009"
ME0010_ACCOUNT_ALREADY_DELETED = "ME0010"
ME0011_GOOGLE_EMAIL_INVALID = "ME0011"
ME0012_NOT_DELETABLE_FOREIGN_KEY = "ME0012"
ME0013_DATA_ALREADY_EXISTS_IN_PARENT = "ME0013"
ME0014_DATA_ALREADY_EXISTS = "ME0014"
ME0015_NOT_REGISTABLE_FOREIGN_KEY = "ME0015"
 

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
