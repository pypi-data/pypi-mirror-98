__version__ = "0.1.0"
from dataclasses import asdict, is_dataclass
from bamboo.drivers.podman import PodmanDriver
from os import PathLike
import sys
from .drivers.protocol import BambooDriverProtocol, ContainerDescription
import click
from typing import Any, Dict, List, Optional, Tuple, Union
from click import group, option, argument, echo, style
from pathlib import Path
from .tyaml import Document
from .deployment import (
    BambooExecutor,
    Resource,
    ServiceContainer,
    Ship,
    Service,
    ServiceEndpoint,
    Deployment,
    ShipExposedEndpoint,
)
from .drivers.net import AnyIPv4Address, asipaddress


BAMBOO_DEFAULT_SUBNET = "10.200.0.0/24"


def dataclass_instance_hash(ins) -> str:
    if not is_dataclass(ins):
        raise TypeError("except dataclasses, got {}".format(ins))
    d = asdict(ins)
    import json
    import hashlib

    s = json.dumps(d, sort_keys=True)
    hash = hashlib.sha3_256(s.encode("utf-8"))
    return hash.hexdigest()


class BambooConfiguration(object):
    def __init__(self, deployment: Deployment) -> None:
        self.data: Dict[str, Dict[str, Any]] = {}
        self.ship: Optional[Ship] = None
        self.deployment = deployment

    @property
    def deployment_name(self) -> str:
        return self.deployment.name

    @classmethod
    def open_ship_file(
        cls, deployment: Deployment, file_path: Union[Path, str]
    ) -> "BambooConfiguration":
        obj = BambooConfiguration(deployment)
        obj.load_ship_file(Path(file_path))
        return obj

    def load_ship_file(self, file_path: Path) -> Ship:
        file_path = file_path.absolute()
        doc = Document(str(file_path))
        yaml_content = doc.parse_yaml()
        name = str(yaml_content["ship"])
        version = str(yaml_content["version"])
        services_raw = yaml_content["services"]
        self_id = "{deployment_name}/{ship_name}/{ship_version}".format(
            deployment_name=self.deployment_name, ship_name=name, ship_version=version
        )
        assert isinstance(services_raw, List)
        exposes_raw: Optional[List[Dict[str, Any]]] = None
        if "exposes" in yaml_content:
            exposes_raw = yaml_content["exposes"]
            assert isinstance(exposes_raw, List)
        subnet_raw: str = (
            yaml_content["subnet"]
            if "subnet" in yaml_content
            else BAMBOO_DEFAULT_SUBNET
        )
        if self.deployment.subnet == "":
            self.deployment.subnet = subnet_raw
        assert (
            subnet_raw == self.deployment.subnet
        )  # deployment should have same subnet to ship
        # TODO (rubicon): try to remove this limitation (use ship-isolated network?)
        services: Dict[str, Service] = {}
        for serv_des in services_raw:
            serv_name = serv_des["name"]
            serv_file_path = serv_des["path"]
            args: Dict[str, Any] = {}
            if "args" in serv_des:
                args = serv_des["args"]
                assert isinstance(args, Dict)
            serv_id = "{ship_id}/{serv_name}".format(
                ship_id=self_id, serv_name=serv_name
            )
            serv_ip = serv_des["ip"] if "ip" in serv_des else None
            serv_network_alias = serv_des.get("network-alias", None)
            services[serv_id] = self.load_service_file(
                doc.expand_path(serv_file_path),
                serv_id,
                args,
                ip=serv_ip,
                network_alias=serv_network_alias,
            )
        exposes: List[ShipExposedEndpoint] = []
        if exposes_raw:
            for expose_des in exposes_raw:
                expose_name = expose_des["name"]
                expose_port = expose_des["port"]
                expose_end = expose_des["end"]
                expose_port = int(expose_port)
                exposes.append(
                    ShipExposedEndpoint(expose_name, expose_end, expose_port)
                )
        ship = Ship(name, version, self_id, services, [], exposes)
        self.ship = ship
        return ship

    def load_service_file(
        self,
        path: Path,
        serv_id: str,
        args: Dict[str, Any],
        *,
        ip: Optional[AnyIPv4Address] = None,
        network_alias: Optional[str] = None,
    ) -> Service:
        path = path.absolute()
        doc = Document(str(path))
        raw_content = doc.parse_yaml()
        if "params" in raw_content:
            params = raw_content["params"]
            assert isinstance(params, Dict)
            doc.check_params(params, args)
        name = str(raw_content["service"])
        version = str(raw_content["version"])
        result = doc.parse(
            deployment=self.deployment_name,
            service_name=name,
            service_version=version,
            service_id=serv_id,
            self_ip=str(ip),
            **args,
        )
        assert isinstance(result, Dict)
        image = result.get("image", None)
        containers_raw = result.get("containers", None)
        containers: List[ServiceContainer] = []
        if containers_raw:
            assert isinstance(containers_raw, List)
            for container_map in containers_raw:
                assert isinstance(containers_raw, Dict)
                container_name = container_map["name"]
                container_id = "{}/{}".format(serv_id, container_name)
                container_image = container_map["image"]
                containers.append(
                    ServiceContainer(id=container_id, image=container_image)
                )
        if image:
            assert isinstance(image, str)
            container_id = "{}/{}".format(serv_id, name)
            containers.append(ServiceContainer(id=container_id, image=image))
        shared = result.get("shared", False)
        resources_raw = result.get("resources")
        resources: List[Resource] = []
        if resources_raw:
            assert isinstance(resources_raw, List)
            for o in resources_raw:
                assert isinstance(o, Dict)
                res_name = o.pop("name")
                res_type = o.pop("type")
                resources.append(Resource(name=res_name, type=res_type, descriptor=o))
        return Service(
            name=name,
            version=version,
            shared=shared,
            id=serv_id,
            ip=str(asipaddress(ip)) if ip else None,
            resources=resources,
            network_alias=network_alias,
            containers=containers,
        )


