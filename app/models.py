from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Link(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    original_url: so.Mapped[str] = so.mapped_column(sa.String(300), nullable=False)
    short_url: so.Mapped[str] = so.mapped_column(sa.String, unique=True, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    visit_count: so.Mapped[int] = so.mapped_column(sa.Integer, default=0, nullable=True)
    deletion_date: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    max_visits: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)

    def __repr__(self):
        return '<Link {}>'.format(self.original_url)