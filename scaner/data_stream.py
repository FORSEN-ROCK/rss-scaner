import os


import exeptions

import requests

from bs4 import BeautifulSoup


class RssParser(object):
    container = 'item'
    title = 'title'
    link = 'guid'
    description = 'description'
    public_date = 'pubdate'
    category = 'category'

    def _get_target(self, content, tag_name):
        """Base method for finding and getting value of xml attr
           Taks content (xml-three) and tag_name (string)
           Return value of this tag
        """

        expression = getattr(self, tag_name, None)

        if not expression:
            raise exeptions.ParserError(
                "Parser couldn't find excpression for tag name: %s"
                %(tag_name)
            )

        element = content.find(expression)

        if element:
            tag_value = element.get_text()
        else:
            tag_value = None

        return tag_value
        
    def separate_context(self, content):
        """Taks current object and xml-three of bs4 from rss source
           Returns list of artical
        """

        if(len(content) <= 0):
            raise exeptions.EmptyContent(
                "Parser can't work with empty content!"
            )

        items = content.findAll(self.container)

        if(len(items) <= 0):
            raise exeptions.ContainerNotFound(
                "Container not found!"
            )

        return items

    def get_title(self, item_content):
        """Taks current object and item content
           Returns text of title
        """
        return self._get_target(item_content, 'title')

    def get_link(self, item_content):
        """Taks current object and item content
            Returns text of link
        """
        return self._get_target(item_content, 'link')

    def get_description(self, item_content):
        """Taks current object and item content
            Returns text of description
        """
        return self._get_target(item_content, 'description')

    def get_public_date(self, item_content):
        """Taks current object and item content
            Returns text of public date
        """
        return self._get_target(item_content, 'public_date')

    def get_category(self, item_content):
        """Taks current object and item content
            Returns text of category
        """
        return self._get_target(item_content, 'category')


class Artical(object):
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.link = kwargs.get('link')
        self.description = kwargs.get('description')
        self.public_date = kwargs.get('public_date')
        self.category = kwargs.get('category')

    def __str__(self):
        return '%s;%s;%s;%s;%s;\n' %(self.link, self.title, 
                self.public_date, self.category, self.description)


def parser(cls_parser=None, cls_data=None, content=None):
    """This is main parser function
       Taks class of parser, class of data definition and content
       Return list of data definition objects
    """

    if((cls_parser is None) or (cls_data is None) or
                                            (content is None)):
        raise exception.ParserError("Required arguments wasn't gave")

    items = cls_parser.separate_context(content)
    data = []

    for item in items:
        title = cls_parser.get_title(item)
        link = cls_parser.get_link(item)
        description = cls_parser.get_description(item)
        category = cls_parser.get_category(item)
        public_date = cls_parser.get_public_date(item)

        data.append(cls_data(title=title,
                             link=link,
                             description=description,
                             category=category,
                             public_date=public_date))

    return data

def stream(file_name, cls_parser=RssParser(), cls_data=Artical):
    """
    """

    links_file = open(file_name, 'r')
    source_links = links_file.read().split('\n')

    agrigate_data = {}

    for rss_url in source_links:

        ## Comment in file of links
        if rss_url[0] == '#':
            continue

        response = requests.get(rss_url)
        channel_data = response.content

        if len(channel_data) <= 0:
            raise RequestError("Chanal %s returns empty response" 
                               %(rss_url))

        content = BeautifulSoup(channel_data, "lxml-xml")

        try:
            items = parser(cls_parser, cls_data, content)
            agrigate_data[rss_url] = items
        except exeptions.ContainerNotFound:
            continue
        except exeptions.EmptyContent:
            continue

    return agrigate_data