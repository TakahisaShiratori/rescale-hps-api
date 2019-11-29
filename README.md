# rescale-hps-api
## Usage
Clone this repository, and build the image
```bash
$ git clone git@github.com:TakahisaShiratori/rescale-hps-api.git
$ cd rescale-hps-api/
$ docker build -t rescale-hps-api .
```

RESCALE_API_KEY is required environmental variable to run the built image.
```bash
$ docker run \
  -e RESCALE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  rescale-hps-api
```

Use RESCALE_PLATFORM to specify platform. For example, Japan platform can be used by
```bash
$ docker run \
  -e RESCALE_PLATFORM=platform.rescale.jp \
  -e RESCALE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  rescale-hps-api
```

By default, RESCALE_PLATFORM is platform.rescale.com
