# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
import dataclasses
import functools
import ipaddress
import json
import shlex
import socket
import urllib.error
import urllib.request
from asyncio import as_completed
from asyncio import create_task
from asyncio import to_thread
from dataclasses import InitVar
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union

import paramiko
from ipaddress import IPv4Address
from ipaddress import IPv6Address

from .enum import *
from .lib import *
from .utils import *
from .utils import logger

__all__ = [
    'IPv4',
    'IPv6',
    'IPLike',
    'IPLoc',
    'IP',
    'getfqdn',
    'ip_addr',
    'ip_loc',
    'ip_loc_aio',
    'myip',
    'ping',
    'ping_aio',
    'sort_ip',
    'ssh_password',
    'ssh_password_aio',
]


@functools.total_ordering
@dataclasses.dataclass(eq=False, repr=False)
class IPv4(IPv4Address):
    _ip: IPLike

    __ignore_attr__ = ['_ALL_ONES', 'compressed', '_constants', '_max_prefixlen', 'max_prefixlen', '_netmask_cache',
                       'packed', 'text', ]

    def __post_init__(self):
        super(IPv4, self).__init__(self._ip)

    @property
    def text(self) -> str:
        return self.exploded


@dataclasses.dataclass(eq=False, repr=False)
class IPv6(IPv6Address):
    _ip: IPLike

    __ignore_attr__ = IPv4.__ignore_attr__ + ['_HEXTET_COUNT', '_HEX_DIGITS', ]

    def __post_init__(self):
        super(IPv6, self).__init__(self._ip)

    @property
    def text(self) -> str:
        return self.exploded


IPLike = Union[IPv4, IPv6, IPv4Address, IPv6Address, str, bytes, int]


@dataclasses.dataclass
class IPLoc(BaseData):
    IPv4: Optional[Any] = None
    city: str = None
    country_code: str = None
    country_name: str = None
    latitude: str = None
    longitude: str = None
    postal: str = None
    state: str = None
    addr: InitVar[Optional[Any]] = None

    priority: Priority = Priority.LOW

    __ignore_attr__ = ['priority', ]

    def __post_init__(self, log: Optional[Log], addr: Optional[Union[IPLike, IP]] = None):
        super().__post_init__(log)
        if self.IPv4 is None and addr:
            self.IPv4 = addr
        elif self.IPv4 is None:
            self.IPv4 = myip()

    @property
    def ip(self) -> Optional[Any]:
        return self.IPv4

    @property
    def post_init(self) -> IPLoc:
        self.attrs_set(**ip_loc(self.IPv4))
        return self

    @property
    async def post_init_aio(self) -> IPLoc:
        self.attrs_set(**await ip_loc_aio(str(self.IPv4), priority=self.priority))
        return self

    @property
    def text(self) -> str:
        return str(self.IPv4)


@dataclasses.dataclass(eq=False)
class IP(BaseDataDescriptor):
    _id: Optional[Union[IP, IPLike]] = None
    loc: Optional[IPLoc] = None
    name: Optional[str] = None
    ping: Optional[bool] = None
    ssh: Optional[bool] = None
    priority: Priority = Priority.LOW

    addr: InitVar[Optional[Union[IPLike, IP]]] = None

    __ignore_kwarg__ = ['priority', ]

    def __post_init__(self, log: Optional[Log], addr: Optional[Union[IPLike, IP]] = None):
        super().__post_init__(log)
        if self._id is None and addr:
            self._id = addr
        self._id = ip_addr(socket.gethostbyname(str(self.ip)) if self.ip else None)

    @property
    def ip(self) -> Union[IPv4, IPv6]:
        return self._id

    def post_init(self, loc: bool = True, name: bool = True, ping_: bool = True, ssh: bool = True) -> IP:
        self.loc = IPLoc(addr=self.ip).post_init if loc else self.loc
        self.name = socket.getfqdn(self.text) if name else self.name
        self.ping = ping(self.ip) if ping_ else self.ping
        self.ssh = ssh_password(self.ip) if ssh else self.ssh
        return self

    async def post_init_aio(self, loc: bool = True, name: bool = True, ping_: bool = True, ssh: bool = True) -> IP:
        task = list()
        if loc:
            task.append(create_task(IPLoc(addr=self.ip, priority=self.priority).post_init_aio, name=f'loc-{self.text}'))
        if name:
            task.append(create_task(getfqdn(self.ip, priority=self.priority), name=f'name-{self.text}'))
        if ping_:
            task.append(create_task(ping_aio(self.ip, priority=self.priority), name=f'ping-{self.text}'))
        if ssh:
            task.append(create_task(ssh_password_aio(self.ip, priority=self.priority), name=f'ssh-{self.text}'))
        if task:
            for coro in as_completed([self.task(t) for t in task]):
                name, result = await coro
                setattr(self, name.split('-')[0], result)
        return self

    @staticmethod
    async def task(task: asyncio.Task) -> tuple[str, Any]:
        return task.get_name(), await task

    @property
    def text(self) -> str:
        return str(self._id)


@Nap.OSERROR.retry_async()
async def getfqdn(ip: Optional[Union[IPLike, IP]], priority: Priority = Priority.LOW, sem: Sem = None) -> str:
    sem = sem if sem else setup_package.sem
    return await sem.run(to_thread(socket.getfqdn, str(ip)), priority=priority, sem=Sems.SOCKET)


@functools.cache
def ip_addr(ip: Optional[Union[IPLike, IP]] = None) -> Union[IPv4, IPv6]:
    ip = str(ip) if ip else myip()
    try:
        return IPv4(ip)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    try:
        return IPv6(ip)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass

    raise ValueError(f'{ip} does not appear to be an IPv4 or IPv6 address')


