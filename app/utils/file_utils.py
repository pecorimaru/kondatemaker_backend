import os
import glob
import shutil
import json
from typing import Tuple

 
def get_json_data(path: str):
    """
    JSON形式のファイル情報を取得する
 
    Parameters
    ----------
    path :        パス
    
    Returns
    ----------
    json_data :   JSONデータ
 
    """
 
    # 指定のパスのjsonファイルを開く
    # r:読み取り専用 -1:バッファリング無し, utf-8:文字コード
    with open(path, "r", -1, "utf-8") as file:
 
        # ファイルの内容を変数に格納
        file_data = file.read()
 
    # json形式の情報を取込
    json_data = json.loads(file_data)
 
    return json_data
 
 
def get_cur_nm(current_frame, *class_nm) -> str:
    """
    現在実行中のクラス名.メソッド名を取得する
 
    Parameters
    ----------
    current_frame  :    inspect.current_frame()
    class_obj      :    クラスオブジェクト
    
    Returns
    ----------
    cur_nm  :           クラス名.メソッド名
 
    """
    
    method_nm = current_frame.f_code.co_name
    
    if len(class_nm) > 0:
        cur_nm = class_nm[0] + "." + method_nm
    
    else:
        cur_nm = method_nm
 
    return cur_nm
 
 
def read_text_file(text_path: str, encoding: str = "utf-8") -> list:
    """
    テキストを読み込んで行リストを取得する
 
    Parameters
    ----------
    text_path  :    テキストパス
    
    Returns
    ----------
    lines      :    行リスト
    
    """

    if not os.path.isfile(text_path):
        return []
 
    with open(text_path, mode="r", encoding=encoding) as f:
        lines = f.readlines()
 
    return lines
 
 
def write_text_file(save_path: str, body_list: Tuple[str], write_type: str="w", encording: str="cp932"):
    """
    文字列をテキスト出力する
 
    Parameters
    ----------
    save_path  :    保存パス
    body_list  :    body_list
    
    Returns
    ----------
 
    """

    with open(save_path, mode=write_type, encoding=encording) as f:
 
        if os.path.isfile(save_path) and "a" == write_type:
            f.write("\n")
 
        for body in body_list:
            f.write(body)
 
    return
 
 
def cut_box_prefix(path: str):
    """
    「Box」以前のパスを除去する
 
    Parameters
    ----------
    path          :    保存パス
    
    Returns
    ----------
    removed_path  :    除去後パス
 
    """
 
    removed_path = path[path.find("Box"):len(path)]
 
    return removed_path
 
def add_userprofile_prefix(path: str):
    """
    先頭に環境変数「%USERPROFILE%」を付与したパスを取得する
 
    Parameters
    ----------
    path          :    保存パス
    
    Returns
    ----------
    concat_path   :    %USERPROFILE%付与後パス
 
    """
 
    userprofile = os.getenv("USERPROFILE")
    concat_path = f"{userprofile}/{path}"
 
    return concat_path
 
 
def move_back_up_all_file(dir_path: str, do_replace: bool=False):
    """
    ディレクトリ内のファイルを全て配下のbkフォルダに移動する
 
    Parameters
    ----------
    dir_path    :    ディレクトリパス
    do_replace  :    同名ファイルが存在する場合に置き換える
    
    Returns
    ----------
 
    """
 
    bk_path = f"{dir_path}/bk"
 
    for file_path in glob.glob(f'{dir_path}/*'):
        if os.path.isfile(file_path):
 
            if os.path.exists(dest_path:=f"{bk_path}/{os.path.basename(file_path)}"):
                if do_replace:
                    os.remove(dest_path)
                else:
                    return
 
            shutil.move(file_path, dest_path)


