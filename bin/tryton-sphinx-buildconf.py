#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    tryton-sphinx-buildconf

    A script which could be invoked to generate the sphinx config for a given
    tryton configuration file and database name

    :copyright: (c) 2011 by Douglas Morato
    :license: BSD, see LICENSE for more details.
"""
from tryton_sphinx import BaseSource, DataSource
from tryton_sphinx.utils import iter_sql_models

INDEXER_SETTINGS = """
#############################################################################
## indexer settings
#############################################################################

indexer
{
	# memory limit, in bytes, kiloytes (16384K) or megabytes (256M)
	# optional, default is 32M, max is 2047M, recommended is 256M to 1024M
	mem_limit		= 32M

	# maximum IO calls per second (for I/O throttling)
	# optional, default is 0 (unlimited)
	#
	# max_iops		= 40


	# maximum IO call size, bytes (for I/O throttling)
	# optional, default is 0 (unlimited)
	#
	# max_iosize		= 1048576


	# maximum xmlpipe2 field length, bytes
	# optional, default is 2M
	#
	# max_xmlpipe2_field	= 4M


	# write buffer size, bytes
	# several (currently up to 4) buffers will be allocated
	# write buffers are allocated in addition to mem_limit
	# optional, default is 1M
	#
	# write_buffer		= 1M


	# maximum file field adaptive buffer size
	# optional, default is 8M, minimum is 1M
	#
	# max_file_field_buffer	= 32M
}
"""

SEARCHD_SETTINGS = """
#############################################################################
## searchd settings
#############################################################################

