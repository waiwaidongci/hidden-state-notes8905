from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,JSON,Text
from src.config.database import Base
class SequenceStudy(Base):
 __tablename__='sequence_studies'
 id:Mapped[int]=mapped_column(primary_key=True)
 name:Mapped[str]=mapped_column(String(150),unique=True)
 filename:Mapped[str]=mapped_column(String(180))
 description:Mapped[str]=mapped_column(Text,default='')
 symbols:Mapped[list]=mapped_column(JSON)
