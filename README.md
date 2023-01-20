# Self configuring OTBR application

## On device setup

Add `ip6table_filter` to `/etc/modules`.

## Fill network information

1. Fill public information to `config.yaml`
2. Create a `secrets.yaml` file:

```
network_key: 00112233445566778899aabbccddeeff
passphrase: j01Nme
```

## Run

```bash
DOCKER_HOST=ssh://otbr1.local docker compose up
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
docker build -f etc/docker/Dockerfile --build-arg NAT64=0 --build-arg DNS64=0 --build-arg MDNS=avahi --build-arg OTBR_OPTIONS="-DOTBR_DBUS=OFF" -t francoisgervais/${PWD##*/} .
```
