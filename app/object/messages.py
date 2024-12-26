from app.object.functions import house_condition_translation, bathroom_translation
from app.object.models.apartment import Apartment
from app.object.models.commercial import Commercial
from app.object.models.land import Land


async def send_rent_apart(db_apartment):
    message = (f'<b>Сдаётся шикарная квартира🏡</b>\n\n📍Район: {db_apartment.district}\n'
               f'📍Адрес: {db_apartment.title}\n\n'
               f'🎯{db_apartment.rooms} комн {db_apartment.floor}/{db_apartment.floor_number}'
               f'\n🎯Площадь: {db_apartment.square_area} м²\n'
               f'🎯{house_condition_translation.get(db_apartment.house_condition.name, db_apartment.house_condition.name)}✅\n'
               f'🎯Санузел {bathroom_translation.get(db_apartment.bathroom.name, db_apartment.bathroom.name)}✅\n\n'
               f'❗Депозит: Договорная\n'
               f'❗Предоплата: Договорная\n'
               f'💰Цена: {db_apartment.price}$ есть торг\n'
               f'🌀Срм - {db_apartment.crm_id}\n\n'
               f'С уважением {db_apartment.responsible}\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 10000 вариантов по всему городу.✅\n')
    return message


async def send_sale_apart(db_apartment: Apartment, phone: str):
    message = (f'<b>❗️СРОЧНА ! Новостройка недалеко от центре города 🔥</b>\n'
               f'<b>Идеально подходит для инвестции тоже Элитный Комплекс ♻️⚜️</b>\n\n'
               f'<b>Премиум класса 😆</b>\n\n'
               f'📍<b>Район:</b> {db_apartment.district}\n'
               f'📍<b>Адрес:</b> {db_apartment.title}\n\n'
               f'🏠 <b>{db_apartment.rooms}-комнатная квартира</b>\n'
               f'🏢 <b>Этаж:</b> {db_apartment.floor} из {db_apartment.floor_number}\n'
               f'📏 <b>Площадь:</b> {db_apartment.square_area}м²\n'
               f'🛋️ <b>{house_condition_translation.get(db_apartment.house_condition.name, db_apartment.house_condition.name)}</b> ✅\n'
               f'📦 <b>Мебель Техника</b> {'✅' if db_apartment.furnished else '❌'}\n\n'
               f'🚶‍♂️ В 5-10 минутах торговые центры, метро, банки, магазины, аптеки, кофейни, рестораны, кафе быстрого питания, школа, детские сады.\n\n'
               f'💰 <b>Цена:</b> {db_apartment.price} у.е. торг\n\n'
               f'С уважением <b>{db_apartment.responsible}</b>\n'
               f'<b>{db_apartment.responsible} "Legacy Real Estate"</b> 🏦\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 15000 вариантов по всему городу.✅\n'
               f'Перейдите по ссылке и выберите свою квартиру 🏠❤️\n\n'
               f'📬 <b>По вопросам пишите:</b>\n'
               f'📱 <b>Телеграм:</b> <a href="https://t.me/legacyrealestate">legacyrealestate</a>\n'
               f'📷 <b>Инстаграм:</b> <a href="https://instagram.com/legacy.uzbekistan">legacy.uzbekistan</a>\n'
               f'☎️ <b>Телефон:</b> {phone} {db_apartment.responsible}\n'
               f'#{db_apartment.rooms}комнатная')
    return message


async def send_rent_comm(db_commercial: Commercial):
    message = (f'<b>Сдаётся шикарная коммерция🏡</b>\n\n📍Район: {db_commercial.district}\n'
               f'📍Адрес: {db_commercial.title}\n\n'
               f'🎯{db_commercial.rooms} комн {db_commercial.floor_number}'
               f'\n🎯Площадь: {db_commercial.square_area} м²\n'
               f'🎯{house_condition_translation.get(db_commercial.house_condition.name)}✅\n'
               f'🎯Mебель {"✅" if db_commercial.furnished else "❌"}\n\n'
               f'❗Депозит: Договорная\n'
               f'❗Предоплата: Договорная\n'
               f'💰Цена: {db_commercial.price}$ есть торг\n'
               f'🌀Срм - {db_commercial.crm_id}\n\n'
               f'С уважением {db_commercial.responsible}\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 10000 вариантов по всему городу.✅\n')
    return message


