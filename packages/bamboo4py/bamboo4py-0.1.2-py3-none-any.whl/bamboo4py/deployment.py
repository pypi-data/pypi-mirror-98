from typing import Any, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union
from dataclasses import dataclass
from netaddr import IPSet, IPAddress, IPNetwork
from pathlib import Path

from .drivers.protocol import (
    BambooDriverProtocol,
    ContainerDescription,
    ContainerMount,
    MountTypes,
    PodDescription,
)
from .drivers.change_actions import (
    ChangeAction,
    ChangeSet,
    ChangeSteps,
    ConnectNetworkAction,
    CreateNetworkAction,
    CreatePodAction,
    DisconnectNetworkAction,
    KillContainerAction,
    NewContainerAction,
    PullImageAction,
    RemoveContainerAction,
    RemovePodAction,
    StartContainerAction,
    StopContainerAction,
)
from .tyaml import read_disk_size, disk_size_str_to_bytes


@dataclass
class ServiceEndpoint(object):
    name: str
    port: int


@dataclass
class ShipExposedEndpoint(object):
    name: str
    end: str
    port: int


@dataclass
class ExternalFolderResource(object):
    name: str
    type: str
    mount: str
    max_size: Optional[int]  # bytes
    min_size: Optional[int]  # bytes


@dataclass
class Resource(object):
    name: str
    type: str
    descriptor: Dict[str, Any]

    def as_external_folder(self) -> ExternalFolderResource:
        max_size_raw = (
            self.descriptor["max_size"] if "max_size" in self.descriptor else None
        )
        min_size_raw = (
            self.descriptor["min_size"] if "min_size" in self.descriptor else None
        )
        max_size = read_disk_size(max_size_raw) if max_size_raw else None
        min_size = read_disk_size(min_size_raw) if min_size_raw else None
        if max_size_raw and (not max_size):
            raise ValueError(
                "parse error: max_size. wrong format of '{}'.".format(max_size_raw)
            )
        elif min_size_raw and (not min_size):
            raise ValueError(
                "parse error: min_size. wrong format of '{}'.".format(min_size_raw)
            )
        return ExternalFolderResource(
            name=self.name,
            type=self.type,
            max_size=disk_size_str_to_bytes(*max_size) if max_size else None,
            min_size=disk_size_str_to_bytes(*min_size) if min_size else None,
            mount=self.descriptor["mount"],
        )


@dataclass
class ServiceContainer(object):
    id: str
    image: str


@dataclass
class Service(object):
    name: str
    version: str
    shared: bool
    id: str
    ip: Optional[str]  # IPv4 Address
    resources: List[Resource]
    network_alias: Optional[str]
    containers: List[ServiceContainer]

    def get_ip(self) -> IPAddress:
        "Return object of `.ip`"
        return IPAddress(self.ip)


@dataclass
class Ship(object):
    name: str
    version: str
    id: str
    services: Dict[str, Service]  # key is service id
    tags: List[Tuple[str, str]]
    exposes: List[ShipExposedEndpoint]

    def shared_services(self) -> List[Service]:
        return list(filter(lambda x: x.shared, self.services.values()))

    def isolated_services(self) -> List[Service]:
        return list(filter(lambda x: not x.shared, self.services.values()))

    def get_used_ips(self) -> Iterator[IPAddress]:
        for serv in self.services.values():
            yield serv.get_ip()


@dataclass
class Deployment(object):
    name: str
    subnet: Optional[str]  # a CIDR
    ships: List[Ship]

    def get_services(self) -> Dict[str, Service]:
        all_services = {}
        for ship in self.ships:
            all_services.update(ship.services)
        return all_services

    def find_service(self, name: str) -> Optional[Service]:
        for s in self.get_services().values():
            if s.name == name:
                return s
        return None

    def shared_service(self) -> List[Service]:
        return list(filter(lambda x: x.shared, self.get_services().values()))

    def isolated_services(self) -> List[Service]:
        return list(filter(lambda x: not x.shared, self.get_services().values()))

    def get_subnet(self) -> IPNetwork:
        return IPNetwork(self.subnet)

    def get_used_ips(self) -> Iterator[IPAddress]:
        for ship in self.ships:
            yield from ship.get_used_ips()

    def get_avaliable_ips(self) -> IPSet:
        avaliable_ipset = IPSet((self.get_subnet(),))
        for addr in self.get_used_ips():
            avaliable_ipset.remove(addr)
        return avaliable_ipset


