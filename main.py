import uvicorn
from data import init_db, stop_sessions

if __name__ == "__main__":
    session = init_db()

    uvicorn.run("api:app", host="192.168.64.161", port=8000, reload=True)    

    stop_sessions(session)
