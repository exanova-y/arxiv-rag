import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine, text

# Create SQLAlchemy engine
engine = create_engine("postgresql://postgres:password@localhost:5432/arxiv_rag")

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
print("\nTable Statistics:")
print("=" * 40)
print(tabulate(stats_df, headers='keys', tablefmt='fancy_grid', showindex=False))

# use %% to fix immutable data type error from sqlalchemy
chat_table_check_query = """
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE '%%chat%%'; 
"""

tables_df = pd.read_sql_query(chat_table_check_query, engine)
tables_df.columns = tables_df.columns.astype(str)
print("Chat tables found:")
print(tabulate(tables_df, headers='keys', tablefmt='grid', showindex=False))

for table_name in tables_df['table_name']:
    print(f"\n--- {table_name.upper()} ---")
    chat_query = f"SELECT * FROM {table_name} LIMIT 5;"
    chat_df = pd.read_sql_query(chat_query, engine)
    if not chat_df.empty:
        print(tabulate(chat_df, headers='keys', tablefmt='grid', showindex=False))
    else:
        print("No data in table")
        
   