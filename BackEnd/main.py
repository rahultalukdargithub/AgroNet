from fastapi import FastAPI, UploadFile, File, Form,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import tensorflow as tf
from model_config import gemini_safety_settings,generation_configuration,model,api_key
from prompt import prompt


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def combined_loss_corn(y_true, y_pred):
    loss1 = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    loss2 = tf.keras.losses.categorical_hinge(y_true, y_pred)
    return 1.0 * loss1 + 0.0 * loss2

custom_objects_corn = {'combined_loss': combined_loss_corn}


def combined_loss_potato(y_true, y_pred):
    loss1 = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    loss2 = tf.keras.losses.categorical_hinge(y_true, y_pred)
    return 0.7 * loss1 + 0.3 * loss2

custom_objects_potato = {'combined_loss': combined_loss_potato}

def combined_loss_wheat(y_true, y_pred):
    loss1 = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    loss2 = tf.keras.losses.categorical_hinge(y_true, y_pred)
    return 1.0 * loss1 + 0.0 * loss2

custom_objects_wheat = {'combined_loss': combined_loss_wheat}


def getGeminiResponse(name: str, d:str) -> str:
    generation_configuration = {
            "temperature": 0.75, 
            "top_p": 0.9, 
            "max_output_tokens": 2048 ,
            "top_k": 10
        }

    try:
        pr = prompt
        prompt_instruction = [
            f"{pr}\nFollowing the above provided rules and guidelines, generate the description and prevention for the crop named {name} with a disease of {d} . Make sure that its readable for the farmers. " 
        ]

        response = model.generate_content(
            contents=prompt_instruction, 
            generation_config=generation_configuration
        )
        # print(response.text)
        return response.text
    
    except Exception as exp:
        raise HTTPException(status_code=500, detail=f"Error occurred while generating the blog: {str(exp)}")
@app.post("/predict/")
async def predict(name: str= Form(...) ,file: UploadFile = File(...)):
    
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))

    if(name=="Corn"):
        try:
            img = Image.open(io.BytesIO(contents)).resize((224, 224))
        except Exception:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  
        img_array = img_array / 255.0  

        
        model = load_model(r'C:\Users\ASUS\Desktop\Final_Year_Project\models\Corn.h5', custom_objects=custom_objects_corn)
        predictions = model.predict(img_array)


        predicted_class = np.argmax(predictions[0])
        corn=['Common Rust', 'Gray Leaf Spot', 'Healthy Corn Leaf', 'Northern Leaf Blight']
        d=corn[int(predicted_class)]
        return {"predicted_class": d, "response":getGeminiResponse(name,d)}
    elif(name=="Potato"):
        try:
            img = Image.open(io.BytesIO(contents)).resize((224, 224))
        except Exception:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  
        img_array = img_array / 255.0  

        
        model = load_model(r'C:\Users\ASUS\Desktop\Final_Year_Project\models\Potato.h5', custom_objects=custom_objects_potato)
        predictions = model.predict(img_array)


        predicted_class = np.argmax(predictions[0])
        potato=['Early Blight', 'Healthy Potato Leaf', 'Late Blight']
        d=potato[int(predicted_class)]
        return {"predicted_class": d, "response":getGeminiResponse(name,d)}
    elif(name=="Wheat"):
        try:
            img = Image.open(io.BytesIO(contents)).resize((224, 224))
        except Exception:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  
        img_array = img_array / 255.0  

        
        model = load_model(r'C:\Users\ASUS\Desktop\Final_Year_Project\models\Wheat.h5', custom_objects=custom_objects_wheat)
        predictions = model.predict(img_array)


        predicted_class = np.argmax(predictions[0])
        wheat=['Brown Rust', 'Healthy Wheat Leaf', 'Yellow Rust']
        d=wheat[int(predicted_class)]
        # print(getGeminiResponse(name,d))
        return {"predicted_class": d, "response":getGeminiResponse(name,d)}
    else:
        try:
            img = Image.open(io.BytesIO(contents)).resize((240, 240))
        except Exception:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

        
        img_array = np.array(img)
        img_array = img_array[np.newaxis, :]   
 
        
        model = load_model(r'C:\Users\ASUS\Desktop\Final_Year_Project\models\Rice.h5')
        predictions = model.predict(img_array)


        predicted_class = np.argmax(predictions[0])
        rice=['Brown Spot', 'Healthy Rice Leaf', 'Rice Leaf Blast','Neck Blast']
        d=rice[int(predicted_class)]

        return {"predicted_class": d, "response":getGeminiResponse(name,d)}





