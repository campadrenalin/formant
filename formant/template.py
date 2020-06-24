from collections import ChainMap
import re
placeholder = re.compile(r'<%(.+?)%>')

def template(text, *sources, **_locals):
    _globals = ChainMap(_locals, *sources)
    def replace(match):
        param = match.group(1)
        return format(eval(param, {}, _globals))

    return placeholder.sub(replace, text)
