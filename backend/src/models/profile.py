from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,String,JSON,DateTime
from sqlalchemy.dialects.mysql import DOUBLE
from datetime import datetime,timezone
from src.config.database import Base
class ModelProfile(Base):
 __tablename__='model_profiles'
 id:Mapped[int]=mapped_column(primary_key=True)
 study_id:Mapped[int]=mapped_column(ForeignKey('sequence_studies.id'))
 name:Mapped[str]=mapped_column(String(180),unique=True)
 version:Mapped[str]=mapped_column(String(80))
 states:Mapped[list]=mapped_column(JSON)
 symbols:Mapped[list]=mapped_column(JSON)
 parameters:Mapped[dict]=mapped_column(JSON)
 normalization_max_delta:Mapped[float]=mapped_column(DOUBLE(asdecimal=False))
 created_by:Mapped[str]=mapped_column(String(120))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
