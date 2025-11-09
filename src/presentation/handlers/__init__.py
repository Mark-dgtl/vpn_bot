from aiogram import Router
from .admin_handlers import admin_router
from .user_handlers import user_router
# from .payment_handlers import payment_router

# Создаем главный объект Router
main_router = Router()

# Включаем в него все остальные
main_router.include_router(admin_router)
main_router.include_router(user_router)
# main_router.include_router(payment_router)