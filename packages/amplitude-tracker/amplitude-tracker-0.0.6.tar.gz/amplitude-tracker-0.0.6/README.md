Amplitude Tracker
==============

Amplitude Tracker library lets you record analytics data from your Python code to [Amplitude](https://amplitude.com)


## Getting Started

Install `amplitude-tracker` using pip:

```
pip install amplitude-tracker
```

Inside your app, you’ll want to *set your* `write_key` before making any analytics calls:

```python
import amplitude_tracker as amplitude

amplitude.write_key = 'xxxxxxxxxxxxxxx'
```
*Note:* If you need to send data to multiple Segment sources, you can initialize a new Client for each write_key.

## Development Settings

The default initialization settings are production-ready and queue messages to be processed by a background thread.

In development you might want to enable some settings to make it easier to spot problems. Enabling amplitude.debug will log debugging info to the Python logger. You can also add an on_error handler to specifically print out the response you’re seeing from the Amplitude's API.



```python
def on_error(error, items):
    print("An error occurred:", error)


analytics.debug = True
analytics.on_error = on_error
```


## Track

`track` lets you record the actions your users perform. Every action triggers what we call an “event”, which can also have associated properties.

```python
import amplitude_tracker as amplitude
amplitude.write_key = 'xxxxxxxxxxxxxxx'

amplitude.track(
    user_id="xxx",
    event_type="xxx",
    user_properties={"trait": "xxx"},
    event_properties={"attribute": "xxx"})
```

## Batching

This library is built to support high performance environments. That means it is safe to use amplitude-tracker on a web server that’s serving hundreds of requests per second.

Every call `track` method *does not* result in an HTTP request, but is queued in memory instead. Messages are flushed in batch in the background, which allows for much faster operation.

By default, this library will flush:

* every `100` messages (control with `upload_size`)
* if `0.5` seconds has passed since the last flush (control with `upload_interval`)

There is a maximum of `500KB` per batch request and `32KB` per call.