class BambooDeploymentSaves(object):
    def __init__(self, datadir: Path) -> None:
        self.datadir = datadir

    @classmethod
    def open_default(cls, app_dir: Optional[str] = None) -> "BambooDeploymentSaves":
        if not app_dir:
            app_dir = click.get_app_dir("bamboo")
        return cls(Path(app_dir) / "deployments")

    def create_data_directory(self) -> None:
        if not self.datadir.exists():
            self.datadir.mkdir(parents=True, exist_ok=True)

    def get_deployment_directory(self, name: str) -> Path:
        deployment_dir = self.datadir / name
        if not deployment_dir.exists():
            deployment_dir.mkdir(parents=True, exist_ok=True)
        return deployment_dir

    def load(self, name: str) -> Optional[Deployment]:
        deployment_dir = self.get_deployment_directory(name)
        snapshot_path = deployment_dir / "snapshot.json"
        if not snapshot_path.exists():
            return None
        return self.load_snapshot(snapshot_path)

    @staticmethod
    def load_snapshot(snapshot_path: Path) -> Deployment:
        """Load deployment snapshot.
        This method will raise Error if snapshot has problem.
        Return `None` if snapshot is not found.
        """
        from json import load
        from validobj import parse_input
        import validobj

        with snapshot_path.open("r") as f:
            snapshot = load(f)
            obj = parse_input(snapshot, Deployment)
            return obj

    def save(self, name: str, deployment: Deployment) -> None:
        deployment_dir = self.get_deployment_directory(name)
        snapshot_path = deployment_dir / "snapshot.json"
        self.save_snapshot(snapshot_path, deployment)

    @staticmethod
    def save_snapshot(snapshot_path: Path, deployment: Deployment) -> None:
        from dataclasses import asdict
        from json import dump

        snapshot = asdict(deployment)
        with snapshot_path.open("w+") as f:
            dump(snapshot, f)

    def load_or_create(self, name: str) -> Deployment:
        deployment = self.load(name)
        if not deployment:
            return Deployment(name, "", list())
        return deployment

    def list(self) -> List[Path]:
        return list(self.datadir.glob("*"))

    def remove(self, name: str) -> None:
        from shutil import rmtree

        path = self.datadir / name
        if path.exists():
            rmtree(path, True)


