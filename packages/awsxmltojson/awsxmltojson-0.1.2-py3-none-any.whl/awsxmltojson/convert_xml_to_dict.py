from lxml import etree
from .xml_etree_to_dict import xml_etree_to_dict

parser = etree.XMLParser(remove_blank_text=True)


def convert_xml_to_dict(xml_string):
    rootelm = etree.fromstring(xml_string, parser=parser)
    return xml_etree_to_dict(rootelm)