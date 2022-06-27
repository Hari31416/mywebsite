from django.db import models
from PIL import Image
import tensorflow as tf
import os
import numpy as np


# Create your models here.
class ImageFile(models.Model):
    img_file = models.ImageField(upload_to="models")
    formats = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        # "gif": "GIF",
        # "bmp": "BMP",
    }
    class_names = [
        "apple_pie",
        "baby_back_ribs",
        "baklava",
        "beef_carpaccio",
        "beef_tartare",
        "beet_salad",
        "beignets",
        "bibimbap",
        "bread_pudding",
        "breakfast_burrito",
        "bruschetta",
        "caesar_salad",
        "cannoli",
        "caprese_salad",
        "carrot_cake",
        "ceviche",
        "cheesecake",
        "cheese_plate",
        "chicken_curry",
        "chicken_quesadilla",
        "chicken_wings",
        "chocolate_cake",
        "chocolate_mousse",
        "churros",
        "clam_chowder",
        "club_sandwich",
        "crab_cakes",
        "creme_brulee",
        "croque_madame",
        "cup_cakes",
        "deviled_eggs",
        "donuts",
        "dumplings",
        "edamame",
        "eggs_benedict",
        "escargots",
        "falafel",
        "filet_mignon",
        "fish_and_chips",
        "foie_gras",
        "french_fries",
        "french_onion_soup",
        "french_toast",
        "fried_calamari",
        "fried_rice",
        "frozen_yogurt",
        "garlic_bread",
        "gnocchi",
        "greek_salad",
        "grilled_cheese_sandwich",
        "grilled_salmon",
        "guacamole",
        "gyoza",
        "hamburger",
        "hot_and_sour_soup",
        "hot_dog",
        "huevos_rancheros",
        "hummus",
        "ice_cream",
        "lasagna",
        "lobster_bisque",
        "lobster_roll_sandwich",
        "macaroni_and_cheese",
        "macarons",
        "miso_soup",
        "mussels",
        "nachos",
        "omelette",
        "onion_rings",
        "oysters",
        "pad_thai",
        "paella",
        "pancakes",
        "panna_cotta",
        "peking_duck",
        "pho",
        "pizza",
        "pork_chop",
        "poutine",
        "prime_rib",
        "pulled_pork_sandwich",
        "ramen",
        "ravioli",
        "red_velvet_cake",
        "risotto",
        "samosa",
        "sashimi",
        "scallops",
        "seaweed_salad",
        "shrimp_and_grits",
        "spaghetti_bolognese",
        "spaghetti_carbonara",
        "spring_rolls",
        "steak",
        "strawberry_shortcake",
        "sushi",
        "tacos",
        "takoyaki",
        "tiramisu",
        "tuna_tartare",
        "waffles",
    ]

    def validate(self):
        """
        Validates image for file size and file type
        """
        valid = True
        error_message = ""
        if self.img_file.size / (1024 * 1024) > 5:
            error_message += "File size should be less than 5 MB\n"
            valid = False
        if self.img_file.name.split(".")[-1] not in self.formats.keys():
            error_message += "File format should be one of the following: "
            for format in self.formats.keys():
                error_message += format + ", "
            error_message = error_message[:-2]
            valid = False
        return valid, error_message

    def load_model(self):
        """
        Loads model from file
        """
        model = tf.keras.models.load_model("food_vision.h5")
        return model

    def preprocess_image(self, image_shape=224):
        image = Image.open(self.img_file)
        image = tf.keras.preprocessing.image.img_to_array(image)
        image = tf.image.resize(image, [image_shape, image_shape])
        if image.shape[2] == 4:
            image = image[:, :, :3]
        image = tf.cast(image, tf.float32)
        image = tf.expand_dims(image, 0)
        return image

    def predict(self, n=5):
        """
        Predicts image using model
        """
        image = self.preprocess_image()
        model = self.load_model()
        preds = model.predict(image)
        sorted_pred = preds.argsort()
        top_preds = list(preds[0][sorted_pred[0][-n:]])
        top_classes = list(np.array(self.class_names)[sorted_pred[0][-n:]])
        top_preds.reverse(), top_classes.reverse()
        return top_preds, top_classes