async def send_sale_comm(db_commercial: Commercial, phone: str):
    message = (f'<b>❗️СРОЧНА ! Новостройка недалеко от центре города 🔥</b>\n'
               f'<b>Идеально подходит для инвестции тоже Элитный Комплекс ♻️⚜️</b>\n\n'
               f'<b>Премиум класса 😆</b>\n\n'
               f'📍<b>Район:</b> {db_commercial.district}\n'
               f'📍<b>Адрес:</b> {db_commercial.title}\n\n'
               f'🏠 <b>{db_commercial.rooms}-комнатная квартира</b>\n'
               f'🏢 <b>Этажность:</b> {db_commercial.floor_number}\n'
               f'📏 <b>Площадь:</b> {db_commercial.square_area}м²\n'
               f'🛋️ <b>{house_condition_translation.get(db_commercial.house_condition.name, db_commercial.house_condition.name)}</b> ✅\n'
               f'📦 <b>Мебель Техника</b> {'✅' if db_commercial.furnished else '❌'}\n\n'
               f'🚶‍♂️ В 5-10 минутах торговые центры, метро, банки, магазины, аптеки, кофейни, рестораны, кафе быстрого питания, школа, детские сады.\n\n'
               f'💰 <b>Цена:</b> {db_commercial.price} у.е. торг\n\n'
               f'С уважением <b>{db_commercial.responsible}</b>\n'
               f'<b>{db_commercial.responsible} "Legacy Real Estate"</b> 🏦\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 15000 вариантов по всему городу.✅\n'
               f'Перейдите по ссылке и выберите свою квартиру 🏠❤️\n\n'
               f'📬 <b>По вопросам пишите:</b>\n'
               f'📱 <b>Телеграм:</b> <a href="https://t.me/legacyrealestate">legacyrealestate</a>\n'
               f'📷 <b>Инстаграм:</b> <a href="https://instagram.com/legacy.uzbekistan">legacy.uzbekistan</a>\n'
               f'☎️ <b>Телефон:</b> {phone} {db_commercial.responsible}\n'
               f'#{db_commercial.rooms}комнатная')
    return message


async def send_rent_land(db_land: Land):
    message = (f'<b>Сдаётся шикарный участок🏡</b>\n\n📍Район: {db_land.district}\n'
               f'📍Адрес: {db_land.title}\n\n'
               f'🎯{db_land.rooms} комн {db_land.floor_number}'
               f'\n🎯Площадь: {db_land.square_area} м²\n'
               f'🎯{house_condition_translation.get(db_land.house_condition.name)}✅\n'
               f'🎯Mебель {"✅" if db_land.furnished else "❌"}\n\n'
               f'❗Депозит: Договорная\n'
               f'❗Предоплата: Договорная\n'
               f'💰Цена: {db_land.price}$ есть торг\n'
               f'🌀Срм - {db_land.crm_id}\n\n'
               f'С уважением {db_land.responsible}\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 10000 вариантов по всему городу.✅\n')
    return message


async def send_sale_land(db_land: Land, phone: str):
    message = (f'<b>❗️СРОЧНА ! Новостройка недалеко от центре города 🔥</b>\n'
               f'<b>Идеально подходит для инвестции тоже Элитный Комплекс ♻️⚜️</b>\n\n'
               f'<b>Премиум класса 😆</b>\n\n'
               f'📍<b>Район:</b> {db_land.district}\n'
               f'📍<b>Адрес:</b> {db_land.title}\n\n'
               f'🏠 <b>{db_land.rooms}-комнатная квартира</b>\n'
               f'🏢 <b>Этажность:</b> {db_land.floor_number}\n'
               f'📏 <b>Площадь:</b> {db_land.square_area}м²\n'
               f'🛋️ <b>{house_condition_translation.get(db_land.house_condition.name, db_land.house_condition.name)}</b> ✅\n'
               f'📦 <b>Мебель Техника</b> {'✅' if db_land.furnished else '❌'}\n\n'
               f'🚶‍♂️ В 5-10 минутах торговые центры, метро, банки, магазины, аптеки, кофейни, рестораны, кафе быстрого питания, школа, детские сады.\n\n'
               f'💰 <b>Цена:</b> {db_land.price} у.е. торг\n\n'
               f'С уважением <b>{db_land.responsible}</b>\n'
               f'<b>{db_land.responsible} "Legacy Real Estate"</b> 🏦\n'
               f'Специалист по недвижимости!\n'
               f'Имеется также более 15000 вариантов по всему городу.✅\n'
               f'Перейдите по ссылке и выберите свою квартиру 🏠❤️\n\n'
               f'📬 <b>По вопросам пишите:</b>\n'
               f'📱 <b>Телеграм:</b> <a href="https://t.me/legacyrealestate">legacyrealestate</a>\n'
               f'📷 <b>Инстаграм:</b> <a href="https://instagram.com/legacy.uzbekistan">legacy.uzbekistan</a>\n'
               f'☎️ <b>Телефон:</b> {phone} {db_land.responsible}\n'
               f'#{db_land.rooms}комнатная')
    return message