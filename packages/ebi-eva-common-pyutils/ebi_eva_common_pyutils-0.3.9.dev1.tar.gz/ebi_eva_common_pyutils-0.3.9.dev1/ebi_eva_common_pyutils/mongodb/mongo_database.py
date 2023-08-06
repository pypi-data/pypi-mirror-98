import copy
from cached_property import cached_property
from ebi_eva_common_pyutils.logger import AppLogger
from ebi_eva_common_pyutils.command_utils import run_command_with_output
from pymongo import MongoClient, uri_parser


class MongoDatabase(AppLogger):
    def __init__(self, uri: str, secrets_file: str = None, db_name: str = "admin"):
        self.uri = uri
        self.secrets_file = secrets_file
        self.db_name = db_name

    @cached_property
    def uri_with_db_name(self):
        """
        Return URI with the database name substituted
        ex:
        If the URI is mongodb://user@localhost:27017/admin and database name is eva_fcatus_90,
        then the URI with the database name will be mongodb://user@localhost:27017/admin
        """
        if self.db_name == "admin":
            return self.db_name
        uri_components = uri_parser.parse_uri(self.uri)
        # Hack needed to log in to a different DB but retain authentication source
        # See https://docs.mongodb.com/v4.0/reference/connection-string/#records-database and https://docs.mongodb.com/v4.0/reference/connection-string/#urioption.authSource
        uri_with_db_name = f"mongodb://{uri_components['username']}@" + \
                           ",".join([node + ':' + str(port) for node, port in uri_components['nodelist']]) + \
                           f"/{self.db_name}?authSource={uri_components['options'].get('authSource', 'admin')}"
        return uri_with_db_name

    @cached_property
    def mongo_handle(self):
        if self.secrets_file:
            with open(self.secrets_file) as secrets_file_handle:
                mongo_password = secrets_file_handle.read().strip()
            return MongoClient(self.uri, password=mongo_password)
        else:
            return MongoClient(self.uri)

    def __del__(self):
        self.mongo_handle.close()

    def create_index_on_collections(self, collection_index_map):
        collection_index_map_copy = copy.deepcopy(collection_index_map)
        for collection_name, index_info_map in collection_index_map_copy.items():
            for name, index_info in index_info_map.items():
                print(index_info)
                keys = index_info['key']
                del (index_info['ns'])
                del (index_info['v'])
                del (index_info['key'])
                del (index_info['background'])
                self.mongo_handle[self.db_name][collection_name].create_index(keys, name=name, **index_info)

    def drop(self):
        self.mongo_handle.drop_database(self.db_name)

    def get_collection_names(self):
        return self.mongo_handle[self.db_name].list_collection_names()

    def get_indexes(self):
        collection_index_map = {}
        for collection_name in self.get_collection_names():
            collection_index_map[collection_name] = self.mongo_handle[self.db_name][collection_name].index_information()
        return collection_index_map

    def enable_sharding(self):
        enable_sharding_command = f"mongo --host {self.uri}  --eval 'sh.enableSharding(\"{self.db_name}\")' " \
                                  f"< {self.secrets_file}"
        run_command_with_output(f"Enabling sharding in the database {self.uri_with_db_name}...",
                                enable_sharding_command, log_error_stream_to_output=True)

    def shard_collections(self, collections_shard_key_map, collections_to_shard):
        for collection_name in collections_to_shard:
            shard_key, shard_key_uniqueness_flag = collections_shard_key_map.get(collection_name, (["_id"], False))
            # Shard key representation in the format {"key1": 1, "key2": 1}
            shard_key_repr = "{{{0}}}".format(",".join([f'"{attribute}": 1' for attribute in shard_key]))
            shard_collection_command = f'sh.shardCollection(' \
                                       f'"{self.db_name}.{collection_name}", ' \
                                       f'{shard_key_repr}, {str(shard_key_uniqueness_flag).lower()})'
            sharding_command = f"mongo --host {self.uri}  " \
                               f"--eval " \
                               f"'{shard_collection_command}' " \
                               f"< {self.secrets_file}"
            run_command_with_output(f"Sharding collection {collection_name} in the database {self.uri_with_db_name} "
                                    f"with key {shard_key_repr}...", sharding_command,
                                    log_error_stream_to_output=True)

    def dump_data(self, dump_dir):
        if self.secrets_file:
            # mongodump is notorious for printing passwords in plain text: https://jira.mongodb.org/browse/TOOLS-1020
            # So we need a file with the password to work around that
            mongodump_command = f"mongodump --uri {self.uri_with_db_name}  " \
                                f"--out {dump_dir} < {self.secrets_file}"
            run_command_with_output(f"Running mongodump for URI: {self.uri}", mongodump_command,
                                    log_error_stream_to_output=True)
        else:
            self.error("Cannot run mongodump without secrets file! See https://jira.mongodb.org/browse/TOOLS-1020")

    def restore_data(self, dump_dir, mongorestore_args=None):
        mongorestore_args = " ".join([f"--{arg} {val}"
                                      for arg, val in mongorestore_args.items()]) if mongorestore_args else ""
        num_parallel_collections_arg = "numParallelCollections"
        if self.secrets_file:
            # mongorestore is notorious for printing passwords in plain text: https://jira.mongodb.org/browse/TOOLS-1020
            # So we need a file with the password to work around that

            # noIndexRestore - Do not restore indexes because MongoDB 3.2 does not have index compatibility with MongoDB 4.0
            mongorestore_command = f"mongorestore --uri {self.uri_with_db_name} " \
                                   f"{mongorestore_args} " \
                                   f"--dir {dump_dir} " \
                                   f"< {self.secrets_file}"
            run_command_with_output("mongorestore", mongorestore_command, log_error_stream_to_output=True,
                                    return_process_output=True)
        else:
            self.error("Cannot run mongorestore without secrets file! See https://jira.mongodb.org/browse/TOOLS-1020")
