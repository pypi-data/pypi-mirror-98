# -*- coding: utf-8 -*-

"""
direct Python Toolbox
All-in-one toolbox to encapsulate Python runtime variants
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?dpt;xml

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
v1.0.3
dpt_xml/xml_parser_MonoXML.py
"""

# pylint: disable=import-error,invalid-name,wrong-import-order,wrong-import-position

import clr
clr.AddReference("System.Xml")

from System.Xml import XmlDocument, XmlNodeReader, XmlNodeType
from time import time

from .abstract_xml_parser import AbstractXmlParser, _PY_STR, _PY_UNICODE_TYPE

class XmlParserMonoXml(AbstractXmlParser):
    """
This implementation supports XmlNodeReader for XML parsing.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    dpt
:subpackage: xml
:since:      v1.0.0
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __slots__ = ( "timeout_retries", )
    """
python.org: __slots__ reserves space for the declared variables and prevents
the automatic creation of __dict__ and __weakref__ for each instance.
    """

    def __init__(self, parser, timeout_retries = 5, log_handler = None):
        """
Constructor __init__(XmlParserMonoXml)

:param parser: Container for the XML document
:param current_time: Current UNIX timestamp
:param timeout_retries: Retries before timing out
:param log_handler: Log handler to use

:since: v1.0.0
        """

        AbstractXmlParser.__init__(self, parser, log_handler)

        self.timeout_retries = (5 if (timeout_retries is None) else timeout_retries)
        """
Retries before timing out
        """
    #

    def _get_merged_result(self, _XmlNodeReader):
        """
Uses the given XmlNodeReader to parse data as a merged tree.

:param _XmlNodeReader: XmlNodeReader object

:return: (dict) Merged XML tree; None on error
:since:  v1.0.0
        """

        # global: _PY_STR, _PY_UNICODE_TYPE

        if (self._log_handler is not None): self._log_handler.debug("dpt_xml/xml_parser_MonoXML.py -{0!r}._get_merged_result()- (81)", self)

        if (hasattr(_XmlNodeReader, "Read")):
            _return = { }

            depth = 0
            is_read = False
            is_valid = True
            node_change_check = False
            node_path = ""
            node_path_list = [ ]
            nodes_dict = { }
            timeout_time = (time() + self.timeout_retries)

            while (is_valid and time() < timeout_time):
                if (_XmlNodeReader.NodeType == XmlNodeType.CDATA):
                    if (node_path in nodes_dict):
                        nodes_dict[node_path]['value'] += (_XmlNodeReader.Value
                                                           if (nodes_dict[node_path]['attributes'].get("xml:space") == "preserve") else
                                                           _XmlNodeReader.Value.strip()
                                                          )
                    #
                elif (_XmlNodeReader.NodeType == XmlNodeType.Element):
                    attributes_dict = { }
                    node_name = _XmlNodeReader.Name.lower()
                    if (node_name[:12] == "digitstart__"): node_name = node_name[12:]

                    if (_XmlNodeReader.HasAttributes):
                        while (_XmlNodeReader.MoveToNextAttribute() and time() < timeout_time):
                            attribute_name = _XmlNodeReader.Name.lower()
                            if (str is not _PY_UNICODE_TYPE and type(attribute_name) is _PY_UNICODE_TYPE): attribute_name = _PY_STR(attribute_name, "utf-8")

                            if (attribute_name.startswith("xmlns:")): attributes_dict["xmlns:{0}".format(attribute_name[6:])] = _XmlNodeReader.Value
                            elif (attribute_name == "xml:space"): attributes_dict['xml:space'] = _XmlNodeReader.Value.lower()
                            else: attributes_dict[attribute_name] = _XmlNodeReader.Value
                        #

                        _XmlNodeReader.MoveToElement()
                    #

                    node_path_list.append(node_name)
                    node_path = "_".join(node_path_list)
                    nodes_dict[node_path] = { "tag": node_name, "value": None, "attributes": attributes_dict }

                    depth = _XmlNodeReader.Depth
                    is_read = True
                    is_valid = _XmlNodeReader.Read()
                    node_change_check = True
                elif (_XmlNodeReader.NodeType == XmlNodeType.EndElement):
                    is_read = True
                    is_valid = _XmlNodeReader.Read()
                    node_change_check = True
                elif (_XmlNodeReader.NodeType == XmlNodeType.Text and node_path in nodes_dict):
                    nodes_dict[node_path]['value'] += (_XmlNodeReader.Value
                                                       if (nodes_dict[node_path]['attributes'].get("xml:space") == "preserve") else
                                                       _XmlNodeReader.Value.strip()
                                                      )
                #

                if (node_change_check):
                    node_change_check = False

                    if (node_path in nodes_dict[node_path]):
                        if ("value" in nodes_dict[node_path]['attributes'] and len(nodes_dict[node_path]['value']) < 1):
                            nodes_dict[node_path]['value'] = nodes_dict[node_path]['attributes']['value']
                            del(nodes_dict[node_path]['attributes']['value'])
                        #

                        if (node_path in _return):
                            if ("tag" in _return[node_path]):
                                node_packed_dict = _return[node_path].copy()
                                _return[node_path] = [ node_packed_dict ]
                                node_packed_dict = None
                            #

                            _return[node_path].append(nodes_dict[node_path])
                        else: _return[node_path] = nodes_dict[node_path]

                        del(nodes_dict[node_path])
                    #

                    depth = _XmlNodeReader.Depth
                    is_read = True
                    node_path_list.pop()
                    node_path = "_".join(node_path_list)
                elif (_XmlNodeReader.Depth < depth):
                    if (node_path in nodes_dict): del(nodes_dict[node_path])

                    depth = _XmlNodeReader.Depth
                    node_path_list.pop()
                    node_path = "_".join(node_path_list)
                #

                if (is_read): is_read = True
                elif (is_valid): is_valid = _XmlNodeReader.Read()
            #

            _XmlNodeReader.Close()
        else: _return = None

        return _return
    #

    def _get_parsed_dict_walker(self, _XmlNodeReader, node_path = "", xml_level = 0):
        """
