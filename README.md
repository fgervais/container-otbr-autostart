# Self configuring OTBR application

## On device setup

1. Add `ip6table_filter` to `/etc/modules`.

2. ```bash
sudo apt install avahi-daemon
```

## Fill network information

1. Fill public information to `config.yaml`
2. Create a `secrets.yaml` file:

```
network_key: <networkkey>
passphrase: <passphrase>
```

## Run

```bash
DOCKER_HOST=ssh://otbr1.local docker compose up
```

### Change the backbone interface

```bash
DOCKER_HOST=ssh://otbr1.local BACKBONE_INTERFACE=eth0 docker compose up
```

## Note on otbr config

OTBR will store the network config in a `.data` file inside
`OPENTHREAD_CONFIG_POSIX_SETTINGS_PATH` folder which defaults to `/var/lib/thread/`.

If you shutdown the containers and `up` them again, the `setup` container won't
need to initiate the network again as otbr will feed from it's internal config.

If you which to start from scratch, you may use the following:

```bash
DOCKER_HOST=ssh://otbr1.local docker compose down
```

## Build the container image

```bash
git clone --recursive https://github.com/openthread/ot-br-posix.git

cd ot-br-posix
docker build -f etc/docker/Dockerfile --build-arg NAT64=0 --build-arg DNS64=0 --build-arg MDNS=avahi --build-arg OTBR_OPTIONS="-DOTBR_DBUS=OFF -DOTBR_TREL=ON" -t francoisgervais/${PWD##*/} .
```

### Other architectures

```bash
docker buildx build --platform linux/arm64 -f etc/docker/Dockerfile --build-arg NAT64=0 --build-arg DNS64=0 --build-arg MDNS=avahi --build-arg OTBR_OPTIONS="-DOTBR_DBUS=OFF -DOTBR_TREL=ON" -t francoisgervais/${PWD##*/} --load .
```

### Multi-arch

```bash
docker buildx build --platform linux/amd64,linux/arm64 -f etc/docker/Dockerfile --build-arg NAT64=0 --build-arg DNS64=0 --build-arg MDNS=avahi --build-arg OTBR_OPTIONS="-DOTBR_DBUS=OFF -DOTBR_TREL=ON" -t francoisgervais/${PWD##*/}:ipv6-only --push .
```
