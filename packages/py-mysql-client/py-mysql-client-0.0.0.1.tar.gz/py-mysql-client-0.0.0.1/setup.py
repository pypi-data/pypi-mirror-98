#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2017, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is also distributed with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation.  The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have included with
# MySQL.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

"""

To install MySQL Connector/Python:

    shell> python ./setup.py install

"""

import setuptools




setuptools.setup(
    name="py-mysql-client",
    version="0.0.0.1",
    description="基于mysql-python-connector库改写的python mysql driver",
    long_description="py-mysql-client是mysql-python-connector库的简易版，基于mysql官方开源库mysql-python-connector实现;\n无cursor,执行query后立即获取数据,模拟mysql命令行客户端执行query的过程;\n支持prepare stmt;\n支持设置自动提交事务;\n支持debug模式:日志输出与mysql server从建联到执行query的整个过程step及mysql报文",
    author="lindaye",
    author_email="454784911@qq.com",
    url="https://github.com/stellaye",
    packages=setuptools.find_packages(),
)

