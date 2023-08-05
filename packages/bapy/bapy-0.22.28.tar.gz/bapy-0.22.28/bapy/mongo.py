# -*- coding: utf-8 -*-
from __future__ import annotations

import dataclasses
import pickle
import re
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

import envtoml
import motor.motor_asyncio
import psutil
import pymongo.database
import pymongo.errors
from bson import Binary
from bson import CodecOptions
from bson import ObjectId
from bson.binary import USER_DEFINED_SUBTYPE
from bson.codec_options import TypeDecoder
from bson.codec_options import TypeRegistry
from libnmap.parser import NmapParser
from pymongo import ReturnDocument

from .enum import *
from .ip import *
from .lib import *
from .utils import *

__all__ = [
    'mongo_conf',
    'MongoPickledBinaryDecoder',
    'MongoConn',
    'MongoBase',
    'MongoBase',
    'MongoDoc',
    'MongoCol',
    'MongoDocIP',
    'MongoColIP',
    'DaemonDoc',
    'DaemonCol',
]

mongo_conf = '.mongo.toml'

MongoDBMotor = motor.motor_asyncio.AsyncIOMotorDatabase
MongoDBPy = pymongo.database.Database
MongoDB = Union[MongoDBMotor, MongoDBPy]

MongoClientMotor = motor.motor_asyncio.AsyncIOMotorClient
MongoClientPy = pymongo.MongoClient
MongoClient = Union[MongoClientMotor, MongoClientPy]

MongoColMotor = motor.motor_asyncio.AsyncIOMotorCollection
MongoColPy = pymongo.database.Collection
MongoCollection = Union[MongoColMotor, MongoColPy]

MongoCursorMotor = motor.motor_asyncio.AsyncIOMotorCursor
MongoCursorPy = pymongo.cursor.Cursor
MongoCursor = Union[MongoCursorMotor, MongoCursorPy]

MongoValue = Optional[Union[bool, dict, list, str]]
MongoFieldValue = dict[str, MongoValue]


class MongoPickledBinaryDecoder(TypeDecoder):
    bson_type = Binary

    def transform_bson(self, value):
        if value.subtype == USER_DEFINED_SUBTYPE:
            # noinspection PickleLoad
            return pickle.loads(value)
        return value


