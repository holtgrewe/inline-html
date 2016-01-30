import os
import base64
import mimetypes
import lxml.html


def img_to_data(path):
    """Convert a file (specified by a path) into a data URI."""
    if not os.path.exists(path):
        raise FileNotFoundError
    mime, _ = mimetypes.guess_type(path)
    with open(path, 'rb') as fp:
        data = fp.read()
        data64 = u''.join(base64.encodestring(data).splitlines())
        return u'data:%s;base64,%s' % (mime, data64)


html = open('in.html', 'rb').read()
root = lxml.html.fromstring(html)

for img in root.xpath('//img'):
    src = img.attrib['src']
    data = img_to_data(src)
    img.attrib['src'] = data

for link in root.xpath('//link'):
    href = link.attrib['href']
    css = open(href, 'rb').read()
    node = lxml.etree.Element('style')
    node.attrib['type'] = 'text/css'
    node.text = css
    link.getparent().replace(link, node)

open('out.html', 'wb').write(lxml.html.tostring(root))

