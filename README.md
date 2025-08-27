# WebRTC Audio Processing For Python

Build webrtc audio processing module and use it in python.

## Setup

```bash
meson . build -Dprefix=$PWD/install
ninja -C build
ninja -C build install

cd python
LIBRARY_PATH=../install/lib/x86_64-linux-gnu/:$LIBRARY_PATH pip install -e .
```
