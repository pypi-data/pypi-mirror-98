#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""Bapy Package."""
from __future__ import annotations

import dataclasses
import datetime
# noinspection PyCompatibility
# noinspection PyCompatibility
import xml
from typing import Any
from typing import Optional
from typing import Union

import dpath.util
import xmltodict

_log.info('Package.defaults()', fm(Package.defaults()))


class BapyException(Exception):
    """Custom base class for all Repo exception types."""


class BapyFrameBackBack(BapyException):
    def __init__(self, message):
        self.message = message


class BapyGitDirectoryIsDirty(BapyException):
    def __init__(self, message):
        self.message = message


class BapyInvalidIP(BapyException):
    def __init__(self, ip):
        self.ip = ip
        self.message = f'Invalid IP: {self.ip}'


class NmapProtoEnum(EnumDict):
    IP = 'P'
    SCTP = 'S'
    TCP = 'T'
    UDP = 'U'


class NmapStateEnum(EnumDict):
    CLOSED = EnumDict.auto()
    FILTERED = EnumDict.auto()
    OPEN = EnumDict.auto()


@dataclasses.dataclass
class NmapParse(DataPostDefault):
    args: str = str()
    debugging: dict = datafield(default_factory=dict)
    host: Union[dict, list] = datafield(default_factory=dict)
    ip: str = str()
    name: EnumDictType = None
    nmaprun: dict = datafield(default_factory=dict)
    rc: int = int()
    runstats: dict = datafield(default_factory=dict)
    scaninfo: dict = datafield(default_factory=dict)
    scanner: str = str()
    stderr: Union[str, list] = str()
    start: str = str()
    startstr: str = str()
    verbose: dict = datafield(default_factory=dict)
    version: str = str()
    xmloutputversion: str = str()
    elapsed: str = datafield(default=str(), init=False)
    extraports: list[dict] = datafield(default_factory=list, init=False)
    os: dict = datafield(default_factory=dict, init=False)
    port: list[dict] = datafield(default_factory=list, init=False)
    ports: dict = datafield(default_factory=dict, init=False)

    def __post_init__(self):
        elapsed = dpath.util.get(self.nmaprun, '/runstats/finished/elapsed', default=str())
        self.elapsed = str(datetime.timedelta(seconds=int(elapsed.split('.')[0]))).split('.')[0]
        self.os = self.host.get('os', dict())
        self.ports = self.host.get('ports', dict())
        extraports = self.ports.get('extraports', list())
        self.extraports = [extraports] if isinstance(extraports, dict) else extraports
        port = self.ports.get('port', list())
        self.port = [port] if isinstance(port, dict) else port

    @classmethod
    def parse(cls, **kwargs):
        return cls(**kwargs | kwargs.get('nmaprun'))


@dataclasses.dataclass
class NmapProto(DataPostDefault):
    ip: Any
    sctp: Any
    tcp: Any
    udp: Any


@dataclasses.dataclass
class NmapState(DataPostDefault):
    closed: Any
    filtered: Any
    open = Any


@dataclasses.dataclass
class NmapServiceScript(DataPostDefault):
    name: Union[list, str]
    value: dict


@dataclasses.dataclass
class NmapPort(DataPostDefault):
    number: int
    state: NmapStateEnum
    proto: NmapProtoEnum
    script: Optional[NmapServiceScript] = None
    service: Optional[NmapServiceScript] = None


@dataclasses.dataclass
class NmapCodec(DataPostDefault):
    parsed: dict[str, dict]


