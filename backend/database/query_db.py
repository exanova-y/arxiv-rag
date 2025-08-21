import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, text


db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Create SQLAlchemy engine
engine = create_engine(db_url)

# section 1: paper storage
# Query first 5 rows with all original columns
query = """
SELECT 
    id,
    text,
    metadata_,
    node_id,
    LEFT(embedding::text, 50) as embedding_preview
FROM data_arxiv_papers 
LIMIT 5;
"""

df = pd.read_sql_query(query, engine)
print("PostgreSQL Table: data_arxiv_papers (First 5 rows)")
print("=" * 120)
print(tabulate(df, headers='keys', tablefmt='grid', showindex=False, 
               maxcolwidths=[4, 60, 40, 36, 30]))

# Function to remove last 50 rows (data science duplicates)
def remove_last_50_rows():
    delete_query = """
    DELETE FROM data_arxiv_papers 
    WHERE id IN (
        SELECT id FROM data_arxiv_papers 
        ORDER BY id DESC 
        LIMIT 50
    );
    """
    
    with engine.connect() as conn:
        result = conn.execute(text(delete_query))
        conn.commit()
        print(f"Deleted {result.rowcount} rows (last 50 entries)")

# Uncomment to remove duplicates:
# remove_last_50_rows()

# Show table stats for papers
stats_query = """
SELECT 
    COUNT(*) as total_rows,
    COUNT(DISTINCT metadata_->>'file_name') as unique_files,
    AVG(LENGTH(text))::int as avg_text_length,
    MIN(LENGTH(text)) as min_text_length,
    MAX(LENGTH(text)) as max_text_length
FROM data_arxiv_papers;
"""

stats_df = pd.read_sql_query(stats_query, engine)
print("Table Statistics:")
print("=" * 40)
print(tabulate(stats_df, headers='keys', tablefmt='fancy_grid', showindex=False))



# section 2: chat storage
# LlamaIndex PostgresChatStore
chat_table = "data_chatstore"
print(f"postgres chatstore table: {chat_table}")

# table stats
stats_chat_df = pd.read_sql_query(
    """
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT key) AS distinct_keys,
        MIN(id) AS min_id,
        MAX(id) AS max_id
    FROM data_chatstore;
    """,
    engine,
)
print("Table Statistics (chat):")
print(tabulate(stats_chat_df, headers='keys', tablefmt='fancy_grid', showindex=False))

# display a specific row (id=1) with all columns
row1_df = pd.read_sql_query(
    """
    SELECT *
    FROM data_chatstore
    WHERE id = 1;
    """,
    engine,
)
if not row1_df.empty:
    print("\nSingle row (id=1):")
    print(tabulate(row1_df, headers='keys', tablefmt='grid', showindex=False, maxcolwidths=[12, 24, 120]))
