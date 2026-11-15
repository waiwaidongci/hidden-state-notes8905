from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,String,JSON,Text,DateTime
from sqlalchemy.dialects.mysql import DOUBLE
from datetime import datetime,timezone
from src.config.database import Base
class InferenceRun(Base):
 __tablename__='inference_runs'
 id:Mapped[int]=mapped_column(primary_key=True)
 study_id:Mapped[int]=mapped_column(ForeignKey('sequence_studies.id'))
 profile_id:Mapped[int]=mapped_column(ForeignKey('model_profiles.id'))
 name:Mapped[str]=mapped_column(String(180),unique=True)
 profile_snapshot:Mapped[dict]=mapped_column(JSON)
 trace_snapshot:Mapped[list]=mapped_column(JSON)
 status:Mapped[str]=mapped_column(String(24),default='queued')
 result:Mapped[dict|None]=mapped_column(JSON,nullable=True)
 error:Mapped[str|None]=mapped_column(Text,nullable=True)
 total_log_likelihood:Mapped[float|None]=mapped_column(DOUBLE(asdecimal=False),nullable=True)
 created_by:Mapped[str]=mapped_column(String(120))
 created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
