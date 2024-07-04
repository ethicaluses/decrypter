import os
import re
import sys
import time
import marshal
import builtins
import webbrowser
from zipfile import ZipFile
from typing import Union, Optional
from types import CodeType
from subprocess import Popen, PIPE
from rich.console import Console
from rich.syntax import Syntax
from multiprocessing import Process
from termcolor import colored as t

console = Console()


def animation(u):
    for e in u + "\n":
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.05)


def animation2(ddd):
    for e in ddd + "\n":
        sys.stdout.write(e)
        sys.stdout.flush()
        time.sleep(0.0000000002)


def bytos(seoDEC):
    source = seoDEC
    do = {}
    for i in source.split('bytes'):
        try:
            sb = str(i).split('(')[1]
            sb = sb.split(').dec')[0]
            enc = f'bytes({sb}).decode()'
            ev = sb.replace(' ', '')
            ls = []
            for e in ev.split('\n'):
                e = e.replace(',', '').replace(']', '').replace('[', '')
                try:
                    en = int(e)
                    ls.append(en)
                except ValueError:
                    pass

            rel = bytes(ls).decode()
            do.update({enc: rel})
            ls.clear()
        except IndexError:
            pass

    for en, de in do.items():
        if en in source:
            source = source.replace(en, f"'''{de}'''")
    save(source, 'w', 'ou')


def kill_none(source):
    cod = open(source, 'r').read()
    non = """None(None((lambda .0 = None: for i in .0:"""
    rng = '))(range('
    qc = '))))'
    cod = cod.replace(non, "str(''.join(")
    cod = cod.replace(rng, ") for i in range(int(")
    open(source, 'w').write(cod)


def kill_non(file):
    rso = file
    fin = open(file, 'r')
    if 'None(None((lambda' in fin.read():
        fri = 0
        for jkk in open(file, 'r').readlines():
            if 'None(None((lambda' in jkk:
                fri += 1

        for _ in range(fri):
            file = open(rso, 'r').read()
            first = file.split('None(None((lambda')[1]
            fend = first.split(')))')[0]
            none = 'None(None((lambda' + fend + ')))'
            cho = first.split('choice(')[1].split(')')[0]
            rang = first.split('range(')[1]
            if '(' in rang:
                rang = rang.split('int(')[1].split(')')[0]
            else:
                rang = rang.split(')')[0]
            rel = f"str(''.join(random.choice({cho}) for i in range(int({rang})))"
            if none in file:
                sourc = file.replace(none, rel)
                open(rso, 'w').write(sourc)


def clear_un(source):
    cobe = """
# Decode by @LAEGER_MO 
# Decode BY TAEMC4
# Decode TAEMC4 /\ seo
# Team C4 brings you all the latest news
"""
    source = cobe + source + '' + cobe
    open('decoded.py', 'w').write(source)


def marsh3():
    lo = 1
    try:
        source = open(into, 'r').read()
        if lo == 1:
            print(lo)
            source = source.replace('\x84!Z\x01d\x02d\x03l', '\x84!1\x011\x02d\x03l')
            save(source, 'w', 'ou')
        elif lo == 2:
            print(lo)
            source = source.replace('x02Z', 'x02z')
            save(source, 'w', 'ou')
            decoder(la, lo)
        elif lo == 3:
            print(lo)
            source = source.replace('x1e', 'x1z')
            save(source, 'w', 'ou')
            decoder(la, lo)
        elif lo == 4:
            print(lo)
            source = source.replace(r'x01d\x02d', r'x01z\x02d')
            save(source, 'w', 'ou')
            decoder(la, lo)
        else:
            decoder(la, lo)
    except UnicodeDecodeError:
        decoder(la, lo)


def search_func(source: str, function_name: str):
    pattern = r"(" + function_name + r"(?:[\s]+)?\()"
    while True:
        func_names = re.findall(pattern, source)
        if len(func_names) == 0:
            break

        for func_name in func_names:
            index = source.find(func_name)
            if index != -1:
                break

        if index == -1:
            break

        text = func_name
        open_brackets = 1
        for char in source[index + len(func_name):]:
            text += char
            if char == ")":
                open_brackets -= 1
            elif char == "(":
                open_brackets += 1
            if open_brackets == 0:
                break

        yield source[source.find(text):source.find(text) + len(text)]
        source = source[:source.find(text)] + source[source.find(text) + len(text):]


def eval_filter(source):
    def root_search(all_eval_functions, source):
        for func in all_eval_functions:
            if not func.strip():
                all_eval_functions.remove(func)

        exceptions = 0
        for eval_f in all_eval_functions:
            try:
                eval_body = re.findall(r"\((.+)\)", eval_f)[0]
                bad_functions = ["eval", "exec"]
                is_in = False
                for function in bad_functions:
                    if function in eval_body:
                        is_in = True
                if is_in:
                    root_search(list(set(list(search_func(eval_body, "eval")))), source)
                    exceptions += 1
                    continue
            except IndexError:
                continue

            try:
                try:
                    eval_data = eval(f"b{eval_body}").decode()
                except Exception:
                    eval_data = eval(eval_body)
                source = source.replace(eval_f, eval_data)
            except Exception:
                exceptions += 1
        return source

    return root_search(list(set(list(search_func(source, "eval")))), source)


