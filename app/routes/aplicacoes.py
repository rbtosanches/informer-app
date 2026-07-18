"""Application management routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.models import Aplicacao, UsuarioAplicacao, Usuario
from app.security.jwt import verify_token
from app.main import templates

router = APIRouter(prefix="/api/aplicacoes", tags=["aplicacoes"])


# ========================================
# Pydantic Models
# ========================================

class AplicacaoCreate(BaseModel):
    """Schema for creating a new application."""
    nom_aplic: str
    desc_aplic: Optional[str] = None
    url_aplic: Optional[str] = None
    ativo_aplic: bool = True

    class Config:
        from_attributes = True


class AplicacaoUpdate(BaseModel):
    """Schema for updating an application."""
    nom_aplic: Optional[str] = None
    desc_aplic: Optional[str] = None
    url_aplic: Optional[str] = None
    ativo_aplic: Optional[bool] = None

    class Config:
        from_attributes = True


class AplicacaoResponse(BaseModel):
    """Schema for application response."""
    id_aplic: int
    nom_aplic: str
    desc_aplic: Optional[str]
    url_aplic: Optional[str]
    ativo_aplic: bool

    class Config:
        from_attributes = True


class UsuarioAplicacaoResponse(BaseModel):
    """Schema for user-application assignment."""
    id_usua: int
    id_aplic: int
    ativo_usua_aplic: bool

    class Config:
        from_attributes = True


# ========================================
# Helper Functions
# ========================================

def get_current_admin(request: Request) -> dict:
    """Get current user and verify admin role."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    payload = verify_token(token)
    if not payload or payload.get("nivel_usuario") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    
    return payload


def get_current_user(request: Request) -> dict:
    """Get current user from token."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return payload


# ========================================
# CRUD Endpoints
# ========================================

@router.post("/", response_model=AplicacaoResponse, status_code=status.HTTP_201_CREATED)
async def create_aplicacao(
    app_data: AplicacaoCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Create a new application (admin only)."""
    
    nova_app = Aplicacao(
        nom_aplic=app_data.nom_aplic,
        desc_aplic=app_data.desc_aplic,
        url_aplic=app_data.url_aplic,
        ativo_aplic=app_data.ativo_aplic
    )
    
    db.add(nova_app)
    db.commit()
    db.refresh(nova_app)
    
    return nova_app


@router.get("/", response_model=List[AplicacaoResponse])
async def list_aplicacoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """List all applications (admin only)."""
    aplicacoes = db.query(Aplicacao).offset(skip).limit(limit).all()
    return aplicacoes


@router.get("/{app_id}", response_model=AplicacaoResponse)
async def get_aplicacao(
    app_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get application by ID."""
    
    aplicacao = db.query(Aplicacao).filter(Aplicacao.id_aplic == app_id).first()
    if not aplicacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aplicação não encontrada")
    
    # Check if user has access to this app
    if current_user["nivel_usuario"] != "admin":
        has_access = db.query(UsuarioAplicacao).filter(
            UsuarioAplicacao.id_usua == current_user["id_usua"],
            UsuarioAplicacao.id_aplic == app_id,
            UsuarioAplicacao.ativo_usua_aplic == True
        ).first()
        
        if not has_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    return aplicacao


@router.put("/{app_id}", response_model=AplicacaoResponse)
async def update_aplicacao(
    app_id: int,
    app_data: AplicacaoUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Update application (admin only)."""
    
    aplicacao = db.query(Aplicacao).filter(Aplicacao.id_aplic == app_id).first()
    if not aplicacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aplicação não encontrada")
    
    if app_data.nom_aplic is not None:
        aplicacao.nom_aplic = app_data.nom_aplic
    if app_data.desc_aplic is not None:
        aplicacao.desc_aplic = app_data.desc_aplic
    if app_data.url_aplic is not None:
        aplicacao.url_aplic = app_data.url_aplic
    if app_data.ativo_aplic is not None:
        aplicacao.ativo_aplic = app_data.ativo_aplic
    
    db.commit()
    db.refresh(aplicacao)
    
    return aplicacao


@router.delete("/{app_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aplicacao(
    app_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Delete application (admin only)."""
    
    aplicacao = db.query(Aplicacao).filter(Aplicacao.id_aplic == app_id).first()
    if not aplicacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aplicação não encontrada")
    
    # Delete all user-app assignments first
    db.query(UsuarioAplicacao).filter(UsuarioAplicacao.id_aplic == app_id).delete()
    
    db.delete(aplicacao)
    db.commit()
    
    return None


# ========================================
# User-Application Assignment
# ========================================

@router.post("/{app_id}/usuarios/{usuario_id}", status_code=status.HTTP_201_CREATED)
async def assign_usuario_to_app(
    app_id: int,
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Assign a user to an application (admin only)."""
    
    # Verify app exists
    app = db.query(Aplicacao).filter(Aplicacao.id_aplic == app_id).first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aplicação não encontrada")
    
    # Verify user exists
    user = db.query(Usuario).filter(Usuario.id_usua == usuario_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Check if already assigned
    existing = db.query(UsuarioAplicacao).filter(
        UsuarioAplicacao.id_usua == usuario_id,
        UsuarioAplicacao.id_aplic == app_id
    ).first()
    
    if existing:
        existing.ativo_usua_aplic = True
        db.commit()
        return {"message": "Usuário já atribuído à aplicação"}
    
    # Create new assignment
    assignment = UsuarioAplicacao(
        id_usua=usuario_id,
        id_aplic=app_id,
        ativo_usua_aplic=True
    )
    
    db.add(assignment)
    db.commit()
    
    return {"message": "Usuário atribuído à aplicação com sucesso"}


@router.delete("/{app_id}/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_usuario_from_app(
    app_id: int,
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Remove user from an application (admin only)."""
    
    assignment = db.query(UsuarioAplicacao).filter(
        UsuarioAplicacao.id_usua == usuario_id,
        UsuarioAplicacao.id_aplic == app_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atribuição não encontrada")
    
    db.delete(assignment)
    db.commit()
    
    return None


# ========================================
# Management Pages (HTML)
# ========================================

@router.get("/pages/aplicacoes", response_class=HTMLResponse)
async def aplicacoes_page(
    request: Request,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Display applications management page (admin only)."""
    
    aplicacoes = db.query(Aplicacao).all()
    
    return templates.TemplateResponse(
        "aplicacoes.html",
        {
            "request": request,
            "aplicacoes": aplicacoes,
            "current_user": admin
        }
    )
