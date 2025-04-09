import json
import qbconnection


def query_records(self, table_id, query):
        """Execute a query on a Quickbase table"""
        endpoint = f"{self.base_url}/records/query"
        
        payload = {
            "from": table_id,
            "select": query
        }
        return self.make_request(endpoint,payload)
    
def query_app_for_tables():
#this will call the api call that is used to get all tables from API Portal
    return []

def get_Schema(dbid):
#This will call the API_GetSchema call
#Used for checking for Mixed encoding/getting a full look at what is found Returns XML usually
    return []

# Example usage
if __name__ == "__main__":
    # Replace these with your actual credentials
    REALM = "your-realm.quickbase.com"
    USER_TOKEN = "your-user-token"
    APP_TOKEN = "your-app-token"
    
    # Initialize the API client
    qb = qbconnection.QuickbaseAPI(REALM, USER_TOKEN, APP_TOKEN)
    
    # Example query
    TABLE_ID = "bqxxxxx"  # Replace with your table ID
    QUERY = [1, 2, 3]  # Replace with your field IDs
    
    try:
        result = qb.query_records(TABLE_ID, QUERY)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}") 