from bamboo.drivers.net import AnyIPNetwork
from typing import (
    List,
    Mapping,
    MutableSequence,
    Optional,
    Protocol,
    Sequence,
    Sized,
    Union,
    runtime_checkable,
)
from dataclasses import dataclass
from .protocol import BambooDriverProtocol, ContainerDescription, PodDescription


def add_indent(s: str, indent: str) -> str:
    lines = s.splitlines(True)
    return "".join(map(lambda x: "{}{}".format(indent, x), lines))


def format_action(
    action_name: str,
    args: Union[Sequence[str], Mapping[str, str]],
    action_color: str = "blue",
):
    real_args: Sequence[str]
    if isinstance(args, Mapping):
        real_args = []
        for k in args:
            real_args.append("{}={}".format(k, args[k]))
    else:
        real_args = args
    from click import style

    return "{} {}".format(style(action_name, fg=action_color), ", ".join(real_args))


class ChangeAction(Protocol):
    def do_action(self, driver: BambooDriverProtocol):
        ...


@runtime_checkable
class SelfDescribed(Protocol):
    def self_describe(self) -> str:
        ...


class ChangeSet(ChangeAction, Sized, SelfDescribed):
    def __init__(self, changes: List[ChangeAction]) -> None:
        self.changes = changes

    def do_action(self, driver: BambooDriverProtocol):
        for c in self.changes:
            c.do_action(driver)

    def __len__(self) -> int:
        count = 0
        for x in self.changes:
            if isinstance(x, Sized):
                count += len(x)
            else:
                count += 1
        return count

    def self_describe(self) -> str:
        if len(self) == 0:
            return ""
        return "\n".join(
            filter(
                lambda x: x,
                map(
                    lambda x: x.self_describe()
                    if isinstance(x, SelfDescribed)
                    else str(x),
                    self.changes,
                ),
            )
        )

    @property
    def empty(self):
        return len(self) > 0


class ChangeSteps(ChangeAction, Sized, SelfDescribed):
    def __init__(self) -> None:
        self.pre: List[ChangeAction] = []
        self.actions: List[ChangeAction] = []
        self.defered: List[ChangeAction] = []

    def do_action(self, driver: BambooDriverProtocol):
        self.create_change_set().do_action(driver)

    def create_change_set(self):
        return ChangeSet(self.create_list())

    def self_describe(self) -> str:
        from click import style

        INDENT = " " * 4
        lines: List[str] = []
        titles = [
            style("PRE:", fg="blue"),
            style("ACTIONS:", fg="blue"),
            style("DEFERED:", fg="blue"),
        ]
        if sum(map(len, [self.pre, self.actions, self.defered])) > 0:
            for title, seq in zip(titles, [self.pre, self.actions, self.defered]):
                if seq:
                    lines.append(title)
                    for el in seq:
                        content = (
                            el.self_describe()
                            if isinstance(el, SelfDescribed)
                            else str(el)
                        )
                        if content:
                            lines.append(
                                add_indent(
                                    content,
                                    INDENT,
                                )
                            )
        else:
            return ""
        return "\n".join(lines)

    @property
    def empty(self):
        return len(self) > 0

    def __len__(self) -> int:
        count = 0
        for seq in [self.pre, self.actions, self.defered]:
            for x in seq:
                if isinstance(x, Sized):
                    count += len(x)
                else:
                    count += 1
        return count

    def create_list(self):
        result = []
        result.extend(self.pre)
        result.extend(self.actions)
        result.extend(self.defered)
        return result


@dataclass
class KillContainerAction(ChangeAction, SelfDescribed):
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.kill_container(self.container_name)

    def self_describe(self) -> str:
        from click import style

        return "{} {}".format(style("KillContainer", fg="red"), self.container_name)


@dataclass
class StopContainerAction(ChangeAction, SelfDescribed):
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.stop_container(self.container_name)

    def self_describe(self) -> str:
        from click import style

        return "{} {}".format(style("StopContainer", fg="red"), self.container_name)


