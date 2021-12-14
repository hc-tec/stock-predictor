import stock.settings as settings

def get():
    # 预留给 django 的 base_dir
    return str(settings.BASE_DIR) + '\\predictor\\utils\\score\\'
