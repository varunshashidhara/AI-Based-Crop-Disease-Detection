from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    "Data",
    target_size=(224,224),
    batch_size=32,
    class_mode="categorical",
    subset="training"
)

print("Classes detected:", train_generator.class_indices)
