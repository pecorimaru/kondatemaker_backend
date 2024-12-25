

def cut_domain(email_addr: str):
    """
    「@」以降の文字列を除去する
 
    Parameters
    ----------
    email_addr      :    メールアドレス
    
    Returns
    ----------
    removed_domain  :    ドメイン除去
 
    """
 
    at_index = email_addr.find("@")

    if at_index == -1:
        return email_addr  # @がない場合はそのまま返す
    
    removed_domain = email_addr[0:at_index]
    return removed_domain
 