@dataclasses.dataclass
class MongoConn(BaseData):
    codec: bool = None
    connectTimeoutMS: Optional[int] = 200000
    name: str = 'test'
    host: Optional[str] = '127.0.0.1'
    maxPoolSize: Optional[int] = Sem.mongo * 2
    password: Optional[str] = str()
    port: Optional[int] = None
    retry: bool = True
    serverSelectionTimeoutMS: Optional[int] = 300000
    srv: bool = False
    username: Optional[str] = str()
    codec_options: CodecOptions = datafield(default=None, init=False)
    file: Optional[Union[Path, str]] = datafield(default='.mongo.toml', init=False)

    __ignore_attr__ = ['col_name', ]

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
        self.file = Path(self.file) if Path(self.file).is_file() else setup_package.home / self.file \
            if (setup_package.home / self.file).is_file() else None
        self.attrs_set(**envtoml.load(self.file.text) if self.file else {})
        if self.codec and self.codec_options is None:
            self.codec_options = CodecOptions(type_registry=TypeRegistry(
                [MongoPickledBinaryDecoder()], fallback_encoder=MongoConn.fallback_encoder_pickle))

    @Nap.MONGO.retry_sync()
    def client(self, db: Optional[str] = None) -> Union[MongoClient, MongoDB]:
        if self.host == '127.0.0.1' and psutil.MACOS:
            cmd('mongossh.sh')
        func = MongoClientMotor if aioloop() else MongoClientPy
        return func(f'mongodb{"+srv" if self.srv else str()}://'
                    f'{str() if (u := ":".join([self.username, self.password])) == ":" else f"{u}@"}{self.host}'
                    f'{f":{self.port}" if self.port and not self.srv else str()}/{db if db else self.name}'
                    f'{"?retryWrites=true&w=majority" if self.retry else str()}',
                    connectTimeoutMS=self.connectTimeoutMS, maxPoolSize=self.maxPoolSize,
                    serverSelectionTimeoutMS=self.serverSelectionTimeoutMS).get_database(db if db else self.name)

    @Nap.MONGO.retry_sync()
    def db(self, name: Optional[str] = None) -> MongoDB:
        name = name if name else self.name
        rv = self.client(db=name)
        return rv.get_database(name=name) if isinstance(rv, (MongoClientPy, MongoClientMotor)) \
            else rv.client.get_database(name=name)

    @Nap.MONGO.retry_sync()
    def col(self, name: str = None, db: Optional[str] = None, codec: Optional[CodecOptions] = None) -> MongoCollection:
        c = dict(codec_options=codec) if codec else dict(codec_options=self.codec_options) if self.codec_options else {}
        return self.db(name=db).get_collection(**dict(name=name if name else self.col_name) | c)

    @property
    def col_name(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def fallback_encoder_pickle(value) -> Binary:
        return Binary(pickle.dumps(value), USER_DEFINED_SUBTYPE)


@dataclasses.dataclass(eq=False)
class MongoBase(BaseDataDescriptor):
    _id: Union[str, ObjectId] = None
    conn: MongoConn = datafield(default_factory=MongoConn)
    priority: Priority = Priority.LOW
    sem: Sem = datafield(default_factory=Sem)

    __ignore_attr__ = []
    __ignore_kwarg__ = ['conn', 'priority', 'sem', ]

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
        if not self.sem:
            self.sem = setup_package.sem
        self.__ignore_attr__ = Obj(self).clsinspect(AttributeKind.PROPERTY)
        self.col_name = re.sub('(Doc|Col).*', '', self.__class__.__name__).lower()
        self.conn = self.conn if self.conn else MongoConn()
        self.col: MongoCollection = self.conn.col(self.col_name)
        self.count_documents = self.col.count_documents
        self.delete_one = self.col.delete_one
        self.delete_many = self.col.delete_many
        self.distinct = self.col.distinct
        self.drop = self.col.drop
        self.estimated_document_count = self.col.estimated_document_count
        self.find = self.col.find
        self.find_one = self.col.find_one
        self.find_one_and_delete = self.col.find_one_and_delete
        self.find_one_and_update = self.col.find_one_and_update
        self.insert_one = self.col.insert_one
        self.insert_many = self.col.insert_many
        self.update_many = self.col.update_many

    @Nap.MONGO.retry_async()
    async def run(self, func, /, *args, **kwargs):
        return await self.sem.run(func, *args, priority=self.priority, **kwargs)

    @property
    def text(self) -> str:
        return str(self._id)


_Doc = TypeVar('_Doc', bound='MongoDoc')


@dataclasses.dataclass(eq=False)
class MongoDoc(MongoBase):
    _id: Union[str, ObjectId] = None

    def __post_init__(self, log: Optional[Log]):
        super(MongoDoc, self).__post_init__(log)

    @Nap.MONGO.retry_sync()
    def find_sync(self, instance: bool = True) -> Union[dict, MongoDoc, _Doc]:
        """
        Find one _id (doc) and returns instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(self.find_one({'_id': self._id}), instance)

    async def find_async(self, instance: bool = True) -> Union[dict, MongoDoc, _Doc]:
        """
        Find one _id (doc) and returns instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(await self.run(self.find_one, filter={'_id': self._id}), instance)

    @classmethod
    def rv(cls, doc: dict = None, instance: bool = True) -> Union[dict, MongoDoc, _Doc]:
        doc = doc if doc else dict()
        rv = doc.copy()
        return cls(**rv) if instance else rv

    async def update_async(self, instance: bool = True) -> Union[dict, MongoDoc, _Doc]:
        """
        Find one _id (doc), updates and returns and updated instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(await self.run(self.find_one_and_update, filter={'_id': self._id},
                                      update={'$set': await self.find_async(instance=False) | self.kwargs},
                                      return_document=ReturnDocument.AFTER, upsert=True), instance)

    @Nap.MONGO.retry_sync()
    def update(self, instance: bool = True) -> Union[dict, MongoDoc, _Doc]:
        """
        Find one _id (doc), updates and returns and updated instance of Mongo or dict for the document.

        Args:
            instance: instance.

        Returns:
             Union[dict, Mongo]:
        """
        return self.rv(self.find_one_and_update({'_id': self._id},
                                                {'$set': self.find_sync(instance=False) | self.kwargs},
                                                return_document=ReturnDocument.AFTER, upsert=True), instance)


_MongoDoc = TypeVar('_MongoDoc', bound=MongoDoc)
_Col = TypeVar('_Col', bound='MongoCol')


@dataclasses.dataclass
class MongoCol(MongoBase):
    _cls: Type[_MongoDoc] = MongoDoc
    chain: ChainMap[dict] = datafield(default_factory=ChainMap)
    chain_sorted: ChainMap[dict] = datafield(default_factory=ChainMap)
    dct: dict = datafield(default_factory=dict)
    dct_sorted: dict = datafield(default_factory=dict)
    lst: list[dict] = datafield(default_factory=list)
    lst_sorted: list[dict] = datafield(default_factory=list)
    obj: list[_MongoDoc] = datafield(default_factory=list)
    obj_sorted: list[_MongoDoc] = datafield(default_factory=list)
    unique: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_obj: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_obj_sorted: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_sorted: Union[list[Any], list[ObjectId]] = datafield(default_factory=list)
    unique_text: list[str] = datafield(default_factory=list)
    unique_text_sorted: list[str] = datafield(default_factory=list)

    __ignore_attr__ = ['_id', ]

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)

    def map(self, data: list = None, field: str = '_id', instance: bool = True,
            sort: bool = False) -> Union[list[str], list[Any]]:
        """
        Type call based on annotations of list of values.

        Args:
            field: field.
            data: data.
            instance: Returns list of _id str or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = data if data else self.unique
        if field == '_id' and self.conn.codec:
            self.unique_obj = data
        rv = data
        if (t := Obj(self._cls).annotation(field)) and instance and not self.conn.codec and not any(
                [len(data) == 1, isinstance(data[0], (str, int, bool, bytes)), isinstance(t[0](), SeqNoStrArgs)]):
            rv = [item if isinstance(item, (*t, ObjectId)) else t[0](item) for item in data]
            if field == '_id':
                self.unique_obj = rv
        if field != '_id':
            return sorted(rv) if sort else rv
        self.unique_obj_sorted = sorted(rv)
        self.unique_text = [item if isinstance(item, (str, int)) else str(item) for item in self.unique]
        self.unique_text_sorted = sorted(self.unique_text)
        return self.unique_sorted

    def _chain(self):
        self.chain_sorted = ChainMap(*self.lst_sorted)
        self.chain = ChainMap(*self.lst)

    def _set(self, item, sort: bool = False):
        if sort:
            self.lst_sorted.append(self._cls.rv(item, instance=False))
            self.obj_sorted.append(self._cls.rv(item))
            del self.dct_sorted[item['_id']]['_id']
        else:
            self.dct[item['_id']] = item
            self.lst.append(self._cls.rv(item, instance=False))
            self.obj.append(self._cls.rv(item))
            del self.dct[item['_id']]['_id']

    async def set_async(self) -> Union[_Col, MongoCol]:
        for item in await self.unique_async():
            self.dct_sorted[item] = await self.run(self.find_one, {'_id': item})
            self._set(self.dct_sorted[item].copy(), sort=True)

        for item in await self.run(self.find().to_list, None):
            # for item in await self.find().to_list(None):
            self._set(item)
        self._chain()
        return self

    @Nap.MONGO.retry_sync()
    def set_sync(self) -> Union[_Col, MongoCol]:
        for item in self.unique_sync():
            self.dct_sorted[item] = self.find_one({'_id': item})
            self._set(self.dct_sorted[item].copy(), sort=True)
        for item in self.find():
            self._set(item)
        self._chain()
        return self

    async def unique_async(self, field: str = '_id', instance: bool = True, sort: bool = False) -> list:
        """
        Unique _id

        Args:
            field: field.
            instance: Returns list of _id str or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = await self.run(self.distinct, field)
        # data = await self.distinct(field)
        if field == '_id':
            self.unique = data
            self.unique_sorted = sorted(data)
        return self.map(data, field, instance, sort)

    @Nap.MONGO.retry_sync()
    def unique_sync(self, field: str = '_id', instance: bool = True, sort: bool = False) -> list:
        """
        Unique _id

        Args:
            field: field.
            instance: Returns list of _id or list of _id instances.
            sort: sort.

        Returns:
            Union[list[str], list[Any]]:
        """
        data = self.distinct(field)
        if field == '_id':
            self.unique = data
            self.unique_sorted = sorted(data)
        return self.map(data, field, instance, sort)


@dataclasses.dataclass(eq=False)
class MongoDocIP(IP, MongoDoc):

    def __post_init__(self, log: Optional[Log], addr: Optional[Union[IPLike, IP]] = None):
        super().__post_init__(addr)  # Only calls first class: IP
        MongoDoc.__post_init__(self, log)


_MongoDocIP = TypeVar('_MongoDocIP', bound=MongoDocIP)
_ColIP = TypeVar('_ColIP', bound='MongoColIP')


@dataclasses.dataclass
class MongoColIP(MongoCol):
    _cls: Type[_MongoDocIP] = MongoDocIP

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)


@dataclasses.dataclass(eq=False)
class DaemonDoc(MongoDocIP):
    scan: Union[NmapParser, dict] = None

    def __post_init__(self, log: Optional[Log], addr: Union[IPLike, IP]):
        super().__post_init__(log, addr)


_DaemonDoc = TypeVar('_DaemonDoc', bound=MongoDoc)
_ColDaemon = TypeVar('_ColDaemon', bound='DaemonCol')


@dataclasses.dataclass
class DaemonCol(MongoColIP):
    _cls: Type[_DaemonDoc] = MongoDoc

    def __post_init__(self, log: Optional[Log]):
        super().__post_init__(log)
