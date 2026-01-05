# AI-Driven Communication Surveillance

This project uses Streamlit, Azure OpenAI, and NLP to analyze email communications for compliance risks.

## Structure

- `app/` – Streamlit UI and main logic
- `services/` – LLM and Azure/OpenAI logic
- `utils/` – Utility functions (text cleaning, etc.)
- `config/` – Environment and Azure client setup
- `requirements.txt` – Dependencies

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up your `.env` file with Azure OpenAI credentials in the root directory.
   
   Example `.env` file:
   ```env
   AZURE_OPENAI_KEY=your-azure-openai-key
   AZURE_OPENAI_API_VERSION=2023-05-15
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   ```
3. Run the app:
   ```bash
   streamlit run app/main.py
   ```

Upload an Excel file with columns: From, To, Subject, Body (max 50 rows).

### Example Input Excel
| From         | To           | Subject         | Body                |
|--------------|--------------|-----------------|---------------------|
| alice@a.com  | bob@b.com    | Compliance Test | Please review...    |

---

Developed with Streamlit, Azure OpenAI, and NLTK.