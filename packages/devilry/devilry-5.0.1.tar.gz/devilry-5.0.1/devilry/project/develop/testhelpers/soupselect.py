"""
soupselect.py - https://code.google.com/p/soupselect/

CSS selector support for BeautifulSoup.

soup = BeautifulSoup('<html>...')
select(soup, 'div')
- returns a list of div elements

select(soup, 'div#main ul a')
- returns a list of links inside a ul inside div#main

"""

import re
from bs4 import BeautifulSoup

tag_re = re.compile('^[a-z0-9]+$')

attribselect_re = re.compile(
    r'^(?P<tag>\w+)?\[(?P<attribute>\w+)(?P<operator>[=~\|\^\$\*]?)' + 
    r'=?"?(?P<value>[^\]"]*)"?\]$'
)

# /^(\w+)\[(\w+)([=~\|\^\$\*]?)=?"?([^\]"]*)"?\]$/
#   \---/  \---/\-------------/    \-------/
#     |      |         |               |
#     |      |         |           The value
#     |      |    ~,|,^,$,* or =
#     |   Attribute 
#    Tag

def attribute_checker(operator, attribute, value=''):
    """
    Takes an operator, attribute and optional value; returns a function that
    will return True for elements that match that combination.
    """
    return {
        '=': lambda el: el.get(attribute) == value,
        # attribute includes value as one of a set of space separated tokens
        '~': lambda el: value in el.get(attribute, '').split(),
        # attribute starts with value
        '^': lambda el: el.get(attribute, '').startswith(value),
        # attribute ends with value
        '$': lambda el: el.get(attribute, '').endswith(value),
        # attribute contains value
        '*': lambda el: value in el.get(attribute, ''),
        # attribute is either exactly value or starts with value-
        '|': lambda el: el.get(attribute, '') == value \
            or el.get(attribute, '').startswith('%s-' % value),
    }.get(operator, lambda el: attribute in el)


def select(soup, selector):
    """
    soup should be a BeautifulSoup instance; selector is a CSS selector 
    specifying the elements you want to retrieve.
    """
    tokens = selector.split()
    current_context = [soup]
    for token in tokens:
        m = attribselect_re.match(token)
        if m:
            # Attribute selector
            tag, attribute, operator, value = m.groups()
            if not tag:
                tag = True
            checker = attribute_checker(operator, attribute, value)
            found = []
            for context in current_context:
                found.extend([el for el in context.findAll(tag) if checker(el)])
            current_context = found
            continue
        if '#' in token:
            # ID selector
            tag, id = token.split('#', 1)
            if not tag:
                tag = True
            el = current_context[0].find(tag, {'id': id})
            if not el:
                return [] # No match
            current_context = [el]
            continue
        if '.' in token:
            # Class selector
            tag, klass = token.split('.', 1)
            if not tag:
                tag = True
            found = []
            for context in current_context:
                found.extend(
                    context.findAll(tag,
                        {'class': lambda attr: attr and klass in attr.split()}
                    )
                )
            current_context = found
            continue
        if token == '*':
            # Star selector
            found = []
            for context in current_context:
                found.extend(context.findAll(True))
            current_context = found
            continue
        # Here we should just have a regular tag
        if not tag_re.match(token):
            return []
        found = []
        for context in current_context:
            found.extend(context.findAll(token))
        current_context = found
    return current_context

def monkeypatch(BeautifulSoupClass=None):
    """
    If you don't explicitly state the class to patch, defaults to the most 
    common import location for BeautifulSoup.
    """
    if not BeautifulSoupClass:
        from BeautifulSoup import BeautifulSoup as BeautifulSoupClass
    BeautifulSoupClass.findSelect = select

def unmonkeypatch(BeautifulSoupClass=None):
    if not BeautifulSoupClass:
        from BeautifulSoup import BeautifulSoup as BeautifulSoupClass
    delattr(BeautifulSoupClass, 'findSelect')


def cssFind(html, selector):
    """
    Parse ``html`` with class:`BeautifulSoup.BeautifulSoup` and use
    :func:`.select` on the result.

    Added by Espen A. Kristiansen to make it even easier to use for testing.
    """
    soup = BeautifulSoup(html)
    return select(soup, selector)

def cssGet(html, selector):
    """
    Same as :func:`.cssFind`, but returns the first match.

    Added by Espen A. Kristiansen to make it even easier to use for testing.
    """
    try:
        return cssFind(html, selector)[0]
    except IndexError as e:
        raise IndexError('Could not find {}.'.format(selector))

def cssExists(html, selector):
    """
    Same as :func:`.cssFind`, but returns ``True`` if the selector matches at least one item.

    Added by Espen A. Kristiansen to make it even easier to use for testing.
    """
    matches = cssFind(html, selector)
    return bool(len(matches))

def prettyhtml(html):
    return BeautifulSoup(html).prettify()

def normalize_whitespace(html):
    return re.sub('(\s|\\xa0)+', ' ', html).strip()
