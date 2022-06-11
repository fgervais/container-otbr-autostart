#

## Setup

Add `ip6table_filter` to `/etc/modules`.

## Run

```bash
DOCKER_HOST=ssh://otbr1.local docker-compose up
```

## Note on otbr config

OTBR will store the network config in a `.data` file inside
`OPENTHREAD_CONFIG_POSIX_SETTINGS_PATH` folder which defaults to `/var/lib/thread/`.

If you shutdown the containers and `up` them again, the `setup` container won't
need to initiate the network again as otbr will feed from it's internal config.

If you which to start from scratch, you may use the following:

```bash
DOCKER_HOST=ssh://otbr1.local docker-compose down
```
