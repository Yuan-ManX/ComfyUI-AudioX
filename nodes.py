import torch
import torchaudio
from einops import rearrange

from .src import get_pretrained_model
from .src.inference.generation import generate_diffusion_cond
from .src.data.utils import read_video
from .src.data.utils import load_and_process_audio


device = "cuda" if torch.cuda.is_available() else "cpu"


class LoadAudioXModel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_path": ("STRING", {"default": "HKUSTAudio/AudioX"}),
            }
        }

    RETURN_TYPES = ("MODEL", "SampleRate", "SampleSize", "FPS")
    RETURN_NAMES = ("model", "sample_rate", "sample_size", "target_fps")
    FUNCTION = "load_model"
    CATEGORY = "AudioX"

    def load_model(self, model_path):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, model_config = get_pretrained_model(model_path)
        sample_rate = model_config["sample_rate"]
        sample_size = model_config["sample_size"]
        target_fps = model_config["video_fps"]
        model = model.to(device)
        return (model, sample_rate, sample_size, target_fps)
    

class LoadAudioXVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {"default": "example/V2M_sample-1.mp4"}),
                "duration": ("INT", {"default": 10}),
                "target_fps": ("FPS",),
            }
        }

    RETURN_TYPES = ("TENSOR",)
    RETURN_NAMES = ("video_tensor",)
    FUNCTION = "load_video"
    CATEGORY = "AudioX"

    def load_video(self, video_path, duration, target_fps):
        video_tensor = read_video(video_path, seek_time=0, duration=duration, target_fps=target_fps)
        return (video_tensor.unsqueeze(0),)


class AudioXPrompt:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_prompt": ("STRING", {"default": "Generate music for the video"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_prompt",)
    FUNCTION = "load_text"
    CATEGORY = "AudioX"

    def load_text(self, text_prompt):
        return (text_prompt,)


class LoadAudioXAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio_path": ("STRING", {"default": None}),
                "sample_rate": ("SampleRate",),
                "seconds_start": ("INT", {"default": 0}),
                "seconds_total": ("INT", {"default": 10}),
            }
        }

    RETURN_TYPES = ("TENSOR",)
    RETURN_NAMES = ("audio_tensor",)
    FUNCTION = "load_audio"
    CATEGORY = "AudioX"

    def load_audio(self, audio_path, sample_rate, seconds_start, seconds_total):
        audio_path = None
        audio_tensor = load_and_process_audio(audio_path, sample_rate, seconds_start, seconds_total)
        return (audio_tensor.unsqueeze(0),)


class Condition:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_tensor": ("TENSOR",),
                "text_prompt": ("STRING",),
                "audio_tensor": ("TENSOR",),
                "seconds_start": ("INT", {"default": 0}),
                "seconds_total": ("INT", {"default": 10}),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "build"
    CATEGORY = "AudioX"

    def build(self, video_tensor, text_prompt, audio_tensor, seconds_start, seconds_total):
        conditioning = [{
            "video_prompt": [video_tensor],
            "text_prompt": text_prompt,
            "audio_prompt": audio_tensor,
            "seconds_start": seconds_start,
            "seconds_total": seconds_total
        }]
        return (conditioning,)


class Generate:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "conditioning": ("CONDITIONING",),
                "sample_size": ("SampleRate",),
                "steps": ("INT", {"default": 250}),
                "cfg_scale": ("FLOAT", {"default": 7.0}),
                "sigma_min": ("FLOAT", {"default": 0.3}),
                "sigma_max": ("FLOAT", {"default": 500.0}),
                "sampler_type": ("STRING", {"default": "dpmpp-3m-sde"}),
                "device": ("STRING", {"default": "cuda"}),
            }
        }

    RETURN_TYPES = ("AUDIO",)
    RETURN_NAMES = ("audio",)
    FUNCTION = "generate"
    CATEGORY = "AudioX"

    def generate(self, model, conditioning, sample_size, steps, cfg_scale, sigma_min, sigma_max, sampler_type, device):
        # device = "cuda" if torch.cuda.is_available() else "cpu"
        output = generate_diffusion_cond(
            model,
            steps=steps,
            cfg_scale=cfg_scale,
            conditioning=conditioning,
            sample_size=sample_size,
            sigma_min=sigma_min,
            sigma_max=sigma_max,
            sampler_type=sampler_type,
            device=device
        )

        # Rearrange audio batch to a single sequence
        audio = rearrange(output, "b d n -> d (b n)")
        return (audio,)


class SaveAudioXAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "sample_rate": ("SampleRate",),
                "output_wav": ("STRING", {"default": "output.wav"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "AudioX"

    def save(self, audio, sample_rate, output_wav):
        # Peak normalize, clip, convert to int16, and save to file
        audio = audio.to(torch.float32).div(torch.max(torch.abs(audio))).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
        torchaudio.save(output_wav, audio, sample_rate)
        return ()
