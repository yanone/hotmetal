hotmetal
========

HoTMetaL (HTML) assembler for Python.

Example 1:

```import hotmetal
html = hotmetal.HotMetal()
html.T('Hello world.')
print html.GeneratePage() # Print whole HTML page```

Output:
```<!DOCTYPE html><html><head><meta content="text/html; charset=utf-8" http-equiv="Content-Type"></head><body>Hello world.</body></html>```

Example 2:

```import hotmetal
html = hotmetal.HotMetal()
html.T('Hello world.')
print html.GenerateBody() # Print just the contents of the <body>```

Output:
```Hello world.```
