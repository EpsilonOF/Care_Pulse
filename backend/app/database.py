import motor.motor_asyncio

# Connexion à MongoDB en utilisant les identifiants et le nom de l'hôte spécifiés dans docker-compose.yml
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://doctogreed:[1[8m.b68Ac~Ke5I{{Sa@mongo:27017/")
db = client['mgdb-infallible-raman']

async def get_n_records(n):
    """Récupérer n enregistrements de la collection spécifiée."""
    collection = db['ma_collection']
    cursor = collection.find().limit(n)
    results = await cursor.to_list(length=n)
    return results
