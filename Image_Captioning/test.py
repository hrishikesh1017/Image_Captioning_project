import streamlit as st
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image


model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

def predict_step(image_paths):
    images = []
    for image_path in image_paths:
        i_image = Image.open(image_path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")
        images.append(i_image)

    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds


def main():
    
        
    
    
    st.title("Image Captioning with Streamlit")
    
    


    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if image is not None:

        st.image(image, caption="Uploaded Image", use_column_width=True)
        if st.button("Generate Caption"):

            captions = predict_step([image])
            st.write("Predicted Caption:")
            st.write(f"<div style='text-align: center; font-weight: bold;'>{captions[0]}</div>", unsafe_allow_html=True)
            #st.write(captions[0])

if __name__ == "__main__":
    main()
