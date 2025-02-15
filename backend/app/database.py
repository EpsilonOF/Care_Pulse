import motor.motor_asyncio

# Connexion à MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://username:password@host:port/dbname")
db = client['nom_de_la_base']

async def get_n_records(n):
    """Récupérer n enregistrements de la collection spécifiée."""
    collection = db['ma_collection']
    cursor = collection.find().limit(n)
    results = await cursor.to_list(length=n)
    return results
