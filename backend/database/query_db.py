import pandas as pd
from tabulate import tabulate
from sqlalchemy import create_engine

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

# Show table stats
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

