"""User management endpoints and CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from app.database import get_db
from app.models import Usuario
from app.security.password import hash_password, verify_password
from app.security.jwt import verify_token
from app.main import templates

router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])


# ========================================
# Pydantic Models
# ========================================

class UsuarioCreate(BaseModel):
    """Schema for creating a new user."""
    usuario: str
    nom_usua: str
    senha_usuario: str
    email_usuario: Optional[str] = None
    nivel_usuario: str = "user"
    ativo_usuario: bool = True

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    """Schema for updating a user."""
    nom_usua: Optional[str] = None
    email_usuario: Optional[str] = None
    nivel_usuario: Optional[str] = None
    ativo_usuario: Optional[bool] = None
    senha_usuario: Optional[str] = None

    class Config:
        from_attributes = True


class UsuarioResponse(BaseModel):
    """Schema for user response."""
    id_usua: int
    usuario: str
    nom_usua: str
    email_usuario: Optional[str]
    nivel_usuario: str
    ativo_usuario: bool

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


# ========================================
# CRUD Endpoints
# ========================================

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Create a new user (admin only)."""
    
    # Check if user already exists
    existing = db.query(Usuario).filter(Usuario.usuario == usuario_data.usuario).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário já existe"
        )
    
    # Hash password
    hashed_password = hash_password(usuario_data.senha_usuario)
    
    # Create new user
    novo_usuario = Usuario(
        usuario=usuario_data.usuario,
        nom_usua=usuario_data.nom_usua,
        senha_usuario=hashed_password,
        email_usuario=usuario_data.email_usuario,
        nivel_usuario=usuario_data.nivel_usuario,
        ativo_usuario=usuario_data.ativo_usuario
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return novo_usuario


@router.get("/", response_model=List[UsuarioResponse])
async def list_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """List all users (admin only)."""
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(lambda r: verify_token(r.cookies.get("access_token")) or {})
):
    """Get user by ID (admin or self only)."""
    
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    # Users can only view their own profile unless they're admin
    if current_user.get("nivel_usuario") != "admin" and current_user.get("id_usua") != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    usuario = db.query(Usuario).filter(Usuario.id_usua == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Update user (admin only)."""
    
    usuario = db.query(Usuario).filter(Usuario.id_usua == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Update fields if provided
    if usuario_data.nom_usua is not None:
        usuario.nom_usua = usuario_data.nom_usua
    if usuario_data.email_usuario is not None:
        usuario.email_usuario = usuario_data.email_usuario
    if usuario_data.nivel_usuario is not None:
        usuario.nivel_usuario = usuario_data.nivel_usuario
    if usuario_data.ativo_usuario is not None:
        usuario.ativo_usuario = usuario_data.ativo_usuario
    if usuario_data.senha_usuario is not None:
        usuario.senha_usuario = hash_password(usuario_data.senha_usuario)
    
    db.commit()
    db.refresh(usuario)
    
    return usuario


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Delete user (admin only)."""
    
    usuario = db.query(Usuario).filter(Usuario.id_usua == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Prevent deleting the last admin
    if usuario.nivel_usuario == "admin":
        admin_count = db.query(Usuario).filter(Usuario.nivel_usuario == "admin").count()
        if admin_count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível deletar o último administrador"
            )
    
    db.delete(usuario)
    db.commit()
    
    return None


# ========================================
# Management Page (HTML)
# ========================================

@router.get("/pages/usuarios", response_class=HTMLResponse)
async def usuarios_page(
    request: Request,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)
):
    """Display user management page (admin only)."""
    
    usuarios = db.query(Usuario).all()
    
    return templates.TemplateResponse(
        "usuarios.html",
        {
            "request": request,
            "usuarios": usuarios,
            "current_user": admin
        }
    )