def get_driver_from_option(
    name: str, driver_path: Optional[str], dryrun: bool
) -> BambooDriverProtocol:
    if name == "podman":
        from .drivers.podman import PodmanDriver

        return PodmanDriver(driver_path, dryrun=dryrun)
    else:
        raise RuntimeError(
            "this function only recvice acceptable driver name: {}".format(
                ", ".join(["podman"])
            )
        )


def get_config_path(config_path: Union[str, PathLike]) -> Path:
    config_path = Path(config_path).absolute()
    if config_path.is_dir():
        config_path = config_path / "_.yaml"
    return config_path


def get_executor_and_driver_from_click_ctx(
    ctx: Any,
) -> Tuple[BambooExecutor, BambooDriverProtocol]:
    driver = get_driver_from_option(
        ctx.obj["driver"], ctx.obj["driver_path"], dryrun=ctx.obj["dryrun"]
    )
    executor = BambooExecutor(driver, bamboo_data_dir=ctx.obj["bamboo_dir"])
    return executor, driver


@group()
@click.version_option(__version__)
@option(
    "--bamboo-dir",
    "bamboo_dir",
    type=click.Path(dir_okay=True),
    required=False,
    default=click.get_app_dir("bamboo"),
    show_default=True,
    help="set bamboo application directory",
)
@option(
    "--driver",
    "driver",
    type=click.Choice(["podman"]),
    default="podman",
    help="the driver to manage namespaces",
)
@option(
    "--driver-path",
    "driver_path",
    type=click.Path(exists=True, file_okay=True),
    required=False,
    help="the driver binary path",
)
@option(
    "--dryrun",
    "dryrun",
    type=bool,
    is_flag=True,
    flag_value=True,
    default=False,
    help="tell driver does not perform any actual changes, but print commands and return fake data",
)
@click.pass_context
def main(ctx, bamboo_dir, driver, driver_path, dryrun):
    """
    bamboo4py  Copyright (C) 2021  The PyBamboo Contributors

    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it under certain conditions.
    """
    ctx.ensure_object(dict)
    ctx.obj["bamboo_dir"] = bamboo_dir
    ctx.obj["driver"] = driver
    ctx.obj["driver_path"] = driver_path
    ctx.obj["dryrun"] = dryrun


@main.command()
@argument("deployment_name", type=str)
@argument("config_path", type=click.Path(exists=True), default=".")
@option("--yes", "-y", "yes", is_flag=True, flag_value=True, default=False)
@click.pass_context
def deploy(ctx, deployment_name, config_path, yes):
    "setup containers and save deployment snapshot"
    config_path = get_config_path(config_path)
    from .deployment import BambooExecutor

    executor, driver = get_executor_and_driver_from_click_ctx(ctx)
    saves = BambooDeploymentSaves.open_default(ctx.obj["bamboo_dir"])
    old_deployment = saves.load_or_create(deployment_name)
    conf = BambooConfiguration.open_ship_file(old_deployment, config_path)
    if not conf.ship:
        raise RuntimeError("bad configuration: {}".format(config_path))
    echo("Calculating dependencies...")
    changes = executor.local_mode_update_deployment(old_deployment, conf.ship)
    changes_number = len(changes)
    echo("Changes check.")
    echo()
    echo(changes.self_describe())
    echo()
    echo("Total: {} Changes.".format(changes_number))
    if not yes:
        while True:
            input: str = click.prompt(
                "Apply these changes? [y/N] ", default="N", type=str
            ).lower()
            if input == "y":
                break
            elif input == "n":
                raise click.Abort()
    if changes_number > 0:
        if isinstance(driver, PodmanDriver):
            # driver.write_to_stdstream = True # That may be not a good idea
            pass
        try:
            changes.do_action(driver)
            if not ctx.obj["dryrun"]:
                saves.save(deployment_name, old_deployment)
        except RuntimeError as e:
            echo(str(e), err=True)
            sys.exit(125)


