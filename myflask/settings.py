"""
Application configuration.
Most configuration is set via environment variables.
For local development, use a .env file to set
environment variables.
"""

SECRET_KEY = "bigmimi"
JSON_AS_ASCII = False
JSON_SORT_KEYS = False

MONGO_URI = "mongodb+srv://chaosrecyclebin:Python3.7@cluster0-xng8n.mongodb.net/test?retryWrites=true&w=majority"
