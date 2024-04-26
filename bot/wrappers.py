from functools import wraps

from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot import exceptions as e
from bot.keyboards import InlineMenu

from .states import TextStates, ImgEditStates, ImgGenStates


def validators(func):
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        context = await state.get_data()
        cancel_btn = context.get('cancel_btn')
        try:
            return await func(message, state, *args, **kwargs)
        except e.IncorrectModelError:
            models_kb = context.get('models_kb')
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Некорректная модель!</strong>'
            )
            msg2 = (
                '<em>Нажмите кнопку с корректной моделью</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            await message.answer(msg2, reply_markup=models_kb)
            await state.set_state(TextStates.choseModel)
        except e.InsufficientFundsError:
            menu = InlineMenu().place(
                **{
                    'Докупить запросы': 'buy',
                    'На главную': 'start',
                    'Начать новый диалог': 'ask',
                }
            )
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>У вас закончились запросы 😔</strong>\n\n'
                '<em>Пополните баланс или выберите другую модель!</em>'
            )
            await message.answer(msg, reply_markup=menu)
            await state.clear()
        except e.IncorrectImageSizeError:
            kb = context.get('sizes_kb')
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Open AI не сможет отправить фото такого размера'
                '</strong>'
            )
            msg2 = (
                '<em>Пожалуйста выберите размер генерируемой картинки\n'
                'из доступных вариантов ниже</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            await message.answer(msg2, reply_markup=kb)
            current_state = await state.get_state()
            if current_state == ImgEditStates.erased:
                await state.set_state(ImgEditStates.erased)
            elif current_state == ImgGenStates.size:
                await state.set_state(ImgGenStates.size)
        except e.IncorrectImageFormatError:
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Некорректный формат изображения</strong>\n\n'
                '<em>Изображение должно быть в формате <strong>.PNG</strong>\n'
                'Не забудте снять галочку с опции "Compress the image"\n\n'
                'Отправьте изображение еще раз</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            current_state = await state.get_state()
            if current_state == ImgEditStates.original:
                await state.set_state(ImgEditStates.original)
            elif current_state == ImgEditStates.erased:
                await state.set_state(ImgEditStates.erased)
        except e.AspectRatioMismatchError:
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Изображение должно быть квадратным!</strong>\n\n'
                '<em>Длинна и ширина вашей картинки должны быть равны,\n'
                'для корректной обработки Open AI\n\n'
                'Отредактируйте ваше изображение и отправьте мне его еще раз\n'
                '</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            current_state = await state.get_state()
            if current_state == ImgEditStates.original:
                await state.set_state(ImgEditStates.original)
            elif current_state == ImgEditStates.erased:
                await state.set_state(ImgEditStates.erased)
        except e.UnknownQualityError:
            kb = context.get('quality_kb')
            msg = (
                '🔴🔴🔴\n\n'
                '<strong>Вы ввели несуществующее качество</strong>'
            )
            msg2 = (
                '<em>Пожалуйста, выберите уровень качества генерируемой\n'
                'картинки из вариантов ниже</em>'
            )
            await message.answer(msg, reply_markup=cancel_btn)
            await message.answer(msg2, reply_markup=kb)
            await state.set_state(ImgGenStates.size)
    return wrapper