searchd
{
	# [hostname:]port[:protocol], or /unix/socket/path to listen on
	# known protocols are 'sphinx' (SphinxAPI) and 'mysql41' (SphinxQL)
	#
	# multi-value, multiple listen points are allowed
	# optional, defaults are 9312:sphinx and 9306:mysql41, as below
	#
	# listen			= 127.0.0.1
	# listen			= 192.168.0.1:9312
	# listen			= 9312
	# listen			= /var/run/searchd.sock
	listen			= 9312
	listen			= 9306:mysql41

	# log file, searchd run info is logged here
	# optional, default is 'searchd.log'
	log			= /var/log/searchd.log

	# query log file, all search queries are logged here
	# optional, default is empty (do not log queries)
	query_log		= /var/log/query.log

	# client read timeout, seconds
	# optional, default is 5
	read_timeout		= 5

	# request timeout, seconds
	# optional, default is 5 minutes
	client_timeout		= 300

	# maximum amount of children to fork (concurrent searches to run)
	# optional, default is 0 (unlimited)
	max_children		= 30

	# PID file, searchd process ID file name
	# mandatory
	pid_file		= /var/log/searchd.pid

	# max amount of matches the daemon ever keeps in RAM, per-index
	# WARNING, THERE'S ALSO PER-QUERY LIMIT, SEE SetLimits() API CALL
	# default is 1000 (just like Google)
	max_matches		= 1000

	# seamless rotate, prevents rotate stalls if precaching huge datasets
	# optional, default is 1
	seamless_rotate		= 1

	# whether to forcibly preopen all indexes on startup
	# optional, default is 1 (preopen everything)
	preopen_indexes		= 1

	# whether to unlink .old index copies on succesful rotation.
	# optional, default is 1 (do unlink)
	unlink_old		= 1

	# attribute updates periodic flush timeout, seconds
	# updates will be automatically dumped to disk this frequently
	# optional, default is 0 (disable periodic flush)
	#
	# attr_flush_period	= 900


	# instance-wide ondisk_dict defaults (per-index value take precedence)
	# optional, default is 0 (precache all dictionaries in RAM)
	#
	# ondisk_dict_default	= 1


	# MVA updates pool size
	# shared between all instances of searchd, disables attr flushes!
	# optional, default size is 1M
	mva_updates_pool	= 1M

	# max allowed network packet size
	# limits both query packets from clients, and responses from agents
	# optional, default size is 8M
	max_packet_size		= 8M

	# crash log path
	# searchd will (try to) log crashed query to 'crash_log_path.PID' file
	# optional, default is empty (do not create crash logs)
	#
	# crash_log_path		= /var/log/crash


	# max allowed per-query filter count
	# optional, default is 256
	max_filters		= 256

	# max allowed per-filter values count
	# optional, default is 4096
	max_filter_values	= 4096


	# socket listen queue length
	# optional, default is 5
	#
	# listen_backlog		= 5


	# per-keyword read buffer size
	# optional, default is 256K
	#
	# read_buffer		= 256K


	# unhinted read size (currently used when reading hits)
	# optional, default is 32K
	#
	# read_unhinted		= 32K


	# max allowed per-batch query count (aka multi-query count)
	# optional, default is 32
	max_batch_queries	= 32


	# max common subtree document cache size, per-query
	# optional, default is 0 (disable subtree optimization)
	#
	# subtree_docs_cache	= 4M


	# max common subtree hit cache size, per-query
	# optional, default is 0 (disable subtree optimization)
	#
	# subtree_hits_cache	= 8M


	# multi-processing mode (MPM)
	# known values are none, fork, prefork, and threads
	# optional, default is fork
	#
	workers			= threads # for RT to work


	# max threads to create for searching local parts of a distributed index
	# optional, default is 0, which means disable multi-threaded searching
	# should work with all MPMs (ie. does NOT require workers=threads)
	#
	# dist_threads		= 4


	# binlog files path; use empty string to disable binlog
	# optional, default is build-time configured data directory
	#
	# binlog_path		= # disable logging
	# binlog_path		= /var/data # binlog.001 etc will be created there


	# binlog flush/sync mode
	# 0 means flush and sync every second
	# 1 means flush and sync every transaction
	# 2 means flush every transaction, sync every second
	# optional, default is 2
	#
	# binlog_flush		= 2


	# binlog per-file size limit
	# optional, default is 128M, 0 means no limit
	#
	# binlog_max_log_size	= 256M


	# per-thread stack size, only affects workers=threads mode
	# optional, default is 64K
	#
	# thread_stack			= 128K


	# per-keyword expansion limit (for dict=keywords prefix searches)
	# optional, default is 0 (no limit)
	#
	# expansion_limit		= 1000


	# RT RAM chunks flush period
	# optional, default is 0 (no periodic flush)
	#
	# rt_flush_period		= 900


	# query log file format
	# optional, known values are plain and sphinxql, default is plain
	#
	# query_log_format		= sphinxql


	# version string returned to MySQL network protocol clients
	# optional, default is empty (use Sphinx version)
	#
	# mysql_version_string	= 5.0.37


	# trusted plugin directory
	# optional, default is empty (disable UDFs)
	#
	# plugin_dir			= /usr/local/sphinx/lib


	# default server-wide collation
	# optional, default is libc_ci
	#
	# collation_server		= utf8_general_ci


	# server-wide locale for libc based collations
	# optional, default is C
	#
	# collation_libc_locale	= ru_RU.UTF-8


	# threaded server watchdog (only used in workers=threads mode)
	# optional, values are 0 and 1, default is 1 (watchdog on)
	#
	# watchdog				= 1


	# SphinxQL compatibility mode (legacy columns and their names)
	# optional, default is 0 (SQL compliant syntax and result sets)
	#
	# compat_sphinxql_magics	= 1
}

# --eof--
"""

if __name__ == '__main__':
    from optparse import OptionParser
    usage = "usage: %prog [options] database filename"
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config', dest="config",
        default=None, help="The tryton configuration file to use")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("Expected 2 argument got %d" % len(args))

    if options.config is not None:
        from trytond.config import CONFIG
        CONFIG.configfile = options.config
        CONFIG.load()

    # Register the classes and get all the modules from the pool
    from trytond.modules import register_classes
    register_classes()

    from trytond.pool import Pool
    pool = Pool(args[0])
    pool.init()

    with open(args[1], 'wb') as file:
        base_source = BaseSource.from_tryton_config(args[0])
        file.write(base_source.as_string())

        for model_object in iter_sql_models(pool):
            ds = DataSource.from_model(model_object, base_source)
            if not ds.sql_query:
                # If there are no attributes which have select=1 then there will
                # be no sql query, so just ignore those data sources
                continue
            file.write(ds.as_string())

        file.write(INDEXER_SETTINGS)
        file.write(SEARCHD_SETTINGS)
