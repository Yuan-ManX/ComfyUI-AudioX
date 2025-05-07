from .nodes import LoadAudioXModel, LoadAudioXVideo, Prompt, LoadAudioXAudio, Condition, Generate, SaveAudioXAudio

NODE_CLASS_MAPPINGS = {
    "LoadAudioXModel": LoadAudioXModel,
    "LoadAudioXVideo": LoadAudioXVideo,
    "Prompt": Prompt,
    "LoadAudioXAudio": LoadAudioXAudio,
    "Condition": Condition,
    "Generate": Generate,
    "SaveAudioXAudio": SaveAudioXAudio,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadAudioXModel": "Load AudioX Model",
    "LoadAudioXVideo": "Load AudioX Video",
    "Prompt": "Prompt",
    "LoadAudioXAudio": "Load AudioX Audio",
    "Condition": "Condition",
    "Generate": "Generate",
    "SaveAudioXAudio": "Save AudioX Audio",
} 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
