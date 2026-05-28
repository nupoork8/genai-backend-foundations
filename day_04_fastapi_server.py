from fastapi import FastAPI
# 1 Initialize FastAPI web engine instance
app = FastAPI(title="GenAI Ingestion Pipeline")

# 2 create basic home endpoint
@app.get("/")
def read_root():

    return{
        "status":"Online",
        "framework":"FastApi",
        "message":"AI Engine server is active"
    }

# 3. Create a data endpoint to receive external inputs (POST Request)
@app.post("/api/v1/query")
def handle_incoming_query(payload: dict):

    #safely extract incoming query text sent by an external application
    user_query = payload.get("query", "")

    simulated_ai_response = f"Processed vector match for query: '{user_query}'"

    return{
        "success":True,
        "received_data":{
            "query": user_query
        },
        "backend_output": simulated_ai_response
    }