Converts XML data into a multi-dimensional dict using this recursive
algorithm.

:param _XmlNodeReader: XmlNodeReader object
:param node_path: Old node path (for recursive use only)
:param xml_level: Current XML depth

:return: (dict) XML tree node; None on error
:since:  v1.0.0
        """

        # global: _PY_STR, _PY_UNICODE_TYPE

        if (str is not _PY_UNICODE_TYPE and type(node_path) is _PY_UNICODE_TYPE): node_path = _PY_STR(node_path, "utf-8")

        if (self._log_handler is not None): self._log_handler.debug("dpt_xml/xml_parser_MonoXML.py -{0!r}._get_parsed_dict_walker({1}, {2:d})- (201)", self, node_path, xml_level)
        _return = None

        if (hasattr(_XmlNodeReader,"Read")):
            attributes_dict = { }
            is_node = False
            is_preserved_mode = False
            is_read = True
            node_content = ""
            nodes_list = [ ]
            timeout_time = (time() + self.timeout_retries)

            while ((not is_node) and is_read and time() < timeout_time):
                if (_XmlNodeReader.NodeType == XmlNodeType.Element):
                    if (self.strict_standard_mode):
                        node_name = _XmlNodeReader.Name
                        if (str is not _PY_UNICODE_TYPE and type(node_name) is _PY_UNICODE_TYPE): node_name = _PY_STR(node_name, "utf-8")
                    else:
                        node_name = _XmlNodeReader.Name.lower()
                        if (str is not _PY_UNICODE_TYPE and type(node_name) is _PY_UNICODE_TYPE): node_name = _PY_STR(node_name, "utf-8")
                        if (node_name[:12] == "digitstart__"): node_name = node_name[12:]
                    #

                    if (_XmlNodeReader.HasAttributes):
                        while (_XmlNodeReader.MoveToNextAttribute() and time() < timeout_time):
                            attribute_name = _XmlNodeReader.Name.lower()
                            if (str is not _PY_UNICODE_TYPE and type(attribute_name) is _PY_UNICODE_TYPE): attribute_name = _PY_STR(attribute_name, "utf-8")

                            if (attribute_name.startswith("xmlns:")): attributes_dict["xmlns:{0}".format(attribute_name[6:])] = _XmlNodeReader.Value
                            elif (attribute_name == "xml:space"):
                                attributes_dict['xml:space'] = _XmlNodeReader.Value.lower()
                                is_preserved_mode = (attributes_dict['xml:space'] == "preserve")
                            elif (self.strict_standard_mode): attributes_dict[_XmlNodeReader.Name] = _XmlNodeReader.Value
                            else: attributes_dict[attribute_name] = _XmlNodeReader.Value
                        #

                        _XmlNodeReader.MoveToElement()
                    #

                    is_node = True
                #

                is_read = _XmlNodeReader.Read()
            #

            if (is_node): node_path = ("{0} {1}".format(node_path, node_name) if (len(node_path) > 0) else node_name)

            while (is_node and time() < timeout_time):
                if (xml_level < _XmlNodeReader.Depth):
                    if (_XmlNodeReader.NodeType == XmlNodeType.CDATA): node_content += (_XmlNodeReader.Value if (is_preserved_mode) else _XmlNodeReader.Value.strip())
                    elif (_XmlNodeReader.NodeType == XmlNodeType.Element):
                        is_read = False
                        nodes_list.append(self._get_parsed_dict_walker(_XmlNodeReader, node_path, _XmlNodeReader.Depth))
                    elif (_XmlNodeReader.NodeType == XmlNodeType.EndElement):
                        is_read = False
                        _XmlNodeReader.Read()
                    elif (_XmlNodeReader.NodeType == XmlNodeType.Text): node_content += (_XmlNodeReader.Value if (is_preserved_mode) else _XmlNodeReader.Value.strip())
                    elif (is_preserved_mode
                          and (_XmlNodeReader.NodeType == XmlNodeType.Whitespace or _XmlNodeReader.NodeType == XmlNodeType.SignificantWhitespace)
                         ): node_content += _XmlNodeReader.Value

                    if (is_read): is_node = _XmlNodeReader.Read()
                    else: is_read = True
                else: break
            #

            _return = { "node_path": node_path, "value": node_content, "attributes": attributes_dict, "children": nodes_list }
        #

        return _return
    #

    def parse(self, data):
        """
