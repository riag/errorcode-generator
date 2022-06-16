# coding=utf8

import typing
import json
import sys
import os
import argparse
from argparse import Namespace
from jinja2 import Template

from typing import List, TextIO

class ErrorCode(object):

    def __init__(self, fpath:str, d:dict):
        self.comment:str = d.get("comment", "")
        self.code:str = d.get("code", "")
        self.name:str = d.get("name", "")
        # 错误码是定义在哪里文件里
        self.fpath = fpath

    def is_comment(self):
        if len(self.name) == 0 or len(self.code) == 0:
            return True
        return False

class ErrorCodeContext(object):
    def __init__(self):
        self.error_codes = []
        self.code_map = {}
        self.name_map = {}

    def add_error_code(self, error_code: ErrorCode):
        if not error_code.is_comment():
            if error_code.code in self.code_map:
                raise Exception(
                    "error code [%s] already define in %s" % (error_code.code, error_code.fpath)
                    )
            if error_code.name in self.name_map:
                raise Exception(
                    "error code [%s] already define in %s" % (error_code.name, error_code.fpath)
                    )

            self.code_map[error_code.code] = error_code
            self.name_map[error_code.name] = error_code

        self.error_codes.append(error_code)


def default_handle(context: ErrorCodeContext, parentdir:str, fpath:str, item:dict):
    ec = ErrorCode(fpath, item)
    context.add_error_code(ec)

def include_handle(context: ErrorCodeContext, parentdir:str, fpath:str, item:dict):
    v = item.get("include", None)
    if v is None:
        return False

    p = v
    if not os.path.isabs(p):
        p = os.path.abspath(os.path.join(parentdir, p))

    parse_errorcodes(context, p)

    return True

handle_func = [
    include_handle,
    default_handle,
]


def parse_errorcodes(context: ErrorCodeContext, fpath:str) :
    data:str= ""
    parentdir = os.path.dirname(fpath)

    with open(fpath, 'r') as f:
        data = f.read()

    l = json.loads(data) 
    for item in l:
        for func in handle_func:
            if func(context, parentdir, fpath, item):
                break


def render_str(tmp_str:str, ec_list: List[ErrorCode], out : TextIO, args: Namespace) -> None:
    template = Template(tmp_str, trim_blocks=True, lstrip_blocks=True)
    s = template.render(errorcodes = ec_list)
    print(s, file=out)

def render_file(ec_list: List[ErrorCode], out : TextIO, args: Namespace) -> None:
    with open(args.tpl, 'r') as f:
        d = f.read()
        template = Template(d, trim_blocks=True, lstrip_blocks=True)
        s = template.render(errorcodes = ec_list)
        print(s, file=out)

markdown_tmp = """
|  错误码   | 错误描述  |
|  :--:  | :--:  |
{% for item in errorcodes %}
    {% if not item.is_comment() %}
| {{item.code}} | {{item.comment}}
    {% endif %}
{% endfor %}
"""
asciidoc_tmp = """
[cols=".^,.^",options="header"]
|===
|错误码
|错误描述

{% for item in errorcodes %}
    {% if not item.is_comment() %}

|{{item.code}} 
|{{item.comment}}
    {% endif %}
{% endfor %}
|===
"""

rst_tmp = """
=====\t=====
错误码\t错误描述
=====\t=====
{% for item in errorcodes %}
    {% if not item.is_comment() %}
{{item.code}}\t{{item.comment}}
    {% endif %}
{% endfor %}
"""

tmp_map = {
    'markdown': markdown_tmp,
    'asciidoc': asciidoc_tmp,
    'rst': rst_tmp,
}

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", default="markdown", help="buildin render type, support: markdown, asciidoc, rst")
    parser.add_argument("--tpl", help="jinja2 template file")
    parser.add_argument("--out", help="out file")
    parser.add_argument("errorcode_file", help="define error code in this file")
    args: Namespace = parser.parse_args()

    p = os.path.abspath(args.errorcode_file)
    context = ErrorCodeContext()
    parse_errorcodes(context, p)
    out:TextIO = sys.stdout
    f = None
    if args.out is not None:
        f = open(args.out, 'w')
        out = f

    try:
        tmp = None
        if args.tpl is None:
            tmp = tmp_map.get(args.type, None)
            if tmp is None:
                print(f"not support render type {args.tpl}", file=sys.stderr)
                sys.exit(-1)
            tmp = tmp.strip()
        else:
            with open(args.tpl, 'r') as f:
                tmp = f.read()

        render_str(tmp, context.error_codes, out, args)
    finally:
        if f is not None:
            f.close()

if __name__ == "__main__":
    cli()