@main.command()
@argument("deployment_name", type=str)
@click.pass_context
def kill(ctx, deployment_name):
    "(local mode) kill deployment."
    saves = BambooDeploymentSaves.open_default(ctx.obj["bamboo_dir"])
    executor, driver = get_executor_and_driver_from_click_ctx(ctx)
    deployment = saves.load(deployment_name)
    if not deployment:
        echo("Error: no such deployment", err=True)
        sys.exit(64)
    changes = executor.local_mode_start_deployment(deployment)
    executor.execute_changes(changes)


@main.command()
@argument("deployment_name", type=str)
@click.pass_context
def start(ctx, deployment_name):
    "(local mode) start containers in a deployment"
    saves = BambooDeploymentSaves.open_default(ctx.obj["bamboo_dir"])
    executor, driver = get_executor_and_driver_from_click_ctx(ctx)
    deployment = saves.load(deployment_name)
    if not deployment:
        echo("Error: no such deployment", err=True)
        sys.exit(64)
    changes = executor.local_mode_start_deployment(deployment)
    executor.execute_changes(changes)


@main.command()
@argument("deployment_name", type=str)
@click.pass_context
def down(ctx, deployment_name):
    "(local mode) stop containers in a deployment"
    saves = BambooDeploymentSaves.open_default(ctx.obj["bamboo_dir"])
    executor, driver = get_executor_and_driver_from_click_ctx(ctx)
    deployment = saves.load(deployment_name)
    if not deployment:
        echo("Error: no such deployment", err=True)
        sys.exit(64)
    changes = executor.local_mode_down_deployment(deployment)
    executor.execute_changes(changes)


@main.command()
def rm(ctx, deployment_name):
    "remove local data and containers for a deployment."
    pass


@main.command()
def export(ctx, deployment_name):
    "export local data from a deployment"
    pass


@main.command()
@argument("deployment_name", type=str)
@argument("config_path", type=click.Path(exists=True), default=".")
@option(
    "--save-deployment",
    "save_deployment",
    is_flag=True,
    flag_value=True,
    type=bool,
    help="save deployment without making actual changes (don't use this unless you know want you are doing)",
)
@click.pass_context
def show_changes(ctx, deployment_name, config_path, save_deployment):
    config_path = get_config_path(config_path)

    bamboo_dir = ctx.obj["bamboo_dir"]
    executor = get_executor_and_driver_from_click_ctx(ctx)
    deployment_saves = BambooDeploymentSaves.open_default(bamboo_dir)
    old_deployment = deployment_saves.load_or_create(deployment_name)
    conf = BambooConfiguration.open_ship_file(old_deployment, config_path)
    if not conf.ship:
        raise RuntimeError("bad configuration: {}".format(config_path))
    changeset = executor.local_mode_update_deployment(old_deployment, conf.ship)
    result = changeset.self_describe()
    echo(result, nl=True if len(result) > 0 else False)
    if save_deployment:
        deployment_saves.save(deployment_name, old_deployment)


def generate_ship_summary(ship: Ship):
    KEY0COLOR = "red"
    KEY1COLOR = "blue"
    INDENT = " " * 4
    assert ship
    yield from [style("SHIP", fg=KEY0COLOR), " ", ship.name, "\n"]
    yield from [INDENT, style("VERSION", fg=KEY1COLOR), " ", ship.version, "\n"]
    yield from [INDENT, style("ID", fg=KEY1COLOR), " ", ship.id, "\n"]
    yield from [
        INDENT,
        style("SERVICES", fg=KEY1COLOR),
        " ",
        ", ".join(ship.services.keys()),
        "\n",
    ]
    yield from [
        INDENT,
        style("EXPOSES", fg=KEY1COLOR),
        " ",
        ", ".join(map(lambda x: "{}({})".format(x.name, x.port), ship.exposes)),
        "\n",
    ]
    for serv_id in ship.services:
        serv = ship.services[serv_id]
        yield from [style("SERVICE", fg=KEY0COLOR), " ", serv_id, "\n"]
        yield from [
            INDENT,
            style("DESCRIPTION NAME", fg=KEY1COLOR),
            " ",
            serv.name,
            "\n",
        ]
        yield from [INDENT, style("VERSION", fg=KEY1COLOR), " ", serv.version, "\n"]
        yield from [
            INDENT,
            style("CONTAINERS", fg=KEY1COLOR),
            " ",
            ", ".join(map(str, serv.containers)),
            "\n",
        ]


