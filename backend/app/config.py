from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    base_dir: str = os.path.dirname(__file__)
    model_path_final: str = Field(
        default=os.path.join(os.path.dirname(__file__), 'crop_disease_model_final.keras'),
        env='MODEL_PATH_FINAL'
    )
    model_path: str = Field(
        default=os.path.join(os.path.dirname(__file__), 'crop_disease_model.keras'),
        env='MODEL_PATH'
    )
    class_indices_path: str = Field(
        default=os.path.join(os.path.dirname(__file__), 'class_indices.json'),
        env='CLASS_INDICES_PATH'
    )
    disease_info_path: str = Field(
        default=os.path.join(os.path.dirname(__file__), 'disease_info.json'),
        env='DISEASE_INFO_PATH'
    )

    class Config:
        env_file = ".env"

settings = Settings()
