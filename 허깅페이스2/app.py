import torch 
import re 
import gradio as gr
from transformers import AutoTokenizer, ViTFeatureExtractor, VisionEncoderDecoderModel 

device='cpu'
#https://huggingface.co/nlpconnect/vit-gpt2-image-captioning 사전학습모델
encoder_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
decoder_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
model_checkpoint = "nlpconnect/vit-gpt2-image-captioning"
feature_extractor = ViTFeatureExtractor.from_pretrained(encoder_checkpoint)
tokenizer = AutoTokenizer.from_pretrained(decoder_checkpoint)
model = VisionEncoderDecoderModel.from_pretrained(model_checkpoint).to(device)


def predict(image,max_length=64, num_beams=4):
  image = image.convert('RGB')
  image = feature_extractor(image, return_tensors="pt").pixel_values.to(device)
  clean_text = lambda x: x.replace('<|endoftext|>','').split('\n')[0]
  caption_ids = model.generate(image, max_length = max_length)[0]
  caption_text = clean_text(tokenizer.decode(caption_ids))
  return caption_text 



input = gr.inputs.Image(label="Upload your Image", type = 'pil', optional=True)
output = gr.outputs.Textbox(type="text",label="Captions")

title = "Image Captioning "

interface = gr.Interface(
        fn=predict,
        inputs = input,
        theme="grass",
        outputs=output,
        title=title,
    )
interface.launch(debug=True)