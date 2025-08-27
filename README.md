# WebRTC Audio Processing For Python

Build webrtc audio processing module and use it in python.

## Setup

```bash
meson setup . build -Dprefix=$PWD/install
ninja -C build
ninja -C build install

cd python
LIBRARY_PATH=../install/lib/x86_64-linux-gnu/:$LIBRARY_PATH pip install -e .
```

## References

1. [webrtc-audio-processing-python](https://github.com/zhoubin-me/webrtc-audio-processing-python)
2. [webrtc-audio-processing](https://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing)
