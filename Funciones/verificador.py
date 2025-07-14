# verificacion.py

from functools import wraps
from flask import session, redirect, url_for, flash

def login_requerido(func):
    @wraps(func)
    def decorada(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión primero.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorada

def es_admin():
    """Devuelve True si el usuario logueado es admin."""
    return session.get('rango') == 'admin'

def admin_requerido(func):
    """Decorador para rutas solo accesibles por admins."""
    @wraps(func)
    def decorada(*args, **kwargs):
        if not es_admin():
            flash('No tienes permisos para entrar aquí.')
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorada
