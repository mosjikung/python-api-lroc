from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import engine
import model

from routers import (station , 
                     dashboard , 
                     broadcast , 
                     datauserstation , 
                     onair , 
                     file_management , 
                     onair_management , 
                     onair_broadcastmanagement , 
                     message,
                     datastationma,
                     report,
                     broadcast_web,
                     after_login,
                     guest,
                     member,
                     system,
                     chart_hits,
                     package,
                     partner,
                     support,
                     channel)

# generate model to table postgresql
# model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://nrc-management.xcoshop.com",
    "https://nrc-management-service.xcoshop.com",
    "https://nrc.xcoshop.com",
    "https://tv-oauth.xcoshop.com",
	"http://192.168.1.7:3000",
	"http://192.168.1.53",
	"http://192.168.1.47"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def Home():
    return "Welcome Home"

#allrounter
app.include_router(dashboard.router)
app.include_router(station.router)
app.include_router(broadcast.router)
app.include_router(datauserstation.router)
app.include_router(onair.router)
app.include_router(file_management.router)
app.include_router(onair_management.router)
app.include_router(onair_broadcastmanagement.router)
app.include_router(message.router)
app.include_router(datastationma.router)
app.include_router(report.router)
app.include_router(broadcast_web.router)
app.include_router(after_login.router)
app.include_router(guest.router)
app.include_router(member.router)
app.include_router(system.router)
app.include_router(chart_hits.router)
app.include_router(package.router)
app.include_router(partner.router)
app.include_router(support.router)
app.include_router(channel.router)




