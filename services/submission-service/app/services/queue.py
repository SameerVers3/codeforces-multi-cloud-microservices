import pika
import json
from app.config import settings

class SubmissionQueue:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=settings.SUBMISSION_QUEUE, durable=True)
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def publish_submission(self, submission_id: str, problem_id: str, code: str, test_cases: list):
        """Publish submission to queue for execution"""
        if not self.channel:
            self.connect()
        
        message = {
            "submission_id": submission_id,
            "problem_id": problem_id,
            "code": code,
            "test_cases": test_cases
        }
        
        self.channel.basic_publish(
            exchange="",
            routing_key=settings.SUBMISSION_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
    
    def close(self):
        """Close connection"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Global queue instance
submission_queue = SubmissionQueue()

