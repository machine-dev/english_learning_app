from plyer import notification
from app.utils.database import Reminder, session
from kivy.clock import Clock
from datetime import datetime

def check_reminders(dt):
    now = datetime.now()
    reminders = session.query(Reminder).all()
    for reminder in reminders:
        if reminder.time <= now:
            notification.notify(
                title='リマインダー',
                message=reminder.message
            )
            session.delete(reminder)
    session.commit()

Clock.schedule_interval(check_reminders, 60)  # 毎分チェック
