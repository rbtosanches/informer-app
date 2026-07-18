"""Main FastAPI application with routers."""

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from app.config import settings
from app.database import engine, Base, get_db
from app.models import Usuario, Aplicacao, UsuarioAplicacao
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token, verify_token

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Informer - Sistema de Gestão",
    description="Aplicação web com autenticação, autorização e CRUD completo",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")


# ========================================
# Import and include routers
# ========================================

from app.routes.usuarios import router as usuarios_router
app.include_router(usuarios_router)


# ========================================
# Authentication Helpers
# ========================================

def get_current_user(request: Request):
    """Get current user from session/cookie."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return payload


# ========================================
# Routes: Authentication
# ========================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Redirect to login or menu based on authentication status."""
    token = request.cookies.get("access_token")
    if token and verify_token(token):
        return RedirectResponse(url="/menu")
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/auth/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """Handle user login."""
    form_data = await request.form()
    usuario = form_data.get("usuario")
    senha = form_data.get("senha")
    
    if not usuario or not senha:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário e senha são obrigatórios"},
            status_code=400
        )
    
    # Query user from database
    db_usuario = db.query(Usuario).filter(Usuario.usuario == usuario).first()
    
    if not db_usuario or not verify_password(senha, db_usuario.senha_usuario):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário ou senha inválidos"},
            status_code=401
        )
    
    if not db_usuario.ativo_usuario:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário inativo"},
            status_code=403
        )
    
    # Create JWT token
    token_data = {
        "sub": db_usuario.usuario,
        "id_usua": db_usuario.id_usua,
        "nom_usua": db_usuario.nom_usua,
        "nivel_usuario": db_usuario.nivel_usuario
    }
    access_token = create_access_token(data=token_data)
    
    # Redirect to menu with token in cookie
    response = RedirectResponse(url="/menu", status_code=302)
    response.set_cookie("access_token", access_token, httponly=True, max_age=86400)
    return response


@app.get("/menu", response_class=HTMLResponse)
async def menu(request: Request, db: Session = Depends(get_db)):
    """Display menu with available applications."""
    try:
        current_user = get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    # Get user's applications
    if current_user["nivel_usuario"] == "admin":
        # Admin sees all active applications
        aplicacoes = db.query(Aplicacao).filter(Aplicacao.ativo_aplic == True).all()
    else:
        # Regular users see only their assigned applications
        aplicacoes = db.query(Aplicacao).join(
            UsuarioAplicacao
        ).filter(
            UsuarioAplicacao.id_usua == current_user["id_usua"],
            UsuarioAplicacao.ativo_usua_aplic == True,
            Aplicacao.ativo_aplic == True
        ).all()
    
    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "usuario": current_user["nom_usua"],
            "aplicacoes": aplicacoes
        }
    )


@app.get("/auth/logout")
async def logout(request: Request):
    """Logout user."""
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response


# ========================================
# Health Check
# ========================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


# ========================================
# Error Handlers
# ========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/login")
    return {"detail": exc.detail}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
