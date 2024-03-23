from datetime import datetime, timedelta
from dateutil import parser
import pytz
import os
from Subscription import Subscription
from User import User
from appwrite.client import Client
from appwrite.services.databases import Databases
from dotenv import load_dotenv

# Billing process
def run_billing_process(client: Client, databases: Databases):
    print("Running billing cycle...")
    sub = Subscription()
    active_subscribers = sub.get_active_subscriptions()
    
    now_utc = datetime.now(pytz.utc)
    print(f"Now: {now_utc}")
    
    for active_subscriber in active_subscribers:
        try:
            renewal_date = parser.isoparse(active_subscriber['renewal_date'])
            
            if renewal_date <= now_utc:
                user = User(active_subscriber["email"])
                subscription = user.get_subscription(active_subscriber["subscription_id"])
                
                # Determine the next renewal date based on frequency
                frequency_to_timedelta = {
                    'weekly': timedelta(weeks=1),
                    'monthly': timedelta(days=30),
                    'yearly': timedelta(days=365),
                    'daily': timedelta(days=1),
                    'hourly': timedelta(hours=1)
                }

                frequency = subscription.get_frequency()
                if frequency not in frequency_to_timedelta:
                    raise ValueError("Invalid frequency type")

                new_renewal_date = now_utc + frequency_to_timedelta[frequency]
                # Process payment and update the subscription
                card = user.get_card()
                if subscription.get_is_enabled():
                    print(f"Subscription '{subscription.get_description()}' is currently enabled, trying payment...")
                    payment_result = card.process_payment(subscription.get_price(), user)
                    if payment_result:
                        try:
                            databases.update_document(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'), active_subscriber['$id'], {"renewal_date": new_renewal_date.isoformat()})
                            print("Payment successful. Renewal date updated")
                        except Exception as e:
                            print(f"Failed to update renewal date for subscriber {active_subscriber['email']}: {e}")
                    else:
                        try:
                            databases.update_document(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'), active_subscriber['$id'], {"is_enabled": False})
                            print("Payment error. Subscription deactivated")
                        except Exception as e:
                            print(f"Failed to deactivate subscription for {active_subscriber['email']}: {e}")
                else:
                    print("Subscription is not active")
        except Exception as e:
            # Log the error and potentially send a notification to the system admin
            print(f"Failed to process renewal for subscriber {active_subscriber['email']}: {e}")
            # Deactivate the subscription
    print("Billing cycle completed")

def schedule_hourly_task(run_task):
    from threading import Timer
    
    def task_wrapper():
        run_task()
        # Schedule the next call itself
        Timer(3600, task_wrapper).start()

    # Start the recurring task
    task_wrapper()

def main():
    load_dotenv()
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')
    client.set_project(os.getenv('PROJECT_ID'))
    client.set_key(os.getenv('APPWRITE_API_KEY'))
    databases = Databases(client)
    
    def billing_process_wrapper():
        run_billing_process(client, databases)

    schedule_hourly_task(billing_process_wrapper)

if __name__ == "__main__":
    main()
