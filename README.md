# errorcode-generator

  在 json 文件里定义好错误码相关信息, 根据 jinja2 模板文件来生成相应的错误代码文件或者文档

## 安装

```
pip3 install https://github.com/riag/errorcode-generator/releases/download/0.1.1/errorcode_generator-0.1.1-py3-none-any.whl
```

## 使用

  `example` 目录里有 2 个简单的例子，可以参考, 下面演示怎么使用

  ```
  errorcode-generator example/simple/errorcodes.json
  ```

  上面例子是根据错误码 json 文件来生成 markdown 表格格式错误码

  ```
  errorcode-generator example/simple/errorcodes.json --tpl example/simple/tpl.kt
  ```

  上面例子是根据 jinja2 模板文件和错误码 json 文件来生成具体的内容


### 参数

  ```
  -t, --type            使用内置的模板生成具体内容，支持 markdown, asciidoc, rst
  --tpl                 使用 jinja2 模板文件
  --out                 生成的内容要写到的文件, 不指定就输出到控制台
  ```

## json 错误码格式

  每个 json 文件里是一个列表，每一项里支持的字段如下:
  
  ```
    code:       错误码代码
    name:       错误码变量名
    comment:    错误码描述或者注释
    include:    包含其他 json 文件
  ```

  具体的使用可以参考 `example/multifile/errorcodes.json`