# etherlab_rocker

A rocker extension that installs the EtherCAT Master IgH (EtherLab) userspace library from source inside a Docker image and forwards the master device and configuration into the container.

The extension clones the `stable-1.5` branch from
`https://gitlab.com/etherlab.org/ethercat.git`, builds it with
`--disable-kernel` (userspace-only), and installs it under
`/usr/local/etherlab`.

## Prerequisites: kernel module on the host

Because this extension builds EtherLab with `--disable-kernel`, **no kernel module is compiled inside the container**. The `ec_master` kernel module must be built and loaded on the **host** machine before starting the container. The userspace library communicates with the master through the `/dev/EtherCAT*` device, which is exposed to the container via `--device`.

Install and load the kernel module on the host (one-time setup).

> **Note:** `/etc/sysconfig/ethercat` is bind-mounted read-only into the container automatically by this extension.

## Installation

### From PyPI

```bash
pip install etherlab-rocker
```

### From source (development)

```bash
git clone https://github.com/ICube-Robotics/etherlab_rocker.git

# Virtual environment
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate

# Install package
pip install -e ./etherlab_rocker
```

## Usage

```bash
sudo apt-get install python3-rocker

rocker --etherlab [--etherlab-version <version>] [--ethercat-master-idx <idx>] <base-image> [command]
```

### Arguments

| Argument | Default | Description |
|---|---|---|
| `--etherlab` | — | Enable the extension (required) |
| `--etherlab-version` | `stable-1.5` | EtherLab branch to build from. Use `none` to skip installation (only forward devices). Supported values: `stable-1.5`, `none` |
| `--ethercat-master-idx` | `0` | Index of the `/dev/EtherCAT<idx>` device to forward into the container. Set to `-1` to disable device forwarding |

`/etc/sysconfig/ethercat` is always bind-mounted read-only from the host.

### Examples

**Basic — install EtherLab and open a shell:**
```bash
rocker --etherlab ubuntu:24.04 bash
```

**Explicit master device index:**
```bash
rocker --etherlab --ethercat-master-idx 0 ubuntu:24.04 bash
```

**Skip installation (use a pre-built image that already has EtherLab):**
```bash
rocker --etherlab --etherlab-version none my-prebuilt-image bash
```

**Disable device forwarding (build/test only, no hardware):**
```bash
rocker --etherlab --ethercat-master-idx -1 ubuntu:24.04 bash
```

### Test the connection to the EtherCAT master

Once inside the container:

```bash
# List slaves on the bus
ethercat slaves

# Show master state
ethercat master
```

