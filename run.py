from app.app import create_app
from app.utils.tasks import free_reserved_tables
from apscheduler.schedulers.background import BackgroundScheduler

app = create_app()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: free_reserved_tables(app), trigger="interval", minutes=1
    )
    scheduler.start()
    app.run(debug=True)