@dataclasses.dataclass
class NmapCommand(DataPostDefault):
    _command: str = datafield(default=str(), init=False)
    _ip: Optional[IP] = None
    debug_async: bool = _env.debug_async.value
    hostname: tuple = 'kali', 'scan'
    log: Log = _log
    name: EnumDictType = None
    os: bool = False
    parse: NmapParse = datafield(default=None, init=False)
    pn: bool = True
    _port: NmapCommandPortTyping = str()
    samples: dict = datafield(default_factory=dict)
    script: NmapCommandScriptTyping = str()
    script_args: str = str()
    ss: bool = True
    su: bool = True
    sv: bool = False
    sy: bool = True
    sz: bool = True
    t: Optional[int] = None

    def __post_init__(self):
        self.install()
        self.command()

    def command(self, ip: Union[IPLike, IP] = None, port: NmapCommandPortTyping = None):
        self.ip = ip if ip else self.ip
        self.port = port if port else self.port

        _script = dict(category=['auth', 'broadcast', 'default', 'discovery', 'dos', 'exploit', 'external', 'fuzzer',
                                 'intrusive', 'malware', 'safe', 'version', 'vuln'],
                       exclude=['broadcast-*', 'ipv6-*', 'targets-ipv6-*', 'lltd-discovery', 'dns-brute',
                                'hostmap-robtex', 'http-robtex-shared-ns', 'targets-asn', 'hostmap-crtsh',
                                'http-icloud-*', 'http-virustotal', 'eap-info'],
                       args=['newtargets'], )
        script = f'({" or ".join(_script["category"])}) and not {" and not ".join(_script["exclude"])}' \
            if self.script == 'complete' else self.script
        script_args = ",".join(_script["args"]) \
            if self.script == 'complete' else self.script_args
        p = f' {self.port}' if self.port and self.port != '-' else self.port
        self._command = f'sudo nmap -R -r --reason -oX - ' \
                        f'{"-O --osscan-guess " if self.os else str()}' \
                        f'{f"-p{p} " if self.port else str()}' \
                        f'{"-Pn " if self.pn else str()}' \
                        f'{f"-script {script} " if script else str()}' \
                        f'{f"-script-args {script_args} " if script_args else str()}' \
                        f'{"-sS " if self.ss else str()}' \
                        f'{"-sU " if self.su else str()}' \
                        f'{"-sV --version-all " if self.sv else str()}' \
                        f'{"-sY " if self.sy else str()}' \
                        f'{"-sZ " if self.sz else str()}' \
                        f'-T{self.t if self.t else 4 if Machine.hostname in self.hostname else 3} ' \
                        f'{f"-{self.ip._id.version}" if self.ip else str()}' \
                        f'{self.ip.ip} ' \
                        f'| grep -v "Fetchfile found "'
        return self._command

    @staticmethod
    @once
    def install():
        Distro.install('nmap')

    @property
    def ip(self) -> Optional[Union[IPLike, IP]]:
        return self._ip

    @ip.setter
    def ip(self, value: Optional[Union[IPLike, IP]]):
        self._ip = IP(value)

    @property
    def port(self) -> Union[str, int]:
        return self._port

    @port.setter
    def port(self, value: Union[str, int]):
        self._port = value

    async def run(self, ip: str = str(), name: EnumDictType = None, port: NmapCommandPortTyping = None) -> NmapParse:
        self.ip = ip if ip else self.ip
        self.name = name if name else self.name

        if self.samples:
            cmd_out = CmdOut(str(), str(), int())
            nmaprun = self.samples[name].get(self.ip, dict())
        else:
            cmd_out = await aiocmd(self.command(port=port), utf8=True)
            try:
                nmaprun = xmltodict.parse(cmd_out.stdout, dict_constructor=dict,
                                          process_namespaces=True, attr_prefix='')['nmaprun']
            except xml.parsers.expat.ExpatError as exception:
                nmaprun = dict()
                cmd_out = CmdOut(str(), f'{exception=}, {self.command=}, {self.ip=}', 255)
                await self.log.aerror(f'{exception=}', f'{cmd_out.stdout=}', f'{self.command=}', f'{self.ip=}')

        self.parse = NmapParse.parse(ip=self.ip, name=self.name, nmaprun=nmaprun, rc=cmd_out.rc, stderr=cmd_out.stderr)
        return self.parse
