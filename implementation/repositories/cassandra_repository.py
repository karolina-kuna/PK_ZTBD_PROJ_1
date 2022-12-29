from cassandra.cluster import Cluster

class CassandraRepository:
    def __init__(self, keyspace, table):
        self.keyspace = keyspace
        self.table = table

        # Connect to the Cassandra cluster
        self.cluster = Cluster()
        self.session = self.cluster.connect(keyspace)

    def get_all(self):
        query = f"SELECT * FROM {self.table}"
        rows = self.session.execute(query)
        return rows

    def get_by_offer_id(self, offer_id):
        query = f"SELECT * FROM {self.table} WHERE offer_id = {offer_id}"
        rows = self.session.execute(query)
        return rows

    def insert(self, address_city, address_street, offer_id, title, price, area, owner_id, apartment_id):
        query = f"INSERT INTO {self.table} (address_city, address_street, offer_id, title, price, area, owner_id, apartment_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.session.execute(query, (address_city, address_street, offer_id, title, price, area, owner_id, apartment_id))

    def update(self, offer_id, new_title, new_price):
        query = f"UPDATE {self.table} SET title = %s, price = %s WHERE offer_id = %s"
        self.session.execute(query, (new_title, new_price, offer_id))

# Example usage
repository = CassandraRepository("mykeyspace", "offers")

# Get all rows
rows = repository.get_all()

# Get a single row by offer_id
offer_id = 123
row = repository.get_by_offer_id(offer_id)

# Insert a new row
repository.insert("New York", "123 Main St", 456, "New Offer", 1000, 500, 1, 2)

# Update an existing row
repository.update(offer_id, "Updated Offer", 1500)