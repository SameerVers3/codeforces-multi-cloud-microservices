import pika
import json
import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.leaderboard_entry import LeaderboardEntry
from app.services.scoring import calculate_score
from app.config import settings

async def process_scoring(message_body: str):
    """Process scoring from execution results"""
    try:
        data = json.loads(message_body)
        submission_id = data["submission_id"]
        contest_id = data["contest_id"]
        user_id = data["user_id"]
        problem_id = data["problem_id"]
        test_cases_passed = data["test_cases_passed"]
        total_test_cases = data["total_test_cases"]
        execution_time_ms = data.get("execution_time_ms", 0)
        problem_points = data.get("problem_points", 100)
        time_limit_ms = data.get("time_limit_ms", 2000)
        
        # Calculate score
        score = calculate_score(
            test_cases_passed=test_cases_passed,
            total_test_cases=total_test_cases,
            execution_time_ms=execution_time_ms,
            problem_points=problem_points,
            time_limit_ms=time_limit_ms
        )
        
        # Update leaderboard
        db = SessionLocal()
        try:
            entry = db.query(LeaderboardEntry).filter(
                LeaderboardEntry.contest_id == contest_id,
                LeaderboardEntry.user_id == user_id
            ).first()
            
            if not entry:
                entry = LeaderboardEntry(
                    contest_id=contest_id,
                    user_id=user_id,
                    total_score=score,
                    total_submissions=1,
                    total_accepted=1 if test_cases_passed == total_test_cases else 0
                )
                db.add(entry)
            else:
                entry.total_score += score
                entry.total_submissions += 1
                if test_cases_passed == total_test_cases:
                    entry.total_accepted += 1
            
            db.commit()
            
            # Recalculate ranks
            _recalculate_ranks(db, contest_id)
            
        finally:
            db.close()
        
        print(f"Scored submission {submission_id}: {score}")
        return {"score": float(score)}
    except Exception as e:
        print(f"Error processing scoring: {e}")
        return None

def _recalculate_ranks(db: Session, contest_id: str):
    """Recalculate ranks for a contest"""
    entries = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.contest_id == contest_id
    ).order_by(
        LeaderboardEntry.total_score.desc(),
        LeaderboardEntry.last_submission_at.asc()
    ).all()
    
    for rank, entry in enumerate(entries, start=1):
        entry.rank = rank
    
    db.commit()

async def start_worker():
    """Start the scoring worker"""
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
            channel = connection.channel()
            channel.queue_declare(queue=settings.SCORING_QUEUE, durable=True)
            
            def callback(ch, method, properties, body):
                asyncio.create_task(process_scoring(body.decode()))
                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=settings.SCORING_QUEUE, on_message_callback=callback)
            channel.start_consuming()
        except Exception as e:
            print(f"Worker error: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)

