from db_session import SqlAlchemyBase
import sqlalchemy as sa

class DiaryTasks(SqlAlchemyBase):
    __tablename__ = 'Tasks'
    task_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    task_title = sa.Column(sa.String, nullable=True)
    task_content = sa.Column(sa.String, nullable=True)
    task_created_date = sa.Column(sa.DateTime, nullable=True)
    task_end_date = sa.Column(sa.Date, nullable=False)
    task_end_time = sa.Column(sa.Time, nullable=False)