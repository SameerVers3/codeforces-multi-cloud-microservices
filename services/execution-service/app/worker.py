import pika
import json
import httpx
import asyncio
from app.config import settings
from app.executor.cpp_executor import CppExecutor

executor = CppExecutor()

async def process_submission(message_body: str):
    """Process a submission from the queue"""
    try:
        data = json.loads(message_body)
        submission_id = data["submission_id"]
        problem_id = data["problem_id"]
        code = data["code"]
        test_cases = data["test_cases"]
        
        # Execute code
        result = executor.execute(
            code=code,
            test_cases=test_cases,
            time_limit_seconds=2,  # Default, should come from problem config
            memory_limit_mb=256  # Default, should come from problem config
        )
        
        # Update submission status via submission service
        # In a real implementation, this would be done via HTTP or message queue
        print(f"Submission {submission_id} processed: {result['status']}")
        
        return result
    except Exception as e:
        print(f"Error processing submission: {e}")
        return None

async def start_worker():
    """Start the message queue worker"""
    connection = None
    channel = None
    
    while True:
        try:
            # Connect to RabbitMQ
            connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            channel = connection.channel()
            channel.queue_declare(queue=settings.SUBMISSION_QUEUE, durable=True)
            
            print(f"Worker started, listening on queue: {settings.SUBMISSION_QUEUE}")
            
            # Consume messages
            def callback(ch, method, properties, body):
                asyncio.create_task(process_submission(body.decode()))
                ch.basic_ack(delivery_tag=method.delivery_tag)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=settings.SUBMISSION_QUEUE,
                on_message_callback=callback
            )
            
            channel.start_consuming()
        except Exception as e:
            print(f"Worker error: {e}, retrying in 5 seconds...")
            await asyncio.sleep(5)
        finally:
            if channel and channel.is_open:
                channel.close()
            if connection and not connection.is_closed:
                connection.close()

