"""
MongoDB connection and client helper module for idesignweb.
Provides direct PyMongo access with connection pooling and index setup.
"""

from pymongo import MongoClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

_mongo_client = None

def get_mongo_client():
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=3000)
    return _mongo_client

def get_db():
    client = get_mongo_client()
    return client[settings.MONGO_DB_NAME]

def get_collection(name):
    db = get_db()
    return db[name]

def init_indexes():
    """Create essential indexes for collections."""
    try:
        db = get_db()
        # Public content indexes
        db.services.create_index('slug', unique=True)
        db.services.create_index('sort_order')
        db.case_studies.create_index('slug', unique=True)
        db.case_studies.create_index('published_at')
        db.posts.create_index('slug', unique=True)
        db.posts.create_index('published_at')
        db.inquiries.create_index('submitted_at')
        
        # Portal collections indexes
        db.announcements.create_index('created_at')
        db.projects.create_index('client_username')
        db.projects.create_index('project_code', unique=True)
        db.assets.create_index('client_username')
        db.tickets.create_index('ticket_id', unique=True)
        db.tickets.create_index('client_username')
        return True
    except Exception as exc:
        logger.warning("Index initialization notice: %s", exc)
        return False
