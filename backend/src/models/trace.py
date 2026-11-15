from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,String,JSON,UniqueConstraint
from src.config.database import Base
class ObservationTrace(Base):
 __tablename__='observation_traces'
 __table_args__=(UniqueConstraint('study_id','reference'),)
 id:Mapped[int]=mapped_column(primary_key=True)
 study_id:Mapped[int]=mapped_column(ForeignKey('sequence_studies.id'))
 reference:Mapped[str]=mapped_column(String(100))
 tokens:Mapped[list]=mapped_column(JSON)