@main.command()
@argument("deployment_name", type=str)
@argument("config_path", type=click.Path(exists=True), default=".")
@click.pass_context
def config_summary(ctx, deployment_name: str, config_path: str):
    confpath = get_config_path(config_path)
    saves = BambooDeploymentSaves(Path(ctx.obj["bamboo_dir"]))
    deployment = saves.load_or_create(deployment_name)
    conf = BambooConfiguration.open_ship_file(deployment, confpath)
    assert conf.ship
    echo("".join(generate_ship_summary(conf.ship)))


@main.group()
def deployment():
    """tools to manage local deployment *data*, don't use these command unless you know what you are doing.
    If you are looking for deploy your configuration, please turn to command `deploy` which is in the same level to this command group.
    """
    pass


@deployment.command("list")
@option("--full-path", "full_path", flag_value=True, is_flag=True)
@option("--details", "details", flag_value=True, is_flag=True)
@click.pass_context
def deployment_list(ctx, full_path, details):
    from io import StringIO

    bamboo_dir: str = ctx.obj["bamboo_dir"]
    saves = BambooDeploymentSaves.open_default(bamboo_dir)
    lines: List[str] = []
    for name in saves.list():
        line_buf = StringIO()
        if full_path:
            line_buf.write(str(name))
        else:
            line_buf.write(name.name)
        line_buf.write(" ")
        if details:
            try:
                deployment = saves.load(name)
                if not deployment:
                    line_buf.write("snapshot: {}, ".format("notfound"))
                else:
                    line_buf.write("snapshot: ok, ")
                    line_buf.write("ships: {}, ".format(len(deployment.ships)))
            except:
                line_buf.write("snapshot: {}, ".format("error"))
        lines.append(line_buf.getvalue().strip())
    echo("\n".join(lines), nl=True if lines else False)


@deployment.command("show-snapshot")
@argument("deployment_name", type=str, required=True)
@click.pass_context
def deployment_show_snapshot(ctx, deployment_name):
    "show snapshot of a deployment"
    from json import dumps
    from dataclasses import asdict

    bamboo_dir = ctx.obj["bamboo_dir"]
    saves = BambooDeploymentSaves.open_default(bamboo_dir)
    deployment = saves.load(deployment_name)
    if deployment:
        s = dumps(asdict(deployment), indent=2)
        echo(s)
    else:
        echo("Error: no such deployment")
        sys.exit(64)


@deployment.command("rm")
@argument("deployment_name", type=str, required=True)
@click.confirmation_option(
    "--yes",
    "-y",
    prompt="Are you sure remove the deployment? This operation can't be undone!",
)
@click.pass_context
def deployment_rm(ctx, deployment_name):
    "remove local deployment data."
    bamboo_dir = ctx.obj["bamboo_dir"]
    saves = BambooDeploymentSaves.open_default(bamboo_dir)
    saves.remove(deployment_name)


@main.group()
def itself():
    pass


@itself.command("directory")
@click.pass_context
def itself_directory(ctx):
    "print current application directory"
    echo(ctx.obj["bamboo_dir"])


@itself.command("server")
@click.pass_context
def itself_server(ctx):  # TODO (rubicon): complete daemon-managed mode
    pass


if __name__ == "__main__":
    main()
