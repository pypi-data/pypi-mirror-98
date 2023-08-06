from io import BytesIO, StringIO
from pathlib import Path
import sys
import click
from typing import Any, Dict, IO, List, NoReturn, Optional, Sequence
from .protocol import (
    BambooDriverProtocol,
    ContainerDescription,
    ContainerMount,
    MountTypes,
    PodDescription,
)
import subprocess
from .net import AnyIPNetwork, asipaddress, asipnetwork
import json


def completed_process_failed(process: subprocess.CompletedProcess) -> NoReturn:
    raise RuntimeError(
        "{} failed with return code {}".format(
            " ".join(process.args), process.returncode
        )
    )


class PodmanDriver(BambooDriverProtocol):
    def __init__(
        self,
        podman_bin_path: Optional[str],
        namespace: Optional[str] = "bamboo",
        write_to_stdstream: Optional[bool] = None,
        dryrun: bool = False,
    ) -> None:
        self.podman_bin_path = podman_bin_path if podman_bin_path else "podman"
        self.namespace = namespace
        self.write_to_stdstream = (
            write_to_stdstream if write_to_stdstream != None else False
        )
        self.dryrun = dryrun

    def set_dryrun(self, enabled: bool = True) -> None:
        self.dryrun = enabled

    def run_podman(self, *args, **kwargs) -> subprocess.CompletedProcess:
        write_to_stdstream = kwargs.get("write_std", self.write_to_stdstream)
        args = (
            self.podman_bin_path,
            *(
                ("--namespace={}".format(self.namespace),)
                if self.namespace
                else tuple()
            ),
            *args,
        )
        if self.dryrun:
            from click import echo

            cmd = " ".join(args)
            echo(cmd)
            fake_stdout = b""
            fake_stderr = b""
            if "-f json" in cmd:
                fake_stdout = b"[]"
                fake_stderr = b"[]"
            return subprocess.CompletedProcess(args, 0, fake_stdout, fake_stderr)
        p = subprocess.Popen(
            args,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        stdout = BytesIO()
        stderr = BytesIO()
        assert p.stdout and p.stderr
        while p.poll() == None:
            while outc := p.stdout.read(1):
                stdout.write(outc)
                if write_to_stdstream:
                    raw_stdout = click.get_binary_stream("stdout")
                    raw_stdout.write(outc)
            while errc := p.stderr.read(1):
                stderr.write(errc)
                if write_to_stdstream:
                    raw_stderr = click.get_binary_stream("stderr")
                    raw_stderr.write(errc)
        return subprocess.CompletedProcess(
            args, p.returncode, stdout.getvalue(), stderr.getvalue()
        )

    def create_network(
        self, name: str, subnet: AnyIPNetwork, ip_range: AnyIPNetwork
    ) -> None:
        command = [
            "network",
            "create",
            "--subnet",
            str(asipnetwork(subnet)),
            "--ip-range",
            str(asipnetwork(ip_range)),
            name,
        ]
        p = self.run_podman(*command)
        if p.returncode != 0:
            completed_process_failed(p)

    def remove_network(self, name: str, force: Optional[bool] = None) -> None:
        command = ["network", "rm", name]
        if force:
            command.append("--force")
        p = self.run_podman(*command)
        if p.returncode != 0:
            completed_process_failed(p)

    def _list_network_names(self) -> List[str]:
        p = self.run_podman("network", "ls", "-f", "json")
        if p.returncode != 0:
            completed_process_failed(p)
        network_dumps: List[Dict[str, Any]] = json.loads(p.stdout)
        if not network_dumps:
            return []
        return list(map(lambda x: x["Name"], network_dumps))

    def exists_network(self, name: str) -> bool:
        return name in self._list_network_names()

    @classmethod
    def generate_volume_option_value(cls, mount: ContainerMount) -> str:
        """Create the value for option `--mount`."""
        result_buffer = StringIO()
        result_buffer.write("type={},".format(mount.type.value))
        if mount.src:
            result_buffer.write("src={},".format(mount.src))
        result_buffer.write("dst={},".format(mount.dst))
        if (
            mount.type == MountTypes.VOLUME
            or mount.type == MountTypes.BIND
            or mount.type == MountTypes.TMPFS
        ) and (not mount.writable):
            result_buffer.write("ro=true,")
        elif (mount.type == MountTypes.IMAGE) and mount.writable:
            result_buffer.write("rw=true,")
        return result_buffer.getvalue()

    def create_container(self, name: str, description: ContainerDescription) -> None:
        assert not description.ip6
        command = ["container", "create", "--name", name]
        if description.network_name:
            command.extend(("--network", description.network_name))
        if description.ip:
            addr = asipaddress(description.ip)
            command.extend(("--ip", str(addr)))
        for mount in description.mounts:
            if mount.type == MountTypes.BIND and mount.src:
                src_path = Path(mount.src)
                if not src_path.exists():
                    src_path.mkdir(parents=True, exist_ok=True)
            command.extend(("--mount", self.generate_volume_option_value(mount)))
        if description.network_alias:
            command.extend(("--network-alias", description.network_alias))
        command.append(description.image)
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def remove_container(self, name: str) -> None:
        command = ["container", "rm", name]
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def kill_container(self, name: str) -> None:
        command = ["container", "kill", name]
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def start_container(self, name: str) -> None:
        command = ["container", "start", name]
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def pause_container(self, name: str) -> None:
        command = ["container", "pause", name]
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def unpause_container(self, name: str) -> None:
        command = ["container", "unpause", name]
        process = self.run_podman(*command)
        if process.returncode != 0:
            completed_process_failed(process)

    def exists_container(self, name: str) -> bool:
        p = self.run_podman("container", "exists", name)
        if p.returncode == 0:
            return True
        elif p.returncode == 1:
            return False
        else:
            completed_process_failed(p)

    def exists_image(self, name: str) -> bool:
        p = self.run_podman("image", "exists", name)
        if (p.returncode > 1) or (p.returncode < 0):
            completed_process_failed(p)
        return True if p.returncode == 0 else False

    def pull_image(self, name: str) -> None:
        p = self.run_podman("pull", name)
        if p.returncode != 0:
            completed_process_failed(p)

    def connect_network(
        self, network_name: str, container_name: str, alias: Optional[str] = None
    ) -> None:
        options = ["network", "connect", network_name, container_name]
        if alias:
            options.extend(("--alias", alias))
        p = self.run_podman(*options)
        if p.returncode != 0:
            completed_process_failed(p)

    def disconnect_network(self, network_name: str, container_name: str) -> None:
        options = ["network", "disconnect", network_name, container_name]
        p = self.run_podman(*options)
        if p.returncode != 0:
            completed_process_failed(p)

    def create_pod(self, description: PodDescription) -> None:
        options = ["pod", "create", "--name", description.name]
        if description.network_name:
            options.extend(("--network", description.network_name))
        if description.network_alias:
            options.extend(("--network-alias", description.network_alias))
        p = self.run_podman(*options)
        if p.returncode != 0:
            completed_process_failed(p)

    def remove_pod(self, name: str) -> None:
        options = ["pod", "rm", name]
        p = self.run_podman(*options)
        if p.returncode != 0:
            completed_process_failed(p)

    def exists_pod(self, name: str) -> bool:
        options = ["pod", "exists", name]
        p = self.run_podman(*options)
        if p.returncode == 0:
            return True
        elif p.returncode == 1:
            return False
        else:
            completed_process_failed(p)

    def stop_container(self, name: str) -> None:
        options = ["container", "stop", name]
        p = self.run_podman(*options)
        if p.returncode != 0:
            completed_process_failed(p)
