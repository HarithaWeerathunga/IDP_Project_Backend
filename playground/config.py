import os
from pathlib import Path

base_dir = Path(__file__).parent.absolute()
instance_dir = base_dir.parent / 'instance'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{instance_dir / 'db.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SPECTRAL_IMAGE_DIR = base_dir.parent / 'binary-masks' / ''
