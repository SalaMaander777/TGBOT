from sqlalchemy import BigInteger, String, ForeignKey, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)



class RealOrganizations(Base):
    __tablename__ = "real_organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    organization_name: Mapped[str] = mapped_column(String(255))
    FIO: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))   


class FakeOrganizations(Base):
    __tablename__ = "fake_organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(255))
    INN_KPP: Mapped[str] = mapped_column(String(255))
    FIO: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    photo: Mapped[str] = mapped_column(String(255))

class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    product_name: Mapped[str] = mapped_column(String(255))
    price = mapped_column(DECIMAL)
    amount: Mapped[int] = mapped_column()


async def async_main():
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)