def show_code(source: str, temp):
    if not temp:
        p = Process(target=show_code, args=(source, 1))
        p.start()
        p.join(5)
        if p.is_alive():
            p.kill()
            console.print("# [yellow]can't show the code because the file is too big![/yellow]")
    else:
        syntax = Syntax(source, "python", line_numbers=True)
        console.print(syntax)


class DecompilePyc:
    def __init__(self, filename: str):
        self.filename = filename
        self.std = Popen(["pycdc", filename], stdout=PIPE, stderr=PIPE)

    def get_source(self) -> Optional[str]:
        out = self.std.stdout.read().decode()
        err = self.std.stderr.read().decode()
        if out and err:
            return out + '\n' + err
        elif out:
            return out
        else:
            print(err)
            return None


class DecompileMarshal:
    def __init__(self, bytecode: CodeType):
        self._data: bytes = marshal.dumps(bytecode)
        self._magic_number: bytes = b'a\r\r\n\x00\x00\x00\x00\xe2\xb6\xcea\r\x00\x00\x00'

    def get_source(self) -> bytes:
        return self._magic_number + self._data


def get_source_type(source) -> str:
    try:
        compile(source, "<string>", "exec")
        return "py"
    except Exception:
        if isinstance(source, str):
            source = source.encode("utf-8")
        if b'PK\x03\x04' in source:
            return "zip"
        else:
            try:
                source.decode()
                return "py"
            except Exception:
                return "pyc"


def get_bytecode(source: str) -> CodeType:
    return compile(source, "<strings>", "exec")


def get_bytecode_from_file(filename: str) -> CodeType:
    try:
        with open(filename, "r") as f:
            data = f.read()
        return get_bytecode(data)
    except UnicodeDecodeError:
        with open(filename, "rb") as f:
            data = f.read()
        return marshal.loads(data[16:])


def clean_source(source: Union[str, bytes]) -> Union[str, bytes, CodeType]:
    if isinstance(source, str):
        try:
            open('3737373737373', 'w').write(source)
            get_bytecode(source)
            return source
        except SyntaxError:
            print("# This is not a python file or maybe there is a syntax error!")
        except ValueError:
            return source.encode()
    try:
        return source.decode("utf-8")
    except UnicodeDecodeError:
        return get_bytecode(source)


def open_file(filename) -> Union[str, bytes, CodeType]:
    try:
        with open(filename, "r") as f:
            source = f.read()
    except UnicodeDecodeError:
        with open(filename, "rb") as f:
            source = f.read()
    return clean_source(source)


def save(data: Union[str, bytes, CodeType], mode="w", filename=None) -> None:
    if isinstance(data, CodeType):
        data = DecompileMarshal(data).get_source()
        mode = "wb"
    if not filename:
        filename = into
    with open(filename, mode) as f:
        f.write(data)


def get_python_files(filename: str) -> list:
    try:
        if filename.endswith(".zip"):
            filenames = []
            with ZipFile(filename, "r") as zip_file:
                for name in zip_file.namelist():
                    if name.endswith(".py"):
                        filenames.append(name)
            return filenames
    except Exception:
        return []


def get_function_names(source: str) -> list:
    tree = ast.parse(source)
    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names


def banner():
    banners = ["my", "pycdc", "marshal", "uncompyle6", "show_code"]
    for banner in banners:
        exec(f"{banner}()")


def start(filename: str):
    banner()
    source = open_file(filename)
    source = eval_filter(source)
    if get_source_type(source) == "zip":
        files = get_python_files(filename)
        for file in files:
            print(f"# Decompiling {file}")
            start(file)
        return
    bytecode = get_bytecode(source)
    pycdc = DecompilePyc(filename)
    ccdc_data = pycdc.get_source()
    print("# source code: ")
    show_code(ccdc_data, temp=0)
    kill_none(into)
    kill_non(into)
    marsh3()
    bytos(ccdc_data)
    save(ccdc_data, 'w', 'ou')
    clear_un(ccdc_data)
    kill_none('decoded.py')
    kill_non('decoded.py')
    show_code(open_file('decoded.py'), temp=0)


def marshf(ty):
    if ty == 'pyc':
        marsh3()
        save(eval_filter(open_file(into)), 'w', into)
        if str(os.path.exists(f"{into}.marshal")):
            if os.path.exists(into):
                os.remove(into)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"# Usage: python {sys.argv[0]} <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print(f"# File '{filename}' not found.")
        sys.exit(1)

    into = "temp_file"
    la = 3
    show_code("", temp=1)
    start(filename)
