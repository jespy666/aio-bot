from aiogram.filters import Command
from aiogram import Router, F, Bot
from aiogram.types.message import ContentType
from aiogram.types import (Message, CallbackQuery, PreCheckoutQuery,
                           LabeledPrice, SuccessfulPayment)

from ..keyboards import InlineKeyboard

from config import config


payment_router = Router()


@payment_router.message(Command('payment'))
async def show_pricing(message: Message) -> None:
    msg = (
        'Выберите сумму платежа (в рублях)'
    )
    opt = InlineKeyboard().place(
        {
            '100 ₽': 'pay_100',
            '200 ₽': 'pay_200',
            '300 ₽': 'pay_300',
            '500 ₽': 'pay_500',
            '1000 ₽': 'pay_1000',
        }
    )
    await message.answer(msg, reply_markup=opt)


@payment_router.callback_query(
    lambda callback: callback.data in config.PAYMENT_OPTIONS.keys()
)
async def process_payment(callback: CallbackQuery) -> None:
    user_id: int = callback.from_user.id
    data: str = callback.data
    img_url: str = config.PAYMENT_OPTIONS[data]['img_url']
    amount: tuple = config.PAYMENT_OPTIONS[data]['amount']
    await callback.bot.send_invoice(
        chat_id=user_id,
        title='Пополнение баланса',
        description=f'{amount[1]} ₽',
        photo_url=img_url,
        photo_width=450,
        photo_height=160,
        provider_token=config.PAYMENT_PROVIDER_TOKEN,
        currency='rub',
        prices=[LabeledPrice(label='На счет', amount=amount[0])],
        is_flexible=False,
        start_parameter='AIO_Chat',
        payload=f'{user_id} pay {amount[1]}',
    )


@payment_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout(pc_query: PreCheckoutQuery, bot: Bot) -> None:
    await bot.answer_pre_checkout_query(pc_query.id, ok=True)


@payment_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_success_payment(message: Message) -> None:
    payment: SuccessfulPayment = message.successful_payment
    await message.answer(f'Вы успешно оплатили {payment.total_amount//100} рублей')


@payment_router.callback_query(F.data == 'payment')
async def payment_callback(callback: CallbackQuery) -> None:
    await show_pricing(callback.message)
