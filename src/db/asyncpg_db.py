import asyncio
import asyncpg


class PGDatabase:
    def __init__(self, user, password, database, host):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(user=self.user, password=self.password, database=self.database,
                                              host=self.host)
        async with self.pool.acquire() as conn:
            return conn

    async def disconnect(self):
        await self.pool.close()

    async def insert_data(self, table, fields, values):
        fields_str = ', '.join(fields)
        placeholders = ', '.join(f'${i + 1}' for i in range(len(fields)))

        insert_query = f'INSERT INTO {table} ({fields_str}) VALUES ({placeholders})'
        async with self.pool.acquire() as conn:
            await conn.executemany(insert_query, values)

    async def upsert_data(self, table, fields, values):
        # upsert query to update all the fields if the primary key already exists
        fields_str = ', '.join(fields)
        placeholders = ', '.join(f'${i + 1}' for i in range(len(fields)))
        update_query = ', '.join(f'{field} = EXCLUDED.{field}' for field in fields if field != 'id')

        upsert_query = f'INSERT INTO {table} ({fields_str}) VALUES ({placeholders}) ON CONFLICT (id) DO UPDATE SET {update_query}'
        async with self.pool.acquire() as conn:
            await conn.executemany(upsert_query, values)

    async def upsert_data_in_batches(self, table, fields, data, chunk_size):
        tasks = []
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            tasks.append(self.upsert_data(table, fields, chunk))
        await asyncio.gather(*tasks)


# usage
async def run(db, table_name, fields, values):
    await db.connect()
    await db.upsert_data_in_batches(table_name, fields, values, 50)
    await db.disconnect()


def bulk_upsert_postgres(db, table_name, fields, values):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(db, table_name, fields, values))
