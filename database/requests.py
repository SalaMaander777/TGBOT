from database.models import async_session
from database.models import Users, RealOrganizations, FakeOrganizations, Products
from sqlalchemy import select
import asyncio


async def get_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        if not user:
            session.add(Users(tg_id=tg_id))
            await session.commit()


async def create_real_organization(tg_id: int, organization_name: str, FIO: str, phone_number: str, email: str, address: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(RealOrganizations).where(RealOrganizations.tg_id == tg_id))
        print(user)
        if not user:
            session.add(RealOrganizations(tg_id=tg_id, organization_name=organization_name, FIO=FIO, phone_number=phone_number, email=email, address=address))
            await session.commit()
        elif user:
            await session.delete(user)
            await session.commit()
            session.add(RealOrganizations(tg_id=tg_id, organization_name=organization_name, FIO=FIO, phone_number=phone_number, email=email, address=address))
            await session.commit()

async def add_product(tg_id: int, product_name: str, price: float, amount: int) -> None:
    async with async_session() as session:
        session.add(Products(tg_id=tg_id, product_name=product_name, price=price, amount=amount))
        await session.commit()

async def delete_product(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalars(select(Products).where(Products.tg_id == tg_id))
        for item in user:
            await session.delete(item)
        await session.commit()


async def get_products(tg_id: int) -> list:
    async with async_session() as session:
        user = await session.scalars(select(Products).where(Products.tg_id == tg_id))
        if user:
            table_data = list()
            i:int = 1
            sum: int = 0
            table_list = user.all()
            #row_num = len(table_list)
            for item in table_list:
                sum += (int(item.price)*int(item.amount))
                table_data.append({'id': i,'product_name': item.product_name, 'price': int(item.price), 'amount': int(item.amount), 'summary': int(item.price)*int(item.amount)})
                i += 1
                

            return table_data, sum
async def get_organizations(tg_id: int) :
    async with async_session() as session:
        user = await session.scalar(select(RealOrganizations).where(RealOrganizations.tg_id == tg_id))
        if user:
            return user
        
async def get_fake_organizations() :
    async with async_session() as session:
        fake_organizations = await session.scalars(select(FakeOrganizations))
        if fake_organizations:
            return fake_organizations
        else:
            return None
    
async def create_fake_organization(organization_name: str, FIO: str, phone_number: str, email: str, address: str) -> None:
    async with async_session() as session:
        session.add(FakeOrganizations(organization_name=organization_name, FIO=FIO, phone_number=phone_number, email=email, address=address))
        await session.commit()


async def delete_fake_organization(id: int) -> None:
    async with async_session() as session:
        del_id = await session.scalar(select(FakeOrganizations).where(FakeOrganizations.id == id))
        
        if del_id != None:
            await session.delete(del_id)
            await session.commit()
            return True
        else: 
            return False