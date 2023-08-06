# Copyright (C) 2000-2001 The OpenRPG Project
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: chat_msg.py
# Author: Ted Berg
# Maintainer:
# Version:
#   $Id: chat_msg.py,v 1.15 2006/11/04 21:24:19 digitalxero Exp $
#
# Description: Contains class definitions for manipulating <chat/> messages
#
#

__version__ = "$Id: chat_msg.py,v 1.15 2006/11/04 21:24:19 digitalxero Exp $"

import orpg.lib.xmlutil as xmlutil
from orpg.chat.chat_version import CHAT_VERSION

CHAT_MESSAGE = 1
WHISPER_MESSAGE = 2
EMOTE_MESSAGE = 3
INFO_MESSAGE = 4
SYSTEM_MESSAGE = 5
WHISPER_EMOTE_MESSAGE = 6

class chat_msg:
    def __init__(self,xml_text="<chat type=\"1\" version=\""+CHAT_VERSION+"\" alias=\"\" ></chat>"):
        self.chat_dom = None
        self.takexml(xml_text)

    def __del__(self):
        if self.chat_dom:
            self.chat_dom.unlink()

    def toxml(self):
        return xmlutil.toxml(self.chat_dom)

    def takexml(self,xml_text):
        xml_dom = xmlutil.parseXml(xml_text)
        node_list = xml_dom.getElementsByTagName("chat")
        if len(node_list) < 1:
            print("Warning: no <chat/> elements found in DOM.")
        else:
            if len(node_list) > 1:
                print("Found more than one instance of <" + self.tagname + "/>.  Taking first one")
            self.takedom(node_list[0])

    def takedom(self,xml_dom):
        if self.chat_dom:
            self.text_node = None
            self.chat_dom.unlink()
        self.chat_dom = xml_dom
        self.text_node = xmlutil.safe_get_text_node(self.chat_dom)

    def set_text(self,text):
        self.text_node.nodeValue = text

    def set_type(self,type):
        self.chat_dom.setAttribute("type",str(type))

    def get_type(self):
        return int(self.chat_dom.getAttribute("type"))

    def set_alias(self,alias):
        self.chat_dom.setAttribute("alias",alias)

    def get_alias(self):
        return self.chat_dom.getAttribute("alias")

    def get_text(self):
        return self.text_node.nodeValue

    def get_version(self):
        return self.chat_dom.getAttribute("version")
