import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class PerryConfig(BaseModel):
    # --- naming
    project_id: str = "new-project"

    # --- networking
    bind_address: str = "localhost"

    # --- ssh
    key_path: Optional[str] = None

    # -- labeling
    env_label: Optional[str] = None

    env_label_suffix: str = "s"
    separator: str = "-"

    # --- paths

    instance_config_path: Optional[str] = "./perry_instance_config.json"
    instance_pem_path: Optional[str] = None

    # --- unison properties
    ignore_dirs: list[str] = []
    local_port_forwards: dict[str, dict[str, str]] = {}
    remote_port_forwards: dict[str, dict[str, str]] = {}
    sync_paths: list[Path]

    # --- instance properties
    instance_username: str = "ubuntu"
    bootstrap_command: str = r"""
        set -x
        && sudo sysctl -w net.core.somaxconn=4096
        && sudo echo GRUB_CMDLINE_LINUX=\\"\"cdgroup_enable=memory swapaccount=1\\"\" | sudo tee -a /etc/default/grub.d/50-cloudimg-settings.cfg
        && sudo update-grub
        && sudo rm /var/lib/dpkg/lock
        && sudo dpkg --configure -a
        && sudo apt-get -y update
        && sudo apt-get -y install docker.io || true
        && sudo usermod -aG docker ubuntu  || true
        && sudo systemctl daemon-reload || true
        && sudo systemctl restart docker.service || true
        && sudo systemctl enable docker.service || true
        && "sudo sed -i -e '/GatewayPorts/ s/^.*$/GatewayPorts yes/' '/etc/ssh/sshd_config'"
        && sudo service sshd restart
        && wget -qO- https://github.com/bcpierce00/unison/releases/download/v2.52.1/unison-v2.52.1+ocaml-4.01.0+x86_64.linux.tar.gz | tar -xvz
        && sudo mv bin/* /usr/local/bin/
        && sudo reboot
    """

    @property
    def expanded_sync_dir(self) -> str:
        return os.path.expanduser("~")

    @property
    def expanded_sync_paths(self) -> list[str]:
        return [
            str(Path(os.path.expanduser(f)).absolute()).split(
                self.expanded_sync_dir + os.sep
            )[1]
            for f in self.sync_paths
        ]
