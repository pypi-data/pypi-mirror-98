![execsql logo](https://static-cdn.osdn.net/thumb/g/6/107/150x150_0.png)  *Multi-DBMS SQL script processor.*

*execsql.py* is a Python program that runs a SQL script stored in a text file 
against a PostgreSQL, MS-Access, SQLite, MS-SQL-Server, MySQL, MariaDB,
Firebird, or Oracle database, or an ODBC DSN.  *execsql* also supports a
set of special commands (metacommands) that can import and export data,
copy data between databases, and conditionally execute SQL statements and metacommands.  
These metacommands make up a control language that works the same across 
all supported database management systems (DBMSs). The metacommands are 
embedded in SQL comments, so they will be ignored by other script 
processors (e.g., *psql* for Postgres and *sqlcmd* for SQL Server).  The 
metacommands make up a toolbox that can be used to create both automated 
and interactive data processing applications.

The program's features and requirements are summarized below.
Complete documentation is available at
[http://execsql.osdn.io](http://execsql.osdn.io).

[![Downloads](https://pepy.tech/badge/execsql)](https://pypi.org/project/execsql/)  
[![Downloads](https://pepy.tech/badge/execsql/month)](https://pepy.tech/project/execsql/)


Capabilities
=========================

You can use *execsql* to:

* Import data from text files or spreadsheets into
  a database.
* Copy data between different databases, even databases using different
  types of DBMSs.
* Export tables and views as formatted text, comma-separated values (CSV), tab-separated
  values (TSV), OpenDocument spreadsheets, HTML tables, JSON, XML, LaTeX tables, HDF5
  tables, unformatted (e.g., binary) data, or several other formats.
* Export data to non-tabular formats using several different
  template processors.
* Display a table or view in a GUI dialog,
  optionally allowing the user to select a data row, enter a data
  value, or respond to a prompt.
* Display a pair of tables or views in a GUI dialog, allowing the user
  to compare data and find rows with matching or non-matching key values.
* Conditionally execute different SQL commands and metacommands based on the DBMS in use,
  the database in use, data values, user input, and other conditions.
* Execute blocks of SQL statements or *execsql* metacommands repeatedly, using
  any of three different looping methods.
* Use simple dynamically-created data entry forms to get user input.
* Write status or informational messages to the console or to a file 
  during the processing of a SQL script. Status messages and data exported in 
  text format can be combined in a single text file. Data tables can be 
  exported in a text format that is compatible with Markdown pipe tables,
  so that script output can be converted into a variety of document formats.
* Write more modular and maintainable SQL code by factoring repeated 
  code out into separate scripts, parameterizing the code using 
  substitution variables, and using the INCLUDE or SCRIPT metacommands 
  to merge the modules into a single stream of commands.
* Merge multiple elements of a workflow—e.g., data loading, summarization, and
  reporting—into a single script for better coupling of related steps and more
  secure maintenance.

Standard SQL provides no features for interacting with external files or 
with the user, or for controlling the flow of actions to be carried out
based either on data or on user input.  Some DBMSs provide these features,
but capabilities and syntax differ between DBMSs.  *execsql* provides 
these features in a way that operates identically across all supported 
DBMSs on both Linux and Windows.

*execsql* is inherently a command-line program that can operate in a completely 
non-interactive mode (except for password prompts). Therefore, it is suitable 
for incorporation into a toolchain controlled by a shell script (on Linux), 
batch file (on Windows), or other system-level scripting application. When 
used in this mode, the only interactive elements will be password prompts.
However, several metacommands generate interactive prompts and data
displays, so *execsql* scripts can be written to provide some user interactivity.

In addition, *execsql* automatically maintains a log that documents key 
information about each run of the program, including the databases that are 
used, the scripts that are run, and the user's choices in response to 
interactive prompts. Together, the script and the log provide documentation 
of all actions carried out that may have altered data.

The documentation includes 30 examples showing the use of
*execsql*'s metacommands, in both simple and complex scripts.


Syntax and Options
========================

Different forms of command lines, with varying arguments and options, are shown below.

Commands
------------------------

```
    execsql.py -ta [other options] sql_script_file Access_db 

    execsql.py -tf [other options] sql_script_file Firebird_host Firebird_db

    execsql.py -tm [other options] sql_script_file MySQL_host MySQL_db 

    execsql.py -tp [other options] sql_script_file Postgres_host Postgres_db

    execsql.py -ts [other options] sql_script_file SQL_Server_host SQL_Server_db

    execsql.py -to [other options] sql_script_file Oracle_host Oracle_service

    execsql.py -tl [other options] sql_script_file SQLite_db 

    execsql.py -tl [other options] sql_script_file DSN_name 
```

Most arguments and options can also be specified in a configuration file, so
only the script file name need be specified on the command line.

```
    execsql.py sql_script_file
```


Command-line Arguments
-----------------------------

```
     sql_script_file   The name of a text file of SQL commands to be executed. Required argument.

     Access_db         The name of the Access database against which to run the SQL.

     DSN_name          The data set name for an ODBC connection.

     Firebird_db       The name of the Firebird database against which to run the SQL.

     Firebird_host     The name of the Firebird host (server) against which to run the SQL. 

     MySQL_db          The name of the MySQL database against which to run the SQL.

     MySQL_host        The name of the MySQL host (server) against which to run the SQL.

     Oracle_host       The name of the Oracle host (server) against which to run the SQL.

     Oracle_service    The Oracle service name (database) against which to run the SQL.

     Postgres_db       The name of the Postgres database against which to run the SQL.

     Postgres_host     The name of the Postgres host (server) against which to run the SQL. 

     SQL_Server_db     The name of the SQL Server database against which to run the SQL.

     SQL_Server_host   The name of the SQL Server host (server) against which to run the SQL. 

     SQLite_db         The name of the SQLite database against which to run the SQL.
```

Command-line Options
------------------------

```
    -a value        Define the replacement for a substitution variable $ARG_x. 
    -d value        Automatically make directories used by the 	EXPORT
                    metacommand: 'n'-no (default); 'y'-yes.
    -e value        Character encoding of the database. Only used for some 
                      database types. 
    -f value        Character encoding of the script file. 
    -g value        Character encoding to use for output of the WRITE and EXPORT
                    metacommands. 
    -i value        Character encoding to use for data files imported with the 
                    IMPORT metacommand. 
    -m              Display the allowable metacommands, and exit. 
    -p value        The port number to use for client-server databases. 
    -s value        The number of lines of an IMPORTed file to scan to diagnose 
                    the quote and delimiter characters. 
    -t value        Type of database: 
                          'p'-Postgres, 
                          'f'-Firebird, 
                          'l'-SQLite, 
                          'm'-MySQL or MariaDB, 
                          'a'-Access, 
                          's'-SQL Server, 
                          'o'-Oracle,
                          'd'-DSN connection.
    -u value        The database user name (optional). 
    -v value        Use a GUI for interactive prompts. 
    -w              Do not prompt for the password when the user is specified. 
    -y              List all valid character encodings and exit. 
    -z value        Buffer size, in kb, to use with the IMPORT metacommand 
                    (the default is 32).
```

Requirements
===========================

The *execsql* program uses third-party Python libraries to communicate with 
different database and spreadsheet software. These libraries must be 
installed to use those programs with *execsql*. Only those libraries that 
are needed, based on the command line arguments and metacommands, must 
be installed. The libraries required for each database or spreadsheet 
application are:

* PosgreSQL: psycopg2.
* SQL Server: pydobc.
* MS-Access: pydobc and pywin32.
* MySQL or MariaDB: pymysql.
* Firebird: fdb.
* Oracle: cx-Oracle.
* DSN connections: pyodbc.
* OpenDocument spreadsheets: odfpy.
* Excel spreadsheets (read only): xlrd.

Connections to SQLite databases are made using Python's standard library, 
so no additional software is needed.

If the Jinja or Airspeed template processors will be used, those software
libraries must also be installed.

All of these libraries can be installed from the Python Package Index (PyPI)
using *pip*.


An Illustration
=================

The following code illustrates the use of metacommands and substitution variables.
Lines starting with "\-\- !x!" are metacommands that implement *execsql*-specific features.
Identifiers enclosed in pairs of exclamation points (!!) are substitution variables
that have been defined with the SUB metacommand.  The "$date_tag" variable is
a substitution variable that is defined by *execsql* itself rather than by the user.

    -- ==== Configuration ====
    -- Put the (date-tagged) logfile name in the 'inputfile' substitution variable.
    -- !x! SUB inputfile logs/errors_!!$date_tag!!
    -- Ensure that the export directory will be created if necessary.
    -- !x! CONFIG MAKE_EXPORT_DIRS Yes

    -- ==== Display Fatal Errors ====
    -- !x! IF(file_exists(!!inputfile!!))
        -- Import the data to a staging table.
        -- !x! IMPORT TO REPLACEMENT staging.errorlog FROM !!inputfile!!
        -- Create a view to display only fatal errors.
        create temporary view fatals as
            select user, run_time, process
            from   staging.errorlog
            where  severity = 'FATAL';
        -- !x! IF(HASROWS(fatals))
            -- Export the fatal errors to a dated report.
            -- !x! EXPORT fatals TO reports/error_report_!!$date_tag!! AS CSV
            -- Also display it to the user in a GUI.
            -- !x! PROMPT MESSAGE "Fatal errors in !!inputfile!!:" DISPLAY fatals
        -- !x! ELSE
            -- !x! WRITE "There are no fatal errors."
        -- !x! ENDIF
    -- !x! ELSE
        -- !x! WRITE "There is no error log."
    -- !x! ENDIF
    drop table if exists staging.errorlog cascade;

The IMPORT metacommand reads the specified file and loads the data into
the target (staging) table, automatically choosing appropriate data types
for each column.  The EXPORT metacommand saves the data in a CSV file
that can be used by other applications.  The PROMPT metacommand produces
a GUI display of the data as follows:

![PROMPT display of 'fatals' view](http://execsql.osdn.io/_images/fatals.png)

The complete documentation includes additional examples.


Documentation, Tools, and Templates
===========================================

Complete documentation is at [OSDN](http://execsql.osdn.io).

Three tools that illustrate the use of execsql, and that are useful in their
own right, are:

* [Upsert scripts](https://execsql-upsert.osdn.io): A set of *execsql* scripts for Postgres, MariaDB/MySQL, and SQL Server that will perform a merge (upsert) operation on multiple tables simultaneously, performing a variety of data integrity checks.  These scripts use the *information_schema* views and so operate on any table in any supported DBMS without customization.

* [Staging table comparison scripts](https://execsql-compare.osdn.io): A set of *execsql* scripts for Postgres, MariaDB/MySQL, and SQL Server that will perform various comparisons of the data in a staging table to the data in the corresponding base table.  These scripts use the *information_schema* views and so operate on any table in any supported DBMS without customization.

* [Glossary creation script](https://execsql-glossary.osdn.io): An *execsql* script that will produce a table of terms (e.g., column names) and definitions, and that may be useful to accompany a database export.

The set of [execsql script templates](https://osdn.net/projects/execsql/releases/p16640) available from OSDN includes several types of templates that may be useful in conjunction with execsql.py. These are:

* *execsql.conf*: An annotated version of the configuration file that includes all configuration settings and notes on their usage.

* *script_template.sql*: A framework for SQL scripts that make use of several *execsql* features.  It includes sections for custom configuration settings, custom logfile creation, and reporting of unexpected script exits (through user cancellation or errors).

* *config_settings.sqlite* and *example_config_prompt.sql*: A SQLite database containing specifications for all settings configurable with the CONFIG metacommand, in the form used by the PROMPT ENTRY_FORM metacommand, and a SQL script illustrating how this database can be used to prompt the user for some or all of the configuration settings.




Copyright and License
================================

Copyright (c) 2007-2021 R.Dreas Nielsen

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. The GNU General Public License is available at
http://www.gnu.org/licenses/.

