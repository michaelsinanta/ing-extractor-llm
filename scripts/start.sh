poetry install
# poetry run python main.py
PORT=$(grep -m 1 '^PORT=' .env | cut -d '=' -f2)
echo "PORT: $PORT"
poetry run streamlit run streamlit.py --server.port=$PORT