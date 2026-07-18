"""UsuarioAplicacao Model."""

from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from app.database import Base


class UsuarioAplicacao(Base):
    """UsuarioAplicacao model linking users to applications."""
    
    __tablename__ = 'iusuarios_iaplicacoes'
    __table_args__ = (
        UniqueConstraint('id_usua', 'id_aplic', name='uq_usua_aplic'),
        {'schema': 'system'}
    )
    
    id_usua_aplic = Column(Integer, primary_key=True, index=True)
    id_usua = Column(Integer, ForeignKey('system.iusuarios.id_usua', ondelete='CASCADE'), nullable=False)
    id_aplic = Column(Integer, ForeignKey('system.iaplicacoes.id_aplic', ondelete='CASCADE'), nullable=False)
    ativo_usua_aplic = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UsuarioAplicacao(id={self.id_usua_aplic}, usuario={self.id_usua}, aplicacao={self.id_aplic})>"
