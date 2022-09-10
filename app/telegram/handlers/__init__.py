from aiogram import Router


def setup_routers() -> Router:
    from . import main_menu
    
    router = Router()
    router.include_router(main_menu.router)

    return router
