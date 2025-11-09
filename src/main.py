import asyncio
from aiogram import Bot, Dispatcher

from src.config import settings
from src.presentation.handlers import main_router

from src.core.UseCases.user_use_cases import UserUseCases
from src.core.UseCases.referal_use_cases import ReferalUseCases
# from src.core.UseCases.subscription_use_cases import SubsUseCase
from src.core.UseCases.traffic_use_cases import TrafficUseCase
from src.core.UseCases.peer_use_cases import PeerUseCases
from src.core.UseCases.payment_use_cases import PaymentUseCases


from src.infrastructure.db.repositories.referal_repo_impl import ReferalRepo
from src.infrastructure.db.repositories.subs_repo_impl import SubsRepo
from src.infrastructure.db.repositories.user_repo_impl import UserRepo
from src.infrastructure.db.repositories.server_repo_impl import ServerRepo
from src.infrastructure.db.repositories.payment_repo_impl import PaymentRepo
from src.infrastructure.db.repositories.peer_repo_impl import PeerRepo


async def main():

    # db_session_pool = await get_db()

    # реализации репозиториев
    # user_repo = UserRepo(db = db_session_pool)
    # peer_repo = PeerRepo(db = db_session_pool)
    # payment_repo = PaymentRepo(db = db_session_pool)
    # referal_repo = ReferalRepo(db = db_session_pool)
    # subs_repo = SubsRepo(db = db_session_pool)
    # server_repo = ServerRepo(db = db_session_pool)

    # use case
    # user_use_cases_instance = UserUseCases(user_repo=user_repo)
    # peer_use_cases_instance = PeerUseCases(peer_repo=peer_repo)
    # payment_use_cases_instance = PaymentUseCases(payment_repo=payment_repo)
    # referal_use_cases_instance = ReferalUseCases(referal_repo=referal_repo)
    # subscription_use_cases_instance = SubsUseCase(subs_repo=subs_repo)
    # traffic_use_cases_instance = TrafficUseCase(traffic_repo=traffic_repo)
    # server_use_cases_instance = ServerRepo()


    # Настройка бота и деспетчера
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(main_router)

    # зависимости для хэндлеров
    # dp["referal_use_cases"] = referal_use_cases_instance
    # dp["user_use_cases"] = user_use_cases_instance
    # # dp["subs_use_cases"] = subscription_use_cases_instance
    # dp["peer_use_cases"] = peer_use_cases_instance
    # # dp["server_use_cases"] = server_use_cases_instance
    # dp["payment_use_cases"] = payment_use_cases_instance


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
