import uvicorn

if __name__ == "__main__":
  host = '0.0.0.0'
  port = 8000

  uvicorn.run("server.api:app", host=host, port=port, reload=True)

