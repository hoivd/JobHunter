from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# load biến môi trường từ .env
load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# tạo driver kết nối
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def close_driver():
    driver.close()
    print("Driver Neo4j đã được đóng.")
