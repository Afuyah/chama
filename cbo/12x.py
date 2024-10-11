from app import create_app, db
from app.models import Member, Role
from werkzeug.security import generate_password_hash
import getpass

app = create_app()

def create_roles_if_not_exist():
    with app.app_context():
        db.create_all()
        
        roles = ["chairman", "secretary", "treasurer", "organizing_sec", "member_rep"]
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                new_role = Role(name=role_name)
                db.session.add(new_role)
                print(f"Created role: {role_name}")
        
        db.session.commit()

def create_member():
    with app.app_context():
        db.create_all()

        # Role input
        role_name = input("Enter the role for this member (chairman/secretary/treasurer/organizing_sec/member_rep): ").lower()
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            print("Invalid role. Please enter a valid role.")
            return

        # Collect Member information
        phone_number = input("Enter phone number: ")
        if Member.query.filter_by(phone_number=phone_number).first():
            print("Member with this phone number already exists.")
            return

        name = input("Enter name: ")
        residence = input("Enter residence: ")
        county = input("Enter county: ")
        gender = input("Enter gender: ")

        # Validate age input
        try:
            age = int(input("Enter age: "))
            if age <= 0:
                print("Age must be a positive integer.")
                return
        except ValueError:
            print("Invalid input for age. Please enter a number.")
            return

        password = getpass.getpass('Enter a secure password for the member: ')
        confirm_password = getpass.getpass('Confirm the password: ')

        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            return

        # Create a new Member
        new_member = Member(
            phone_number=phone_number,
            password_hash=generate_password_hash(password),  # Hash the password for Member
            name=name,
            residence=residence,
            county=county,
            gender=gender,
            age=age,
            role_id=role.id  # Link Member to Role using role_id
        )

        try:
            db.session.add(new_member)
            db.session.commit()  # Commit to finalize the new Member creation
            print("Member created successfully.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"An error occurred while creating the member: {e}")

if __name__ == '__main__':
    create_roles_if_not_exist()
    create_member()
