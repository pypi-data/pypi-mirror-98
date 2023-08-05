from __future__ import unicode_literals

from pandas import DataFrame
from portalocker import Lock as Open
from django.utils.crypto import get_random_string

import xml.etree.ElementTree as ET
import datetime
import os


class XML(object):
    """
    Read and Write XML objects by using XML.etree.ElementTree module
    """

    def __init__(self, xml_file):
        if xml_file is None:
            raise ValueError("'xml_file' is not populated")

        if not os.path.isdir(os.path.dirname(xml_file)):
            raise ValueError("'xml_file' %r is not a valid directory" % os.path.dirname(xml_file))

        if not os.path.exists(os.path.dirname(xml_file)):
            raise Exception("'xml_file' %r does not exist" % os.path.dirname(xml_file))

        self.xml_file = xml_file
        self.read_handlers = list()

    def read(self, xmlns_rs, dict_var=None):
        """
        Reads XML files and store in a dict or pandas DataFrame

        :param xmlns_rs: XMLNS_RS sentence in XML file
        :param dict_var: (Optional) Dict object
        :return: Dataframe or Dict
        """

        if not os.path.exists(self.xml_file):
            raise Exception("'xml_file' %r is not a valid filepath" % xml_file)

        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        if isinstance(dict_var, dict):
            for item in root.findall(xmlns_rs):
                dict_var = self.__parse_element(item, dict_var)

            return dict_var
        else:
            parsed = list()
            i = 0

            mylist = root.findall(xmlns_rs)
            for item in mylist:
                parsed.append(self.__parse_element(item))

                if self.__parse_df({'xml_data': parsed, 'counter': i - len(parsed) + 1}):
                    parsed.clear()

                i += 1

            if self.read_handlers:
                self.__parse_df({'xml_data': parsed, 'counter': i - len(parsed) + 1}, ignore=True)
            else:
                df = DataFrame(parsed)
                return df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def write(self, dataframe):
        """
        Write Dataframe to XML

        :param dataframe: Pandas DataFrame
        """

        if not isinstance(dataframe, DataFrame):
            raise ValueError("'dataframe' %r is not an instance of DataFrame from pandas" % dataframe)

        while os.path.exists(self.xml_file):
            uid = get_random_string(length=16,
                                    allowed_chars=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            date = datetime.datetime.now()
            self.xml_file = os.path.join(os.path.dirname(self.xml_file),
                                         '%s-%s-%s_%s.xml' % (date.year, date.month, date.day, uid))

        with Open(self.xml_file, 'w') as xmlfile:
            xmlfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            xmlfile.write('<records>\n')
            xmlfile.write(
                '\n'.join(dataframe.apply(self.__xml_encode, axis=1))
            )
            xmlfile.write('\n</records>')

    def read_event(self, buffer=1000, **kwargs):
        def registerhandler(handler):
            self.read_handlers.append([handler, buffer, kwargs])
            return handler

        return registerhandler

    def __parse_df(self, data, ignore=False):
        return_val = False

        if self.read_handlers:
            data['df'] = DataFrame()

            for read_handler in self.read_handlers:
                if ignore or len(data['xml_data']) >= read_handler[1]:
                    return_val = True

                    if data['df'].empty:
                        data['df'] = DataFrame(data['xml_data'])
                        data['df'] = data['df'].applymap(lambda x: x.strip() if isinstance(x, str) else x)

                    if read_handler[2]:
                        read_handler[0](data, **read_handler[2])
                    else:
                        read_handler[0](data)

        return return_val

    def __parse_element(self, element, parsed=None):
        if not parsed:
            parsed = dict()

        if element.keys():
            for key in element.keys():
                if key not in parsed:
                    parsed[key] = element.attrib.get(key)

                if element.text and element.tag not in parsed:
                    parsed[element.tag] = element.text

        elif element.text and element.tag not in parsed:
            parsed[element.tag] = element.text

        for child in list(element):
            self.__parse_element(child, parsed)

        return parsed

    @staticmethod
    def __xml_encode(row):
        xmlitem = ['  <record>']

        for field in row.index:
            if row[field]:
                xmlitem.append('    <var var_name="{0}">{1}</var>'.format(field, row[field]))

        xmlitem.append('  </record>')

        return '\n'.join(xmlitem)
