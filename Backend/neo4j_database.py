from asyncio.trsock import TransportSocket
import datetime
from tokenize import Number
import uuid
from neo4j import GraphDatabase, Session, Transaction, basic_auth
from flask import g
from passlib.hash import sha256_crypt

DATABASE_USERNAME = "neo4j"
DATABASE_PASSWORD = "Asdfg@123#"
DATABASE_URL = "bolt://localhost:7687"

driver = GraphDatabase.driver(
    DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD))
)

def get_db() -> Session:
    if not hasattr(g, "neo4j_db"):
        g.neo4j_db = driver.session()
    return g.neo4j_db

def close_db(error):
    if hasattr(g, "neo4j_db"):
        g.neo4j_db.close()

def create_user(tx: Transaction, name: str, lastname: str, email: str, password: str, role: str, provider: str):
    return tx.run(
        """
        CREATE (user:User {id: $id, name: $name, lastname: $lastname, email: $email, password: $password, role: $role, provider: $provider}) RETURN user
        """,
        {
            "id": str(uuid.uuid4()),
            "name": name,
            "lastname": lastname,
            "email": email,
            "password": sha256_crypt.hash(password),
            "role": role,
            "provider": provider,
        },
    ).single()

def check_password(user, password):
    if sha256_crypt.verify(password, user["password"]):
        return 1
    else:
        return 0
    
def get_user_by_email(tx: Transaction, email: str):
    return tx.run(
        """
        MATCH (user:User {email: $email})
        RETURN user
        """,
        {"email": email},
    ).single()

def get_user_by_id(tx: Transaction, user_id: str):
    return tx.run(
        """
        MATCH (user:User {id: $user_id})
        RETURN user
        """,
        { "user_id": user_id },
    ).single()

def delete_nodes(tx: Transaction):
    return tx.run(
        """
        MATCH (n)
        DETACH DELETE n
        """
    ).single()

def create_stories(tx: Transaction):
    return tx.run(
        """
        """
    ).single()

def get_stories(tx: Transaction):
    return tx.run(
        """
        """
    ).single()

def create_category(tx: Transaction, category_name: str):
    return tx.run(
        """
        CREATE (category:Category {id: $id, name: $name})
        RETURN category
        """,
        {"id": str(uuid.uuid4()), "name": category_name}
    ).single()

def create_categories():
    db = get_db()

    db.write_transaction(create_category, "Sports")
    db.write_transaction(create_category, "Documents")
    db.write_transaction(create_category, "Ideas")
    db.write_transaction(create_category, "Other")

def get_categories(tx: Transaction):
    return tx.run(
        """
        MATCH (category:Category)
        RETURN category
        """
    ).data()

def category(category):
    return {"id": category["id"], "name": category["name"]}
def serialize_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "lastname": user["lastname"],
        "email": user["email"],
        "role": user["role"],
        "provider": user["provider"],
    }
def serialize_category(category):
    return {
        "id": category["id"],
        "name": category["name"],
    }
def serialize_blog_form(blog):
    return {
        "title": blog["title"],
        "text": blog["text"]
    }
def serialize_blog(blog):
    return {
        "blog": serialize_blog_form(blog["blog"]),
        "user": serialize_user(blog["user"]),
        "category": serialize_category(blog["category"])
    }

def db_create_blog(tx: Transaction, title: str, text: str, timestamp: datetime):
    return tx.run(
        """
            CREATE (blog: Blog {id:$id, title:$title, text:$text, timestamp:$timestamp})
            return blog
        """,
        {"id": str(uuid.uuid4()), "title": title, "text": text, "timestamp": timestamp},
    ).single()

def db_add_blog_to_user(tx: Transaction, user_id: str, blog_id: str):
    return tx.run(
        """
            MATCH (user:User {id:$user_id}),(blog:Blog {id:$blog_id})
            MERGE (user)-[:WROTE]->(blog)
            return user
        """,
        {"user_id": user_id, "blog_id": blog_id},
    )

def db_add_category_to_blog(tx: Transaction, blog_id: str, category_id: str):
    return tx.run(
        """
            MATCH (blog:Blog {id:$blog_id}),(category:Category {id:$category_id})
            MERGE (blog)-[:IN_CATEGORY]->(category)
            RETURN blog
        """,
        {"blog_id": blog_id, "category_id": category_id},
    ).single()

def db_get_blogs(tx: Transaction):
    return tx.run(
        """
        MATCH (user:User)-[wr:WROTE]-(blog:Blog)-[:IN_CATEGORY]-(category:Category)
        RETURN blog, user, category
        ORDER BY blog.timestamp DESC
        """
    ).data()

def db_get_blogs_by_category(tx: Transaction, category_id: str):
    return tx.run(
        """
        MATCH (user:User)-[wr:WROTE]-(blog:Blog)-[:IN_CATEGORY]-(category:Category {id:$category_id})
        RETURN blog, user, category
        ORDER BY blog.timestamp DESC
        """,
        {"category_id": category_id},
    ).data()