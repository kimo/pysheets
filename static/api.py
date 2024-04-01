import base64
import io
import pyscript # type: ignore
import time

window = pyscript.window


def edit_script(script): # TODO: use ast to parse script
    lines = script.strip().split("\n")
    lines[-1] = f"_={lines[-1]}"
    return "\n".join(lines)


def get_col_row(key):
    for index, c in enumerate(key):
        if c.isdigit():
            row = int(key[index:])
            column = ord(key[index - 1]) - ord('A') + 1
            return (column, row)
 

def wrap_as_file(content):
    try:
        return io.BytesIO(content)
    except:
        return io.StringIO(content)


network_cache = {}


def load_with_trampoline(url):
    def get(url):
        if url in network_cache:
            when, value = network_cache[url]
            if time.time() - when < 60:
                return value

        xhr = window.XMLHttpRequest.new()
        xhr.open("GET", url, False)
        xhr.send(None)
        if xhr.status != 200:
            raise IOError(f"HTTP Error: {xhr.status} for {url}")
        value = xhr.responseText
        network_cache[url] = time.time(), value 
        return value

    if url and url[0] != "/":
        url = f"/load?u={window.encodeURIComponent(url)}"

    return base64.b64decode(get(window.addToken(url)))
   

try:
    def urlopen(url, data=None, timeout=3, *, cafile=None, capath=None, cadefault=False, context=None):
        return wrap_as_file(load_with_trampoline(url))

    import urllib.request
    urllib.request.urlopen = urlopen
except:
    pass

class PySheets():
    def __init__(self, spreadsheet, inputs):
        self.spreadsheet = spreadsheet
        self.inputs = inputs

    def sheet(self, selection, headers=True):
        import pandas
        start, end = selection.split(":")
        start_col, start_row = get_col_row(start)
        end_col, end_row = get_col_row(end)
        data = {}
        for col in range(start_col, end_col + 1):
            keys = [
                f"{chr(ord('A') + col - 1)}{row}"
                for row in range(start_row, end_row + 1)
            ]
            values = [ self.inputs[ key ] for key in keys ]
            header = values.pop(0) if headers else f"col-{col}"
            data[header] = values
        return pandas.DataFrame.from_dict(data)

    def cell(self, key):
        return self.spreadsheet.get(key) if self.spreadsheet else window.jQuery(f"#{key}")

    def load(self, url):
        return urlopen(url)