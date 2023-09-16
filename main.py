import os
import click
import pytz
from sqlalchemy.orm import Session
from modules.User import User
from modules.Wallet import Wallet
from modules.Logs import Log
from modules.Notifications import Notification
from modules.Security import SecuritySetting
from modules.Transaction import Transaction
from modules.PaymentProvider import PaymentProvider
from modules.CurrencyExchange import CurrencyExchangeRate
from modules.database import SessionLocal, engine, Base
from datetime import datetime

# Define the East African Time (EAT) timezone
eat_timezone = pytz.timezone('Africa/Nairobi')

Base.metadata.create_all(bind=engine)

# Define query helper methods

# Function to retrieve all users
def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

# Function to retrieve all wallets for a user
def get_user_wallet(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        wallet = user.wallet
        db.close()
        return wallet
    else:
        db.close()
        return None


# Function to retrieve all logs for a user
def get_user_logs(user_id):
    db = SessionLocal()
    logs = db.query(Log).filter(Log.user_id == user_id).all()
    db.close()
    return logs

# Function to retrieve all notifications for a user
def get_user_notifications(user_id):
    db = SessionLocal()
    notifications = db.query(Notification).filter(Notification.user_id == user_id).all()
    db.close()
    return notifications


# Function to retrieve all security settings for a user
def get_user_security_settings(user_id):
    db = SessionLocal()
    security_settings = db.query(SecuritySetting).filter(SecuritySetting.user_id == user_id).all()
    db.close()
    return security_settings

# Function to retrieve all transactions for a user
def get_user_transactions(user_id):
    db = SessionLocal()
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    db.close()
    return transactions

# Function to retrieve all payment providers
def get_all_payment_providers():
    db = SessionLocal()
    payment_providers = db.query(PaymentProvider).all()
    db.close()
    return payment_providers

# Function to retrieve all currency exchange rates
def get_all_currency_exchange_rates():
    db = SessionLocal()
    currency_exchange_rates = db.query(CurrencyExchangeRate).all()
    db.close()
    return currency_exchange_rates

@click.group()
def main():
    pass

# CLI commands

# Create User Command
@click.command("create-user")
def create_user_command():
    create_user_prompt()

# List Users Command
@click.command("list-users")
def list_users_command():
    list_users()

# Create Wallet Command
@click.command("create-wallet")
def create_wallet_command():
    db = SessionLocal
    create_wallet_for_user_prompt(db)

# List Wallets Command
@click.command("list-wallets")
def list_wallets_command():
    list_wallets()

# Create Log Command
@click.command("create-log")
def create_log_command():
    create_log_prompt()

# List Logs Command
@click.command("list-logs")
def list_logs_command():
    list_logs()

# Create Notification Command
@click.command("create-notification")
def create_notification_command():
    create_notification_prompt()

# List Notifications Command
@click.command("list-notifications")
def list_notifications_command():
    list_notifications()

# Create Security Setting Command
@click.command("create-security-setting")
def create_security_setting_command():
    create_security_setting_prompt()

# List Security Settings Command
@click.command("list-security-settings")
def list_security_settings_command():
    list_security_settings()

# Create Transaction Command
@click.command("create-transaction")
def create_transaction_command():
    create_transaction_prompt()

# List Transactions Command
@click.command("list-transactions")
def list_transactions_command():
    list_transactions()

# List Payment Providers Command
@click.command("list-payment-providers")
def list_payment_providers_command():
    list_payment_providers()

# List Currency Exchange Rates Command
@click.command("list-currency-exchange-rates")
def list_currency_exchange_rates_command():
    list_currency_exchange_rates()

# Exit Command
@click.command("exit")
def exit_command():
    exit_program()

# Add commands to the main group
main.add_command(create_user_command)
main.add_command(list_users_command)
main.add_command(create_wallet_command)
main.add_command(list_wallets_command)
main.add_command(create_log_command)
main.add_command(list_logs_command)
main.add_command(create_notification_command)
main.add_command(list_notifications_command)
main.add_command(create_security_setting_command)
main.add_command(list_security_settings_command)
main.add_command(create_transaction_command)
main.add_command(list_transactions_command)
main.add_command(list_payment_providers_command)
main.add_command(list_currency_exchange_rates_command)
main.add_command(exit_command)

# Implement CLI prompt functions

# Function to create a user with prompts
def create_user_prompt():
    username = click.prompt('Enter a username')
    email = click.prompt('Enter your email address')
    phone_number = click.prompt('Enter phone number')
    password = click.prompt('Enter your password', hide_input=True, confirmation_prompt=True)
    
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()
    existing_email = db.query(User).filter(User.email == email).first()
    existing_phone = db.query(User).filter(User.phone_number == phone_number).first()

    if existing_user:
        db.close()
        print(f"User {username} already exists.")
        return

    if existing_email:
        db.close()
        print(f"Email {email} is already registered.")
        return
    if existing_phone:
        db.close()
        print(f"phone Number {phone_number} is already registered.")
        return


    current_time_eat = datetime.now(eat_timezone)
    
    user = User(username=username, email=email,phone_number=phone_number, password=password, registration_date=current_time_eat)
    db.add(user)
    db.commit()
    db.close()

    print(f"User {username} registered successfully.")

# Function to list all users
def list_users():
    users = get_all_users()
    
    if users:
        print("List of Users:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    else:
        print("No users found.")

# Implement other prompt functions
# Function to create a wallet with prompts
def create_wallet_for_user_prompt(db: Session):
    user_id = click.prompt('Enter User ID', type=int)
    initial_balance = click.prompt('Enter Initial Balance', type=float)
    
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        print(f"User with ID {user_id} does not exist.")
        return

    # Create a new wallet with the initial balance
    wallet = Wallet(balance=initial_balance, user=user)
    
    db.add(wallet)
    db.commit()
    
    print(f"Wallet created successfully for user '{user.username}' with an initial balance of {initial_balance}.")

# Function to list all wallets
def list_wallets():
    user_id = click.prompt('Enter User ID', type=int)
    wallet = get_user_wallet(user_id)
    
    if wallet:
        print(f"Wallet for User ID {user_id}:")
        print(f"ID: {wallet.id}, Balance: {wallet.balance}")
    else:
        print(f"No wallet found for User ID {user_id}.")


# Function to create a log with prompts
def create_log_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    action = click.prompt('Enter Log Action', type=str)
    timestamp = datetime.now(eat_timezone)
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    try:
        new_log = Log(action=action, timestamp=timestamp, user=user)
        db.add(new_log)
        db.commit()
        print(f"Log created successfully for user '{user.username}'.")
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise
    finally:
        db.close()

# Function to list all logs
def list_logs():
    user_id = click.prompt('Enter User ID', type=int)
    logs = get_user_logs(user_id)
    
    if logs:
        print(f"Logs for User ID {user_id}:")
        for log in logs:
            print(f"ID: {log.id}, Action: {log.action}, Timestamp: {log.timestamp}")
    else:
        print(f"No logs found for User ID {user_id}.")

# Function to create a notification with prompts
def create_notification_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    message = click.prompt('Enter Notification Message', type=str)
    is_read = click.prompt('Is Notification Read? (True/False)', type=bool)
    timestamp = datetime.now(eat_timezone)
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    try:
        new_notification = Notification(message=message, is_read=is_read, timestamp=timestamp, user=user)
        db.add(new_notification)
        db.commit()
        print(f"Notification created successfully for user '{user.username}'.")
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise
    finally:
        db.close()

# Function to list all notifications
def list_notifications():
    user_id = click.prompt('Enter User ID', type=int)
    notifications = get_user_notifications(user_id)
    
    if notifications:
        print(f"Notifications for User ID {user_id}:")
        for notification in notifications:
            print(f"ID: {notification.id}, Message: {notification.message}, Read: {notification.is_read}, Timestamp: {notification.timestamp}")
    else:
        print(f"No notifications found for User ID {user_id}.")

def create_security_setting_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    two_factor_enabled = click.prompt('Is Two-Factor Authentication Enabled? (True/False)', type=bool)
    password_expiry_days = click.prompt('Enter Password Expiry Days', type=int)
    password_history = click.prompt('Enter Password History Count', type=int)

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    try:
        new_security_setting = SecuritySetting(
            user_id=user_id,
            two_factor_enabled=two_factor_enabled,
            password_expiry_days=password_expiry_days,
            password_history=password_history
        )
        db.add(new_security_setting)
        db.commit()
        print(f"Security setting created successfully for user '{user.username}'.")
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise
    finally:
        db.close()

# Function to list all security settings for a user
def list_security_settings():
    user_id = click.prompt('Enter User ID', type=int)
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    security_settings = user.security_settings
    
    if security_settings:
        print("List of Security Settings:")
        for setting in security_settings:
            print(f"ID: {setting.id}, User ID: {setting.user_id}, "
                  f"Two-Factor Enabled: {setting.two_factor_enabled}, "
                  f"Password Expiry Days: {setting.password_expiry_days}, "
                  f"Password History: {setting.password_history}")
    else:
        print(f"No security settings found for user '{user.username}'.")
    
    db.close()

# Function to handle deposit prompt
def handle_deposit_prompt(db: Session, user):
    amount = click.prompt("Enter the deposit amount:", type=float)
    try:
        transaction = Transaction.make_deposit(user, amount)
        db.add(transaction)
        db.commit()
        print(f"Deposit of {amount} successfully made.")
    except ValueError as e:
        print(str(e))

# Function to handle withdrawal prompt
def handle_withdrawal_prompt(db: Session, user):
    amount = click.prompt("Enter the withdrawal amount:", type=float)
    try:
        transaction = Transaction.make_withdrawal(user, amount)
        db.add(transaction)
        db.commit()
        print(f"Withdrawal of {amount} successfully made.")
    except ValueError as e:
        print(str(e))

# Function to handle checking wallet balance prompt
def handle_check_balance_prompt(user):
    balance = Transaction.check_wallet_balance(user)
    print(f"Current wallet balance: {balance}")

# Function to handle the transaction prompt
def handle_transaction_prompt(db: Session, user):
    choice = click.prompt(
        "Choose a transaction option:\n"
        "1. Make a deposit\n"
        "2. Make a withdrawal\n"
        "3. Check wallet balance\n"
        "Enter the option number (1/2/3): ",
        type=click.Choice(['1', '2', '3'], case_sensitive=False)
    )

    if choice == '1':
        handle_deposit_prompt(db, user)
    elif choice == '2':
        handle_withdrawal_prompt(db, user)
    elif choice == '3':
        handle_check_balance_prompt(user)
    else:
        print("Invalid choice. Please select a valid option (1/2/3).")

# Function to create a transaction with prompts
def create_transaction_prompt():
    user_id = click.prompt('Enter User ID', type=int)
    transaction_type = click.prompt(
        'Choose a transaction type:\n'
        '1. Deposit\n'
        '2. Withdrawal\n'
        '3. Check wallet balance\n'
        'Enter the transaction type (1/2/3): ',
        type=click.Choice(['1', '2', '3'], case_sensitive=False)
    )
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        db.close()
        print(f"User with ID {user_id} does not exist.")
        return

    if transaction_type == '1':
        amount = click.prompt("Enter the deposit amount:", type=float)
        try:
            transaction = Transaction.make_deposit(user, amount)
            db.add(transaction)
            db.commit()
            print(f"Deposit of {amount} successfully made.")
        except ValueError as e:
            print(str(e))
    elif transaction_type == '2':
        amount = click.prompt("Enter the withdrawal amount:", type=float)
        try:
            transaction = Transaction.make_withdrawal(user, amount)
            db.add(transaction)
            db.commit()
            print(f"Withdrawal of {amount} successfully made.")
        except ValueError as e:
            print(str(e))
    elif transaction_type == '3':
        balance = Transaction.check_wallet_balance(user)
        print(f"Current wallet balance: {balance}")
    else:
        print("Invalid transaction type. Please select a valid option (1/2/3).")

    db.close()


# List Transactions Command
@click.command("list-transactions")
def list_transactions_command():
    list_transactions()

# Function to list all transactions for a user
def list_transactions():
    user_id = click.prompt('Enter User ID', type=int)
    transactions = get_user_transactions(user_id)
    
    if transactions:
        print(f"Transactions for User ID {user_id}:")
        for transaction in transactions:
            print(f"ID: {transaction.id}, Type: {transaction.transaction_type}, Amount: {transaction.amount}")
    else:
        print(f"No transactions found for User ID {user_id}.")

# List Payment Providers Command
@click.command("list-payment-providers")
def list_payment_providers_command():
    list_payment_providers()

# Function to list all payment providers
def list_payment_providers():
    payment_providers = get_all_payment_providers()
    
    if payment_providers:
        print("List of Payment Providers:")
        for provider in payment_providers:
            print(f"ID: {provider.id}, Name: {provider.name}")
    else:
        print("No payment providers found.")

# List Currency Exchange Rates Command
@click.command("list-currency-exchange-rates")
def list_currency_exchange_rates_command():
    list_currency_exchange_rates()

# Function to list all currency exchange rates
def list_currency_exchange_rates():
    currency_exchange_rates = get_all_currency_exchange_rates()
    
    if currency_exchange_rates:
        print("List of Currency Exchange Rates:")
        for rate in currency_exchange_rates:
            print(f"ID: {rate.id}, Currency Pair: {rate.currency_pair}, Rate: {rate.exchange_rate}")
    else:
        print("No currency exchange rates found.")










# Function to exit the program
def exit_program():
    print("Exiting the program.")
    exit()

# Function to display the menu
def display_menu():
    os.system('clear')
    print("------------- M-Pesa Clone: Select an Option -------------")
    print("1. Create User")
    print("2. List Users")
    print("3. Create Wallet")
    print("4. List Wallets")
    print("5. Create Log")
    print("6. List Logs")
    print("7. Create Notification")
    print("8. List Notifications")
    print("11. Create Security Setting")
    print("12. List Security Settings")
    print("13. Create Transaction")
    print("14. List Transactions")
    print("15. List Payment Providers")
    print("16. List Currency Exchange Rates")
    print("0. Exit")

# Function to handle user choice
def handle_choice(choice):
    if choice == 1:
        create_user_command()
    elif choice == 2:
        list_users_command()
    elif choice == 3:
        create_wallet_command()
    elif choice == 4:
        list_wallets_command()
    elif choice == 5:
        create_log_command()
    elif choice == 6:
        list_logs_command()
    elif choice == 7:
        create_notification_command()
    elif choice == 8:
        list_notifications_command()
    elif choice == 11:
        create_security_setting_command()
    elif choice == 12:
        list_security_settings_command()
    elif choice == 13:
        create_transaction_command()
    elif choice == 14:
        list_transactions_command()
    elif choice == 15:
        list_payment_providers_command()
    elif choice == 16:
        list_currency_exchange_rates_command()
    elif choice == 0:
        exit_program()
    else:
        print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    while True:
        display_menu()
        
        while True:
            try:
                choice = int(input("Enter your choice (0-16): "))
                handle_choice(choice)
            except ValueError:
                print("Invalid input. Please enter a valid option.")
