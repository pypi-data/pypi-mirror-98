"""Store various application values."""
import os


class AppKeys:
    """Store application keys in one place."""

    GITHUB_TOKEN = 'GITHUB_TOKEN'
    VAULT_ADDR = 'VAULT_ADDR'

    IMAGE_API_RELATIVE_URL = 'image_api_relative_url'
    IMAGE_ENHANCE_API_RELATIVE_URL = 'image_enhance_api_relative_url'


class SecretPaths:
    """Store secret paths used against the vault service."""

    TOKEN_ENDPOINT = os.environ['TOKEN_ENDPOINT']
    CLIENT_ID_API = os.environ['CLIENT_ID_API']
    CLIENT_SECRET_API = os.environ['CLIENT_SECRET_API']
    LOUVRE_DOMAIN = os.environ['LOUVRE_DOMAIN']

    # Against PROD
    TOKEN_ENDPOINT_PROD = os.environ['TOKEN_ENDPOINT_PROD']
    CLIENT_ID_API_PROD = os.environ['CLIENT_ID_API_PROD']
    CLIENT_SECRET_API_PROD = os.environ['CLIENT_SECRET_API_PROD']
    LOUVRE_DOMAIN_PROD = os.environ['LOUVRE_DOMAIN_PROD']

    ISSUER = os.environ['ISSUER']


class ImageVariants:
    """Allowed values for the image variant parameter."""

    STANDARD = 'standard'
    THUMBNAIL = 'thumbnail'
    ORIGINAL = 'original'
    DEFAULT = STANDARD
