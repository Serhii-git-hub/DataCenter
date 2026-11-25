import asyncio

from auth.security import hash_password
from db.db_helper import db_helper
from model.users import User


async def main():
    async with db_helper.session_factory() as session:
        admin = User(
            full_name="Administrator",
            login="admin",
            password_hash = hash_password('admin_password_2050'),
            role = "admin",
        )
        session.add(admin)
        await session.commit()
        print(f'{admin.user_id}')
    await db_helper.dispose()

if __name__ == '__main__':
    asyncio.run(main())