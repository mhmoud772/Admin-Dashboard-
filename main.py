from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx
import os
import asyncio

import models
from database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="General Admin Dashboard", version="1.0.0")

# Setup Templates
templates = Jinja2Templates(directory="templates")

# Mount Static if exists (assuming we might need it, otherwise we can ignore)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------
# HTML Page Routes
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    systems = db.query(models.System).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "systems": systems})

@app.get("/systems", response_class=HTMLResponse)
async def systems_page(request: Request, db: Session = Depends(get_db)):
    systems = db.query(models.System).all()
    return templates.TemplateResponse("systems.html", {"request": request, "systems": systems})

@app.get("/systems/{system_id}", response_class=HTMLResponse)
async def system_detail_page(request: Request, system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    return templates.TemplateResponse("system_detail.html", {"request": request, "system": system})

@app.get("/logs", response_class=HTMLResponse)
async def logs_page(request: Request, db: Session = Depends(get_db)):
    systems = db.query(models.System).all()
    return templates.TemplateResponse("logs.html", {"request": request, "systems": systems})

# ----------------------------
# API Routes for Systems Management
# ----------------------------
@app.post("/systems/add")
async def add_system(
    name: str = Form(...),
    api_url: str = Form(...),
    system_type: str = Form(...),
    db: Session = Depends(get_db)
):
    new_system = models.System(name=name, api_url=api_url, system_type=system_type)
    db.add(new_system)
    db.commit()
    # Redirect back to systems list
    return RedirectResponse(url="/systems", status_code=303)

@app.post("/systems/{system_id}/delete")
async def delete_system(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if system:
        db.delete(system)
        db.commit()
    return RedirectResponse(url="/systems", status_code=303)

# ----------------------------
# Backend Proxy Async Endpoints 
# ----------------------------
async def fetch_async(url: str, client: httpx.AsyncClient):
    try:
        response = await client.get(url, timeout=3.0)
        return response.json()
    except Exception as e:
        return {"status": "offline", "error": str(e)}

@app.get("/api/systems/{system_id}/health")
async def get_system_health(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    url = f"{system.api_url}/health"
    async with httpx.AsyncClient() as client:
        result = await fetch_async(url, client)
    return result

@app.get("/api/systems/{system_id}/stats")
async def get_system_stats(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    url = f"{system.api_url}/stats"
    async with httpx.AsyncClient() as client:
        result = await fetch_async(url, client)
    return result

@app.get("/api/systems/{system_id}/logs")
async def get_system_logs(system_id: int, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    url = f"{system.api_url}/logs"
    async with httpx.AsyncClient() as client:
        result = await fetch_async(url, client)
    return result

@app.get("/api/systems/all/logs")
async def get_all_logs(db: Session = Depends(get_db)):
    systems = db.query(models.System).all()
    logs = []
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for sys in systems:
            url = f"{sys.api_url}/logs"
            tasks.append(fetch_async(url, client))
        
        results = await asyncio.gather(*tasks)
        
        for sys, res in zip(systems, results):
            sys_logs = res.get("logs", []) if isinstance(res, dict) else []
            for log in sys_logs:
                log["system"] = sys.name
            logs.extend(sys_logs)
            
    # Sort logs by timestamp hypothetically
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return logs
@app.post("/api/systems/{system_id}/action")
async def system_action(system_id: int, request: Request, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.id == system_id).first()
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    
    body = await request.json()
    url = f"{system.api_url}/action"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=body, timeout=3.0)
            return response.json()
    except Exception as e:
        return {"error": str(e)}
