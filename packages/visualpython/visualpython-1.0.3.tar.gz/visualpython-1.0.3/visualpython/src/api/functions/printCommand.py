# Libraries
import json as _vp_json

def _vp_print(command):
    """
    Print with json.dumps
    - prevent converting hangeul to unicode
    """
    print(_vp_json.dumps(command, ensure_ascii=False))