class BambooExecutor(object):
    """Executor returns a `ChangeAction` or a series of it which can make actual changes to environment."""

    def __init__(
        self, driver: BambooDriverProtocol, bamboo_data_dir: Union[Path, str]
    ) -> None:
        self.driver = driver
        self.bamboo_data_dir = Path(bamboo_data_dir)

    def execute_changes(self, action: ChangeAction):
        action.do_action(self.driver)

    @staticmethod
    def create_name_from_id(bamboo_id: str) -> str:
        """Create correct name for containers and network from bamboo id.
        Bamboo uses slash to split id to parts, which is not supported to be names of containers and (virtual) networks.
        This function translate slash to _, _ to __.
        """
        return bamboo_id.replace("_", "__").replace("/", "_")

    def get_deployment_data_dir(self, deployment_name: str):
        return (
            self.bamboo_data_dir / "deployments" / deployment_name / "data"
        ).absolute()

    def local_mode_deploy_ship(
        self, new_ship: Ship, old_deployment: Deployment
    ) -> ChangeAction:
        """Deploy `new_ship` under `old_deployment`.
        Bamboo will instantly make changes to a deployment in local mode.

        The only one ship in `old_deployment` will be replaced in place by `new_ship`.
        """
        changeset = ChangeSteps()
        changeset.pre.append(self.pull_not_found_images_of_ship(new_ship))
        new_shared_services = new_ship.shared_services()
        new_isolated_services = new_ship.isolated_services()
        network_name = self.create_name_from_id(
            old_deployment.name
        )  # TODO: (rubicon) per-ship isolated network
        deployment_data_dir = self.get_deployment_data_dir(old_deployment.name)
        old_shared_services: List[
            Service
        ] = list()  # old shared services should be stopped
        if not self.driver.exists_network(network_name):
            changeset.pre.append(
                CreateNetworkAction(
                    network_name, old_deployment.subnet, old_deployment.subnet
                )
            )
        for s in old_deployment.shared_service():
            old_shared_services.append(
                s
            )  # we add all shared services in old deployment, but it's not mean all those are old
        for service in new_shared_services:
            old_shared_service = old_deployment.find_service(service.name)
            if old_shared_service and old_shared_service.shared:
                if old_shared_service.version != service.version:
                    changeset.actions.append(
                        self.remove_service(old_shared_service, network_name)
                    )
                    changeset.actions.append(
                        self.create_service_containers(
                            service, deployment_data_dir, network_name
                        )
                    )
                else:
                    # we don't need to update the service because the one in description have same version to deployed one.
                    # remove it from `old_shared_services`, the service not that old.
                    old_shared_services.remove(old_shared_service)
                    # but we need update the service in the new ship: replace the one have new id with the one have been there
                    new_ship.services.pop(service.id)
                    new_ship.services[old_shared_service.id] = old_shared_service
            else:
                if old_shared_service:  # stop the old one if it does not shared
                    changeset.pre.append(
                        self.kill_service_containers(old_shared_service)
                    )
                    changeset.actions.insert(
                        0, self.remove_container(old_shared_service.id)
                    )
                # just add the service if it have not deployed
                changeset.actions.append(
                    self.create_service_containers(
                        service, deployment_data_dir, network_name
                    )
                )
        for serv in old_shared_services:
            changeset.pre.append(self.kill_service_containers(serv))
        for service in new_isolated_services:
            changeset.actions.append(
                self.create_service_containers(
                    service, deployment_data_dir, network_name
                )
            )
        if len(old_deployment.ships) > 0:
            old_ship = old_deployment.ships.pop()
            for serv in old_ship.services.values():
                if not serv.shared or serv.id in old_shared_services:
                    changeset.pre.append(self.kill_service_containers(serv))
                    changeset.pre.append(self.remove_service(serv, network_name))
                    changeset.actions.insert(0, self.remove_container(serv.id))
        old_deployment.ships.append(new_ship)
        return changeset

    def create_container(
        self, service: Service, container: ServiceContainer, deployment_data_dir: Path
    ) -> ChangeAction:
        mounts = []
        for resource in service.resources:
            if resource.type == "external_folder":
                exfolder = resource.as_external_folder()
                # TODO: (rubicon) perform min_size checking to prevent the container creating on the place against limitation
                folder_path = (
                    deployment_data_dir / "folders" / exfolder.name
                ).absolute()
                mounts.append(
                    ContainerMount(
                        MountTypes.BIND,
                        src=str(folder_path),
                        dst=exfolder.mount,
                        writable=True,
                    )
                )
        container_name = self.create_name_from_id(container.id)
        changeset = ChangeSet([])
        changeset.changes.append(
            NewContainerAction(
                container_name,
                ContainerDescription(
                    image=container.image,
                    mounts=mounts,
                    pod_name=self.create_name_from_id(service.id),
                ),
            )
        )
        return changeset

    def connect_network_from_service(
        self, network_name: str, service: Service
    ) -> ChangeAction:
        return ConnectNetworkAction(
            network_name,
            self.create_name_from_id(service.id),
            alias=service.network_alias,
        )

    def remove_container(self, service_id: str) -> ChangeAction:
        return RemoveContainerAction(self.create_name_from_id(service_id))

    def disconnect_network_from_service(
        self, network_name: str, service: Service
    ) -> ChangeAction:
        return DisconnectNetworkAction(
            network_name, self.create_name_from_id(service.id)
        )

    def remove_service(self, service: Service, network_name: str) -> ChangeAction:
        return ChangeSet(
            [
                self.disconnect_network_from_service(network_name, service),
                self.remove_container(service.id),
                RemovePodAction(self.create_name_from_id(service.id)),
            ]
        )

    def create_service_containers(
        self, service: Service, deployment_data_dir: Path, network: str
    ) -> ChangeAction:
        steps = ChangeSteps()
        if self.driver.exists_pod(self.create_name_from_id(service.id)):
            steps.pre.append(RemovePodAction(self.create_name_from_id(service.id)))
        steps.pre.append(
            CreatePodAction(
                PodDescription(
                    name=self.create_name_from_id(service.id),
                    network_name=network,
                    network_alias=service.network_alias,
                )
            )
        )
        for serv_con in service.containers:
            steps.actions.append(
                self.create_container(service, serv_con, deployment_data_dir)
            )
        return steps

    def pull_not_found_images_of_ship(self, ship: Ship) -> ChangeAction:
        changeset = []
        for serv in ship.services.values():
            for serv_con in serv.containers:
                if not self.driver.exists_image(serv_con.image):
                    changeset.append(PullImageAction(serv_con.image))
        return ChangeSet(list(changeset))

    def kill_service_containers(self, service: Service) -> ChangeAction:
        changes = ChangeSet([])
        for con in service.containers:
            changes.changes.append(
                KillContainerAction(self.create_name_from_id(con.id))
            )
        return changes

    def start_service_containers(self, service: Service) -> ChangeAction:
        changes = ChangeSet([])
        for con in service.containers:
            changes.changes.append(
                StartContainerAction(self.create_name_from_id(con.id))
            )
        return changes

    def stop_service_containers(self, service: Service) -> ChangeAction:
        changes = ChangeSet([])
        for con in service.containers:
            changes.changes.append(
                StopContainerAction(self.create_name_from_id(con.id))
            )
        return changes

    def local_mode_start_deployment(self, deployment: Deployment) -> ChangeSet:
        assert len(deployment.ships) <= 1
        if len(deployment.ships) == 0:
            return ChangeSet([])
        changeset = ChangeSet([])
        for serv in deployment.get_services().values():
            changeset.changes.append(self.start_service_containers(serv))
        return changeset

    def local_mode_down_deployment(self, deployment: Deployment) -> ChangeSet:
        assert len(deployment.ships) <= 1
        if len(deployment.ships) == 0:
            return ChangeSet([])
        changeset = ChangeSet([])
        for serv in deployment.get_services().values():
            changeset.changes.append(self.stop_service_containers(serv))
        return changeset

    def local_mode_kill_deployment(self, deployment: Deployment) -> ChangeSet:
        assert len(deployment.ships) <= 1
        if len(deployment.ships) == 0:
            return ChangeSet([])
        changeset = ChangeSet([])
        for serv in deployment.get_services().values():
            changeset.changes.append(self.kill_service_containers(serv))
        return changeset

    def local_mode_update_deployment(
        self,
        deployment: Deployment,
        ship: Ship,
        ignore_version=False,
        ignore_name=False,
    ) -> ChangeSet:
        assert len(deployment.ships) <= 1
        changeset = ChangeSet([])
        if len(deployment.ships) == 1:
            old_ship = deployment.ships[0]
            if (not ignore_name) and old_ship.name == ship.name:
                if (not ignore_version) and old_ship.version != ship.version:
                    changeset.changes.append(
                        self.local_mode_deploy_ship(ship, deployment)
                    )
        elif len(deployment.ships) == 0:
            changeset.changes.append(self.local_mode_deploy_ship(ship, deployment))
        else:
            raise RuntimeError("local mode only accept one-ship deployment")
        return changeset
