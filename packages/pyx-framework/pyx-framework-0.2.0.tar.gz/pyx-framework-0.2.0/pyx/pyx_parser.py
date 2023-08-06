import re
from html import unescape
from html.parser import HTMLParser
from html.parser import endendtag, endtagfind, tagfind_tolerant


attrfind_tolerant = re.compile(
    r'((?<=[\'"{}\s/])[^\s/>][^\s/=>]*)(\s*=+\s*(\'[^\']*\'|"[^"]*"|{[^{}]*}|(?![\'"{}])[^>\s]*))?(?:\s|/(?!>))*'
)
locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][^\t\n\r\f />\x00]*         # tag name
  (?:[\s/]*                            # optional whitespace before attribute name
    (?:(?<=['"{}\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                      # value indicator
        (?:'[^']*'                     # LITA-enclosed value
          |"[^"]*"                     # LIT-enclosed value
          |{[^{}]*}                    # bare python value
          |(?!['"{}])[^>\s]*           # bare value
         )
         (?:\s*,)*                     # possibly followed by a comma
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                  # trailing whitespace
""", re.VERBOSE)

def map_attrs(attrs, tab):
    res = []
    _len = len(attrs)
    i = 0
    while i < _len:
        _name_changed = False
        _value_changed = False
        name, value = attrs[i]
        value = value or ''
        if name[:1] == '{' and name[-1:] == '}':
            name = name[1:-1]
            _name_changed = True
            _value_changed = not value
        elif not value:
            value = 'True'
            _value_changed = True
        if value[:1] == '{' and value[-1:] == '}':
            value = value[1:-1]
            if value[:1] == '<':
                value = PyxHTMLParser().feed(value)
            else:
                value = value or 'None'
            _value_changed = True
        if not _name_changed:
            name = f'"{name}"'
        if not _value_changed:
            value = f'"{value}"'
        res.append(name + (': ' + value if value else ''))
        i += 1
    if not res:
        return ''
    res.insert(0, '')
    res.append('')
    return (',\n    ' + tab).join(res)[1:]


class PyxHTMLParser(HTMLParser):
    CDATA_CONTENT_ELEMENTS = ("script", "style", "python")

    def __init__(self, /, **k):
        super().__init__(**k)
        self.data = ''
        self.temp_data = []
        self.temp_children = []
        self.temp_text = ''
        self.tags = []
        self.tags_set = set()

    def feed(self, *a, **k):
        super().feed(*a, **k)
        return self.data

    def error(self, message):
        print('[PYX] Error:', message)

    def _get_tab(self):
        m = re.search(r' +', self.data[-2::-1])
        if m is None:
            return ''
        return m.group()[::-1]

    def _append_child(self, data):
        children = self.temp_children[-1]
        if children:
            children += ', '
        children += data
        self.temp_children[-1] = children

    # Internal -- check to see if we have a complete starttag; return end
    # or -1 if incomplete.
    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend_tolerant.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j+1]
            if next == ">":
                return j + 1
            if next == "/":
                if rawdata.startswith("/>", j):
                    return j + 2
                if rawdata.startswith("/", j):
                    # buffer boundary
                    return -1
                # else bogus input
                if j > i:
                    return j
                else:
                    return i + 1
            if next == "":
                # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if j > i:
                return j
            else:
                return i + 1
        raise AssertionError("we should not get here!")

    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = match.group(1)
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                    attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = unescape(attrvalue[1:-1])
            elif attrvalue[:1] == '{' and attrvalue[-1:] == '}':
                attrvalue = attrvalue
            else:
                attrvalue = unescape(attrvalue)
            attrs.append((attrname, attrvalue))
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == "</", "unexpected call to parse_endtag"
        match = endendtag.search(rawdata, i + 1)  # >
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, i)  # </ + tag + >
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, i + 2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i:i + 3] == '</>':
                    self.handle_endtag('__fragment__')
                    return i + 3
                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group(1)
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after tha name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos + 1

        elem = match.group(1)  # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos

        self.handle_endtag(elem)
        self.clear_cdata_mode()
        return gtpos
    
    def handle_starttag(self, tag, attrs):
        tab = self._get_tab()
        self.tags.append(tag)
        self.tags_set.add(tag)
        if tag == '__fragment__':
            self.temp_text = ''
        if tag == 'python':
            attrs.append(('_locals', '{locals()}'))
        self.temp_data.append(map_attrs(attrs, tab))
        if len(self.temp_children) == len(self.tags) and len(self.temp_children) > 1:
            data = self.temp_children.pop()
            self.temp_children[-1] += data
            self.temp_children.append('')
        elif not self.temp_text.strip():
            self.temp_text = ''
            self.temp_children.append('')
        else:
            self.temp_children.append(self.temp_text)

    def handle_endtag(self, tag):
        args = self.temp_data.pop()
        text = self.temp_text
        children = self.temp_children.pop() if self.temp_children else ''
        result_arguments = "(**{" + args +\
            ('"children": [' + children + (', ' + text if children and text else text) + ']' if children or text else '') +\
            "})"
        if result_arguments == '(**{})':
            result_arguments = '()'
        data = tag + result_arguments
        if self.tags[-1] == tag:
            self.tags.pop()
        
        if self.tags:
            LEN = len(self.tags) - 1
            if self.temp_children[LEN]:
                data = ', ' + data
            self.temp_children[LEN] += data
        else:
            if text:
                self.temp_children.append(text)
            self.data += data
        self.temp_text = ''

    def handle_data(self, data):
        if data.startswith('>'):
            data = data[1:]
        if data == '<':
            return self.handle_starttag('__fragment__', {})
        if not data.strip():
            self.temp_text += data.strip()
            return
        if self.tags:
            if self.temp_text:
                if self.temp_text.strip() and self.temp_text.strip()[-1] == ')':
                    self.temp_children.append(self.temp_text)
            if '{' in data or '}' in data:
                if data[0] == '{' and data[-1] == '}':
                    self._append_child(data[1:-1])
                else:
                    self._append_child('f"""' + data + '"""')
            else:
                self._append_child('"""' + data + '"""')
        else:
            self.data += data


def parse(pre=lambda a, b, c: '', post=lambda c: None):
    import sys
    if len(sys.argv) > 1:
        filenames = sys.argv[1:]
    else:
        filenames = []
        from pathlib import Path
        for path in Path().rglob('*.pyx'):
            filenames.append(path.name[:-4])

    print(filenames)
    for filename in filenames:
        with open(filename + '.pyx', 'r') as _in, open(filename + '.py', 'w+') as _out:
            d = pre(PyxHTMLParser, _in.read(), filename) or ''
            _out.write(d)
            post(filename)


if __name__ == '__main__':
    def main(cls, inp, filename):
        import os
        parser = cls()
        feed = parser.feed(inp)
        parser.tags_set.add('__pyx__')
        os.environ["__PYX__"] = filename
        return '''
from pyx import *  # importing all: tag, default tags (div, select, tabs, etc.), ...
from pyx import (  # importing extra data for pyx render
    __fragment__,
)
%s
tags_set = %s


l = locals()
for tag_name in tags_set:
    if _tag := l.get(tag_name):
        l[tag_name] = cached_tag(_tag)
    else:
        l[tag_name] = Tag(name=tag_name)(div)
''' % (feed, parser.tags_set)

    parse(main)
