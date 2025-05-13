<table border="0" style="border: none; border-collapse: collapse;">
  <tr>
    <td align="left" valign="top" width="480" padding="0" border="none" border-collapse="collapse">
      <img
        src="https://github.com/siddiq0611/git_repo/blob/main/kalpkatha.png"
        alt="Kalpkatha Logo"
        width="480"
        align="center"
      />
    </td>
    <td align="left" valign="top">
      <h1 align="center">Kalpkatha</h1>
      <h3>
        This is a FastAPI-based backend service that generates creative stories using
        OpenAI's GPT models. Provide a prompt, and the API will return an engaging,
        structured tale with rich characters, world-building, and plot development.
      </h3>
    </td>
  </tr>
</table>




## 🌐 Live API

The service is hosted and running.  
You can test the API at: [kalpkatha_backend](https://kalpkatha-backend.onrender.com)


## 🧠 Features

- ✨ AI-powered story generation using OpenAI GPT
- 🧩 Modular and extensible FastAPI architecture
- ⚙️ Environment-based configuration
- 🔐 API key protected (via `.env`)
- 🔄 CORS enabled for frontend integration
- 📖 Smart story structure (Three-act arc, character depth, dialogue)


## 📂 Project Structure

```bash
backend/
├── app.py             # FastAPI application
├── config.py          # Pydantic-based config management
├── story_writer.py    # Story generation logic
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (not committed)
├── __pycache__/       # Python cache files
└── env/               # Virtual environment (excluded)
```


## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/siddiq0611/kalpkatha_backend.git
```
### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env\Scripts\activate        # For Linux and macOS: env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key
DEBUG=true
MODEL_NAME=gpt-4o
DEFAULT_TEMPERATURE=0.7
```

## 🧪 API Endpoints
### ✅ Health Check
GET /health

Returns:
```json
{
"status": "healthy"
}
```

## ✨ Generate a Story
POST /api/generate-story

Request Body
```json
{
  "prompt": "Once upon a time in a galaxy far away..."
}
```

Response
```json
{
  "prompt_used": "Once upon a time in a galaxy far away...",
  "story": "In the swirling violet sky of the Andromeda Cluster, a young star-sailor named Lyra..."
}
```

## 🛠 Technologies Used

- **FastAPI**  
- **OpenAI Python SDK**  
- **Pydantic & pydantic-settings**  
- **Uvicorn**  


## 🔐 Security Notes

- Keep your `.env` file private and never commit it to version control.
- Limit CORS origins to trusted sources in production (`app.py`).
- Use HTTPS in production to secure your API key in transit.


## 📌 To-Do / Enhancements

- [ ] Add genre or length customization to prompts  
- [ ] User authentication & history saving  
- [ ] Docker support for containerized deployment  
- [ ] Frontend integration (React, Vue, etc.)


## 📜 License

MIT License © [siddiq0611]


## 🙌 Acknowledgements

- Thanks to [OpenAI](https://openai.com/) for the API  
- Inspired by a love for storytelling, coding, and imagination.
