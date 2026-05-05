from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel , HttpUrl
from sqlalchemy import Column , DateTime , Integer ,String, create_engine
from sqlalchemy.orm import DeclarativeBase , Session , sessionmaker
from fastapi.responses import RedirectResponse
import hashlib
import string

engine = create_engine("sqlite:///./urls.db",connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class ShortURL(Base):
    __tablename__ = "short_urls"
    id = Column(Integer,primary_key= True)
    code = Column(String(16),unique=True,index=True)
    original_url = Column(String(2048), unique=True, index=True)


Base.metadata.create_all(bind=engine)


BASE62 = string.ascii_letters + string.digits

def to_base62(number):
    if number == 0:
        return BASE62[0]
    result = []
    while number:
        result.append(BASE62[number % 62])
        number //= 62
    return "".join(reversed(result))

def make_code(url,length=7):
    digest = hashlib.sha256(url.encode()).hexdigest()
    number = int(digest,16)
    return to_base62(number)[: length]

app = FastAPI(title = "URL Shortener")

BASE_URL = "http://localhost:8000"


class ShortenRequest(BaseModel):
    url:HttpUrl


class ShortenResponse(BaseModel):
    short_url: str
    code:str
    original_url :str




@app.post("/shorten",response_model=ShortenResponse,status_code=201)
def shorten(payload: ShortenRequest):
    long_url = str(payload.url)
    with SessionLocal() as db:
        existing = db.query(ShortURL).filter_by(original_url= long_url).first()
        if existing:
            return ShortenResponse(
                short_url = f"{BASE_URL}/{existing.code}",
                code = existing.code,
                original_url = long_url,
            )
        code = make_code(long_url, length=7) 
        

        record = ShortURL(code=code, original_url=long_url)
        db.add(record)
        db.commit()
        
    return ShortenResponse( short_url=f"{BASE_URL}/{code}", 
                           code=code, 
                           original_url=long_url, )
    

@app.get("/{code}") 
def redirect(code: str):
    with SessionLocal() as db:
        record = db.query(ShortURL).filter_by(code=code).first()
        if not record:
            raise HTTPException(status_code=404, detail="Not found")

    return RedirectResponse(url=record.original_url, status_code=302)
    
    