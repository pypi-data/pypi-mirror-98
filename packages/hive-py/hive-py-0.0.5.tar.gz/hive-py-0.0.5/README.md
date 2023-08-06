Hive is designed to simplify distributed systems that communicate over messages published to topics. It is designed for
robotics/cloud systems, to be simple to use and flexible. The basic worker structure is modelled after ROS.

Example of connecting to MQTT running locally:

```python
from hive.mqtt import HiveMqtt
from hive import HiveWorker



bee = HiveWorker(
    host='localhost'
)

publisher = bee.publisher("foo", dict)
bee.subscribe("foo", dict, lambda msg: print(msg))

publisher.publish({
    "id": "test",
    "x": 1.5,
    "list_foo": [1, 2, 3]
})

bee.spin()
```
