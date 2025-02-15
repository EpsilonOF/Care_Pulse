routes :

/create/patient
creer un patient
curl -X POST http://localhost:8000/create/patient/ \
-H "Content-Type: application/json" \
-d '{"nom": "Jean Dupont"}'
