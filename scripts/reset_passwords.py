#!/usr/bin/env python3
"""
Reset default passwords in the database.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Usuario
from app.security.password import hash_password
from app.config import settings

# Load environment
load_dotenv()

# Create engine and session
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Reset admin password
    admin = db.query(Usuario).filter(Usuario.usuario == "admin").first()
    if admin:
        admin.senha_usuario = hash_password("s4nch3s")
        db.commit()
        print("✓ Admin password reset to: s4nch3s")
    
    # Reset rbtosanches password
    user = db.query(Usuario).filter(Usuario.usuario == "rbtosanches").first()
    if user:
        user.senha_usuario = hash_password("s4nch3s")
        db.commit()
        print("✓ User rbtosanches password reset to: s4nch3s")
    
    # Reset usuario_teste password
    test_user = db.query(Usuario).filter(Usuario.usuario == "usuario_teste").first()
    if test_user:
        test_user.senha_usuario = hash_password("s4nch3s")
        db.commit()
        print("✓ User usuario_teste password reset to: s4nch3s")
    
    print("\n✓ All passwords reset successfully!")
    
finally:
    db.close()