@Nap.HTTPJSON.retry_sync()
def ip_loc(ip: Optional[Union[IPLike, IP]] = None) -> dict:
    """
    IP location.

    Args:
        ip: ip.

    Returns:
        dict:
    """
    ip = str(ip) if ip else myip()
    with urllib.request.urlopen(f'https://geolocation-db.com/json/697de680-a737-11ea-9820-af05f4014d91/'
                                f'{ip}') as loc:
        try:
            return json.loads(loc.read().decode())
        except json.decoder.JSONDecodeError as exception:
            logger.child().warning(f'{ip}', f'{exception}')
            return dict()


async def ip_loc_aio(ip: Any, priority: Priority = Priority.LOW, sem: Sem = None) -> dict:
    """
    IP location.

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        dict:
    """
    sem = sem if sem else setup_package.sem
    return await sem.run(to_thread(ip_loc, str(ip)), priority=priority, sem=Sems.HTTP)


@Nap.HTTPJSON.retry_sync()
def myip() -> str:
    return ip if (ip := urllib.request.urlopen('https://ident.me').read().decode('utf8')) else '127.0.0.1'


@Nap.OSERROR.retry_sync()
def ping(ip: Any = None) -> Optional[bool]:
    """
     Pings host.

     Args:
         ip: ip.

     Returns:
         Optional[bool]:
     """
    ip = str(ip) if ip else myip()
    pings = 3
    cmd_out = cmd(f'sudo ping -c {pings} {shlex.quote(str(ip))}')
    if cmd_out.rc == 0:
        rv = True
    elif cmd_out.rc == 2:
        rv = False
    else:
        rv = None
    return rv


async def ping_aio(ip: Any = None, priority: Priority = Priority.LOW, sem: Sem = None) -> Optional[bool]:
    """
    Pings host.

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        Optional[bool]:
    """
    sem = sem if sem else setup_package.sem
    return await sem.run(to_thread(ping, str(ip)), priority=priority, sem=Sems.PING)


def sort_ip(data: Iterable[str], rv_dict: bool = False, rv_ipv4: bool = False,
            rv_base: bool = False) -> Union[list[IPv4Address], list[str], list[IP], dict[str, IPv4Address]]:
    """
    Sort IPs.
    Args:
        data: data.
        rv_dict: dict rv with IPv4Address.
        rv_ipv4: list rv with IPv4Address.
        rv_base: list rv with IPBase and str.

    Returns:
        Union[list[IPv4Address], list[str], dict[str, IPv4Address]]:
    """
    data = iter_split(data)
    if rv_dict or rv_ipv4 or rv_base:
        rv = sorted([ipaddress.ip_address(addr) for addr in iter_split(data)])
        if rv_dict or rv_base:
            rv = {item.exploded: item for item in rv}
            if rv_base:
                rv = [IP(value, key) for key, value in rv.items()]
        return rv
    return sorted(iter_split(data), key=IPv4Address)


@Nap.OSERROR.retry_sync()
def ssh_password(ip: Any = None) -> Optional[bool]:
    """
    SSH password.

    Args:
        ip: ip.

    Returns:
        Optional[bool]:
    """
    ip = str(ip) if ip else myip()
    passwords = {str(): False, 'fake': False}
    users = dict(root=False, fake=False)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log = logger.child()
    for user in users:
        for passwd in passwords:
            while True:
                try:
                    client.connect(ip, username=user, password=passwd, look_for_keys=False, timeout=3)
                    break
                except socket.timeout:
                    # 'Unreachable'
                    users[user] = None
                    passwords[passwd] = None
                    break
                except (paramiko.ssh_exception.NoValidConnectionsError, OSError, EOFError):
                    # 'Unable to connect'
                    users[user] = None
                    passwords[passwd] = None
                    break
                except paramiko.ssh_exception.BadAuthenticationType as exception:
                    if 'publickey' in repr(exception):
                        users[user] = False
                        passwords[passwd] = False
                        break
                except paramiko.ssh_exception.AuthenticationException:
                    users[user] = True
                    passwords[passwd] = True
                    break
                except paramiko.SSHException:
                    # Quota exceeded, retrying with delay...
                    users[user] = None
                    passwords[passwd] = None
                    Nap.OSERROR.sleep()
                    break
                except (urllib.error.URLError, OSError) as exception:
                    log.warning('Waiting for connection', f'{ip=}', f'{repr(exception)=}')
                    Nap.OSERROR.sleep()
                    continue
                except (ConnectionResetError, paramiko.ssh_exception.SSHException, EOFError) as exception:
                    log.warning(f'Waiting for connection', f'{ip=}', f'{repr(exception)=}')
                    Nap.OSERROR.sleep()
                    continue
                users[user] = True
                passwords[passwd] = True
                try:
                    client.exec_command('hostname;w')
                    log.critical('Connection established', f'{ip=}', f'{user=}', f'{passwd=}')
                except paramiko.ssh_exception.SSHException as exception:
                    log.error('Connection established with error ', f'{ip=}', f'{user=}', f'{passwd=}', f'{exception=}')
                break
        if users['fake'] is None and users['root'] is None:
            value = None
        elif passwords[str()] or passwords['fake'] or users['root'] or users['fake']:
            value = True
        else:
            value = False
        return value


async def ssh_password_aio(ip: Any = None, priority: Priority = Priority.LOW, sem: Sem = None) -> Optional[bool]:
    """
    SSH password..

    Args:
        ip: ip.
        priority: priority.
        sem: sem.

    Returns:
        Optional[bool]:
    """
    sem = sem if sem else setup_package.sem
    return await sem.run(to_thread(ssh_password, str(ip)), priority=priority, sem=Sems.SSH)
