Using MySQL with ``ffscraper``
==============================

This currently houses my notes for setting up and using MySQL on Fedora 28 for use in this project, with some temporary documentation or scripts that may be useful.

The prompts are used fairly interchangeably here, ``$`` will represent a bash prompt whereas ``mysql>`` represents that the MySQL prompt is being used.

Setting Up MySQL on Fedora 28
-----------------------------

This is heavily adapted from [#]_, start by downloading the yum package from the `MySQL Yum Download Page <http://dev.mysql.com/downloads/repo/yum/>`_.

.. code-block:: bash

                $ sudo rpm -Uvh platform-and-version-specific-package-name.rpm
                $ sudo dnf install mysql-community-server
                $ sudo service mysqld start
                $ sudo grep 'temporary password' /var/log/mysqld.log
                $ mysql -uroot -p
                mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'chooseyourpassword';

Installing Connector/Python
---------------------------

.. code-block:: bash

                $ pip install mysql-connector-python

Creating a User for the MySQL Python Connector
----------------------------------------------

I had a copy of [#]_ within reach and based a few of these sections on their suggestions.

The example below grants quite a few privileges to ``fanfictionuser``, separating these out such that only root may perform certain actions would typically be prefereable. In such a case, granting ``select``, ``insert``, ``delete``, and ``update`` may be prefereable.

.. code-block:: sql

                mysql> create database fanfictiondb;
                mysql> create user 'fanfictionuser'@'localhost'
                    -> identified by 'chooseyourpassword';
                mysql> grant select, insert, update, delete, index, alter, create, drop
                    -> on fanfictiondb.* to 'fanfictionuser'@'localhost';

Appendix:
---------

Helpful commands that I can never seem to remember and have to look up when I need them.

1. Starting MySQL Server: ``$ sudo service mysqld start``
2. Checking Server Status: ``$ sudo service mysqld status``
3. Show users: ``mysql> select user from mysql.user;``

References:
-----------

.. [#] "A Quick Guide to Using the MySQL Yum Repository" https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/
.. [#] Welling, Luke and Laura Thomson, "PHP and MySQL Web Development. Fourth Edition." Pearson Education, Inc. 2009. ISBN: 978-0-672-32916-6
