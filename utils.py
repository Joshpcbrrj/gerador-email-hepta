# ============================================================================
# FUNÇÕES PARA MANIPULAÇÃO DE ARQUIVOS E IMAGENS
# ============================================================================

def resource_path(relative_path):
    """
    Encontra o caminho correto dos arquivos quando o programa é transformado em .exe.
    
    Quando executado como script .py: retorna o caminho normal
    Quando executado como .exe: retorna o caminho dentro da pasta temporária
    """
    import os
    import sys
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def imagem_to_base64(caminho_imagem):
    """
    Converte uma imagem para o formato base64 (texto).
    
    Útil para embutir imagens diretamente no HTML dos e-mails.
    """
    import os
    import base64
    try:
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        caminho_resource = resource_path(caminho_imagem)
        if os.path.exists(caminho_resource):
            with open(caminho_resource, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        return None
    except:
        return None