@dataclass
class NewContainerAction(ChangeAction, SelfDescribed):
    container_name: str
    container_description: ContainerDescription

    def do_action(self, driver: BambooDriverProtocol):
        driver.create_container(self.container_name, self.container_description)

    def self_describe(self) -> str:
        from click import style

        return "{} {}, {}".format(
            style("NewContainer", fg="green"),
            self.container_name,
            self.container_description,
        )


@dataclass
class RemoveContainerAction(ChangeAction, SelfDescribed):
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.remove_container(self.container_name)

    def self_describe(self) -> str:
        from click import style

        return "{} {}".format(style("RemoveContainer", fg="red"), self.container_name)


@dataclass
class PauseContainerAction(ChangeAction, SelfDescribed):
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.pause_container(self.container_name)

    def self_describe(self) -> str:
        from click import style

        return "{} {}".format(style("PauseContainer", fg="red"), self.container_name)


@dataclass
class StartContainerAction(ChangeAction, SelfDescribed):
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.start_container(self.container_name)

    def self_describe(self) -> str:
        return format_action(
            "StartContainer", (self.container_name,), action_color="green"
        )


@dataclass
class CreateNetworkAction(ChangeAction, SelfDescribed):
    name: str
    ip_range: AnyIPNetwork
    subnet: AnyIPNetwork

    def do_action(self, driver: BambooDriverProtocol):
        driver.create_network(self.name, self.subnet, self.ip_range)

    def self_describe(self) -> str:
        from dataclasses import asdict

        return format_action("CreateNetwork", asdict(self), action_color="green")


@dataclass
class RemoveNetworkAction(ChangeAction, SelfDescribed):
    name: str
    force: Optional[bool] = None

    def do_action(self, driver: BambooDriverProtocol):
        driver.remove_network(self.name, self.force)

    def self_describe(self) -> str:
        return format_action("RemoveNetwork", (self.name,), "red")


@dataclass
class PullImageAction(ChangeAction, SelfDescribed):
    name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.pull_image(self.name)

    def self_describe(self) -> str:
        return format_action("PullImage", (self.name,))


@dataclass
class Failed(ChangeAction, SelfDescribed):
    reason: str
    linked_action: SelfDescribed

    def do_action(self, driver: BambooDriverProtocol):
        raise RuntimeError(self.reason, self.linked_action)

    def self_describe(self) -> str:
        return format_action(
            "FAILED", (self.reason, self.linked_action.self_describe())
        )


@dataclass
class ConnectNetworkAction(
    ChangeAction, SelfDescribed
):  # avoid this unless run as root, podman does not support `podman network connect` for rootless containers
    network_name: str
    target_name: str
    alias: Optional[str] = None

    def do_action(self, driver: BambooDriverProtocol):
        driver.connect_network(self.network_name, self.target_name, self.alias)

    def self_describe(self) -> str:
        return format_action(
            "ConnectNetwork",
            {
                "network": self.network_name,
                "target": self.target_name,
                **({"alias": self.alias} if self.alias else {}),
            },
        )


@dataclass
class DisconnectNetworkAction(
    ChangeAction, SelfDescribed
):  # avoid this as the reason for `ConnectNetworkAction`
    network_name: str
    container_name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.disconnect_network(self.network_name, self.container_name)

    def self_describe(self) -> str:
        return format_action(
            "DisconnectNetwork",
            {"network": self.network_name, "container": self.container_name},
        )


@dataclass
class CreatePodAction(ChangeAction, SelfDescribed):
    description: PodDescription

    def do_action(self, driver: BambooDriverProtocol):
        driver.create_pod(self.description)

    def self_describe(self) -> str:
        return format_action(
            "CreatePod", (str(self.description),), action_color="green"
        )


@dataclass
class RemovePodAction(ChangeAction, SelfDescribed):
    name: str

    def do_action(self, driver: BambooDriverProtocol):
        driver.remove_pod(self.name)

    def self_describe(self) -> str:
        return format_action("RemovePod", (self.name,), action_color="red")
