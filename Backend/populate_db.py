import datetime
from neo4j_database import create_categories, create_user, get_db, delete_nodes
from app import app

with app.app_context():
    db = get_db()
    print("Clearing nodes")
    db.write_transaction(delete_nodes)
    print("Cleared nodes!")
    create_categories()
    print("Creating users...")
    user1 = db.write_transaction(create_user, "Admin", "Petkovic", "admin@analog.net", "123", "admin", "local")
    user2 = db.write_transaction(create_user, "Maksim", "Petkovic", "maksim@elfak.rs", "123", "staff", "local")
    user3 = db.write_transaction(create_user, "Ognjen", "Markovic", "ogi@elfak.rs", "123", "staff", "local")
    user4 = db.write_transaction(create_user, "Stefana", "Milosavljevic", "stefana@elfak.rs", "staff", "123", "local")
    user5 = db.write_transaction(create_user, "Dimitrije", "Eric", "dimi@elfak.rs", "123", "staff", "local")

    print("Created users!")

    print("Finished")