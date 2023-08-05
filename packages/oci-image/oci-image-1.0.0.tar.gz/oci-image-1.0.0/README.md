# OCI Image Resource helper

This is a helper for working with OCI image resources in the charm operator
framework.


## Usage

Add this to your charm by including `oci-image` in your `requirements.txt` file.

The `OCIImageResource` class will wrap the framework resource for the given
resource name, and calling `fetch` on it will either return the image info
or raise an `OCIImageResourceError` if it can't fetch or parse the image
info. The exception will have a `status` attribute you can use directly,
or a `status_message` attribute if you just want that.

Example usage:

```python
from ops.charm import CharmBase
from ops.main import main
from oci_image import OCIImageResource, OCIImageResourceError


class MyCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = OCIImageResource(self, 'resource-name')
        self.framework.observe(self.on.start, self._on_start)

    def _on_start(self, event):
        try:
            image_info = self.image.fetch()
        except OCIImageResourceError as e:
            self.model.unit.status = e.status
            event.defer()
            return

        self.model.pod.set_spec({'containers': [{
            'name': 'my-charm',
            'imageDetails': image_info,
        }]})


if __name__ == "__main__":
    main(MyCharm)
```

## Developing

Tests can be run with [tox](https://tox.readthedocs.io/en/latest/).
