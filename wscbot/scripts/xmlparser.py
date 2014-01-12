# -*- coding: utf-8 -*-

"""
Faz o parse do arquivo XML

"""
"""Autor: Breno Rodrigues Brito"""
import xml.etree.ElementTree as ET
# from xml.dom import minidom

tree = ET.parse(pathtofile)
root = tree.getroot()

# xmldoc = minidom.parse('items.xml')
# itemlist = xmldoc.getElementsByTagName('item') 
# print len(itemlist)
# print itemlist[0].attributes['name'].value
# for s in itemlist :
#     print s.attributes['name'].value
