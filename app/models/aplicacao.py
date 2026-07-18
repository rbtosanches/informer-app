"""Aplicacao Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text
from app.database import Base


class Aplicacao(Base):
    """Aplicacao model representing system applications."""
    
    __tablename__ = 'iaplicacoes'
    __table_args__ = ({'schema': 'system'},)
    
    id_aplic = Column(Integer, primary_key=True, index=True)
    cod_aplic = Column(String(50), unique=True, nullable=False, index=True)
    nom_aplic = Column(String(150), nullable=False)
    desc_aplic = Column(Text)
    end_aplic = Column(String(255))
    ativo_aplic = Column(Boolean, default=True, index=True)
    data_aplic = Column(Date, default=datetime.now().date())
    versao_aplic = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Aplicacao(id={self.id_aplic}, cod='{self.cod_aplic}')>"