Parses a given XML string and return the result in the format set by "mode"
and "strict_standard_mode".

:return: (dict) Multi-dimensional or merged XML tree; None on error
:since:  v1.0.0
        """

        # global: _PY_STR, _PY_UNICODE_TYPE

        if (self._log_handler is not None): self._log_handler.debug("dpt_xml/xml_parser_MonoXML.py -{0!r}.parse()- (284)", self)

        _return = None

        if (str is not _PY_UNICODE_TYPE and type(data) is _PY_UNICODE_TYPE): data = _PY_STR(data, "utf-8")

        parser_ptr = XmlDocument()
        parser_ptr.LoadXml(data)
        parser_ptr = XmlNodeReader(parser_ptr)

        if (parser_ptr is not None):
            _return = (self._get_merged_result(parser_ptr)
                       if (self._merged_mode) else
                       self._update_parser_with_result(parser_ptr)
                      )
        #

        return _return
    #

    def _update_parser_with_parsed_dict_walker(self, data_dict):
        """
Imports a pre-parsed XML dict into the given parser instance.

:param data_dict: Result dict of a "_get_parsed_dict_walker()"

:return: (bool) True on success
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("dpt_xml/xml_parser_MonoXML.py -{0!r}._update_parser_with_parsed_dict_walker()- (314)", self)
        _return = False

        if (type(data_dict) is dict):
            if (len(data_dict['value']) > 0 or len(data_dict['attributes']) > 0 or len(data_dict['children']) > 0):
                if ((not self.strict_standard_mode) and "value" in data_dict['attributes'] and len(data_dict['value']) < 1):
                    data_dict['value'] = data_dict['attributes']['value']
                    del(data_dict['attributes']['value'])
                #

                self.parser.add_node(data_dict['node_path'], data_dict['value'], data_dict['attributes'])
            #

            if (len(data_dict['children']) > 0):
                for child_dict in data_dict['children']: self._update_parser_with_parsed_dict_walker(child_dict)
            #

            _return = True
        #

        return _return
    #

    def _update_parser_with_result(self, _XmlNodeReader):
        """
Uses the given XmlNodeReader to parse data for the defined parser instance.

:param _XmlNodeReader: XmlNodeReader object

:return: (dict) Multi-dimensional XML tree
:since:  v1.0.0
        """

        if (self._log_handler is not None): self._log_handler.debug("dpt_xml/xml_parser_MonoXML.py -{0!r}._update_parser_with_result()- (347)", self)
        _return = { }

        if (hasattr(_XmlNodeReader, "Read")):
            is_available = True
            timeout_time = (time() + self.timeout_retries)

            self.parser.set_xml_tree({ }, True)

            while (is_available
                   and _XmlNodeReader.NodeType != XmlNodeType.Element
                   and time() < timeout_time
                  ): is_available = _XmlNodeReader.Read()

            monoxml_dict = self._get_parsed_dict_walker(_XmlNodeReader)
            _XmlNodeReader.Close()

            if (type(monoxml_dict) is dict): is_available = self._update_parser_with_parsed_dict_walker(monoxml_dict)
            if (is_available): _return = self.parser.data
        #

        return _return
    #
#
