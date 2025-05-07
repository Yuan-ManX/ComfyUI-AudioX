# ComfyUI-AudioX

Make AudioX avialbe in ComfyUI.

[AudioX](https://github.com/ZeyueT/AudioX): Diffusion Transformer for Anything-to-Audio Generation.



## Installation

1. Make sure you have ComfyUI installed

2. Clone this repository into your ComfyUI's custom_nodes directory:
```
cd ComfyUI/custom_nodes
git clone https://github.com/Yuan-ManX/ComfyUI-AudioX.git
```

3. Install dependencies:
```
cd ComfyUI-AudioX
pip install -r requirements.txt
```


## Model

### Pretrained Checkpoints

Download the pretrained model from 🤗 [AudioX on Hugging Face](https://huggingface.co/HKUSTAudio/AudioX):

```bash
mkdir -p model
wget https://huggingface.co/HKUSTAudio/AudioX/resolve/main/model.ckpt -O model/model.ckpt
wget https://huggingface.co/HKUSTAudio/AudioX/resolve/main/config.json -O model/config.json
```

