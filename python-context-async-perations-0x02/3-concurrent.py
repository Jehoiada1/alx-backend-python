import asyncio
import aiosqlite

DB_NAME = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:")
    print(all_users)
    print("\nUsers Older Than 40:")
    print(older_users)

# Run the concurrent fetch
asyncio.run(fetch_concurrently())
