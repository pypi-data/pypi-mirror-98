from typing import Protocol, Optional, List
from dataclasses import dataclass, field
from .net import AnyIPv4Address, AnyIPNetwork, AnyIPv6Address
from enum import Enum


class MountTypes(Enum):
    BIND = "bind"
    VOLUME = "volume"
    IMAGE = "image"
    TMPFS = "tmpfs"


@dataclass
class ContainerMount(object):
    type: MountTypes
    src: Optional[str]
    dst: str
    writable: bool


@dataclass
class ContainerDescription(object):
    image: str
    network_name: Optional[str] = None
    mounts: List[ContainerMount] = field(default_factory=list)
    ip: Optional[AnyIPv4Address] = None
    ip6: Optional[AnyIPv6Address] = None  # Not supported by podman
    network_alias: Optional[str] = None  # rubicon note: use this field as possible
    pod_name: Optional[str] = None


@dataclass
class PodDescription(object):
    name: str
    network_name: Optional[str] = None
    network_alias: Optional[str] = None


class BambooDriverProtocol(Protocol):
    """Protocol between namespace management tool and pybamboo.
    PyBamboo promise to handle these error for edge cases:
    - `NotImplementedError` for operations does not implement.
    - `RuntimeError` for runtime errors.
    """

    def set_dryrun(self, enabled: bool = True) -> None:
        ...

    def run_command(self, *args) -> int:
        ...

    def create_network(
        self, name: str, subnet: AnyIPNetwork, ip_range: AnyIPNetwork
    ) -> None:
        ...

    def remove_network(self, name: str, force: Optional[bool] = None) -> None:
        ...

    def exists_network(self, name: str) -> bool:
        ...

    def connect_network(
        self, network_name: str, name: str, alias: Optional[str] = None
    ) -> None:
        ...

    def disconnect_network(self, network_name: str, name: str) -> None:
        ...

    def create_container(self, name: str, description: ContainerDescription) -> None:
        ...

    def remove_container(self, name: str) -> None:
        ...

    def kill_container(self, name: str) -> None:
        ...

    def stop_container(self, name: str) -> None:
        ...

    def start_container(self, name: str) -> None:
        ...

    def pause_container(self, name: str) -> None:
        ...

    def unpause_container(self, name: str) -> None:
        ...

    def exists_container(self, name: str) -> bool:
        ...

    def pull_image(self, name: str) -> None:
        ...

    def exists_image(self, name: str) -> bool:
        ...

    def create_pod(self, description: PodDescription) -> None:
        """Create a new pod with `description`.
        From podman manual: "Pods are a group of one or more containers sharing the same network, pid and ipc namespaces."
        """
        ...

    def remove_pod(self, name: str) -> None:
        ...

    def exists_pod(self, name: str) -> bool:
        ...
