import numpy as np
import ctypes


class WebRTCAPM:
    def __init__(self, webrtc_lib_path):
        ctypes.CDLL(webrtc_lib_path, ctypes.RTLD_GLOBAL)
        self.webrtc_apm = __import__("webrtc_audio_processing")

    def init_audio_processor(
        self,
        enable_aec=False,
        enable_agc=False,
        enable_ns=False,
        enable_hpf=False,
    ):
        builder = self.webrtc_apm.AudioProcessingBuilder()
        config = self.webrtc_apm.Config()
        if enable_aec:
            config.echo_canceller.enabled = True
            config.echo_canceller.mobile_mode = False
        if enable_agc:
            config.gain_controller1.enabled = True
            config.gain_controller1.mode = (
                self.webrtc_apm.GainController1Mode.ADAPTIVE_ANALOG
            )
            config.gain_controller2.enabled = True
        if enable_ns:
            config.noise_suppression.enabled = True
            config.noise_suppression.level = (
                self.webrtc_apm.NoiseSuppressionLevel.MODERATE
            )
        if enable_hpf:
            config.high_pass_filter.enabled = True
        builder.SetConfig(config)
        ap = builder.Create()
        self.ap = ap

    def set_stream_config(self, sample_rate: int, num_channels=1):
        self.stream_config = self.webrtc_apm.StreamConfig(sample_rate, num_channels)

    def process_farend_stream(self, farend_frame: np.ndarray):
        farend_frame = farend_frame.copy()
        self.ap.ProcessReverseStream(
            farend_frame, self.stream_config, self.stream_config, farend_frame
        )

    def process_mic_stream(self, mic_frame: np.ndarray):
        mic_frame = mic_frame.copy()
        self.ap.ProcessStream(
            mic_frame, self.stream_config, self.stream_config, mic_frame
        )
        return mic_frame
