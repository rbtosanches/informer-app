"""Usuario Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Index
from app.database import Base


class Usuario(Base):
    """Usuario model representing system users."""
    
    __tablename__ = 'iusuarios'
    __table_args__ = ({'schema': 'system'},)
    
    id_usua = Column(Integer, primary_key=True, index=True)
    nom_usua = Column(String(255), nullable=False)
    usuario = Column(String(100), unique=True, nullable=False, index=True)
    nivel_usuario = Column(String(50), default='usuario')
    senha_usuario = Column(String(255), nullable=False)
    ativo_usuario = Column(Boolean, default=True, index=True)
    email_usuario = Column(String(150), index=True)
    dir_usuario = Column(String(255))
    data_usuario = Column(Date, default=datetime.now().date())
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Usuario(id={self.id_usua}, usuario='{self.usuario}')>"
