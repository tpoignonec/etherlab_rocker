# etherlab_rocker

A rocker extension that installs the EtherCAT Master IgH (EtherLab) userspace library from source inside a Docker image and forwards the master device and configuration into the container.

The extension clones a chosen tag or branch of EtherLab EtherCAT master from
`https://gitlab.com/etherlab.org/ethercat.git`, builds it with
`--disable-kernel` (userspace-only), and installs it under
`/usr/local/etherlab`.

In addition, the `/dev/EtherCAT<idx>` device is exposed to the container via `--device` and the EtherLab config`/etc/sysconfig/ethercat` is bind-mounted (read-only) into the container automatically.

**Missing features:**
- Multiple EtherCAT devices (multi-master setup);
- EtherLab repos URL as an argument;
- Master launch at startup, i.e., run `sudo /etc/init.d/ethercat start` in host.

## Prerequisites: kernel module on the host

Because this extension builds EtherLab with `--disable-kernel`, **no kernel module is compiled inside the container**. The `ec_master` kernel module must be built and loaded on the **host** machine before starting the container. The userspace library communicates with the master through the exposed `/dev/EtherCAT*` device.

## Installation

### From PyPI

```bash
pip install etherlab-rocker
```

### From source (development)

```bash
git clone https://github.com/tpoignonec/etherlab_rocker.git

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
| `--etherlab` | — | Enable the extension (**required**) |
| `--etherlab-version` | `stable-1.5` | Any git tag or branch of the EtherLab repository (e.g. `stable-1.5`, `1.6.1`, etc.). Use `none` to skip installation and only forward devices and config |
| `--ethercat-master-idx` | `0` | Index of the `/dev/EtherCAT<idx>` device to forward into the container. Set to `-1` to disable device forwarding |

### Examples

**Basic — install EtherLab `stable-1.5` (default) and open a shell:**
```bash
rocker --etherlab ubuntu:24.04 bash
```

**Use a specific tag or branch:**
```bash
rocker --etherlab --etherlab-version stable-1.6 ubuntu:24.04 bash
```

**Explicit master device index:**
```bash
rocker --etherlab --ethercat-master-idx 1 ubuntu:24.04 bash
```

Note that no value is the same as `0`.

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

