📒 Notes Manager App
A simple and efficient Notes Management web application built using FastAPI, MongoDB, and HTML/CSS/JS.
This app allows users to upload, view, search, and download notes easily.

🚀 Features


📤 Upload notes with file support


📂 Store files directly in database (MongoDB)


📄 View all uploaded notes


🔍 Search notes by title or subject


⬇️ Download uploaded files


🌐 Simple and responsive UI



🛠️ Tech Stack


Backend: FastAPI


Database: MongoDB


Frontend: HTML, CSS, JavaScript


Server: Uvicorn


⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/notes-app.gitcd notes-app

2️⃣ Create virtual environment
python -m venv venv
Activate it:


Windows:


venv\Scripts\activate


Mac/Linux:


source venv/bin/activate

3️⃣ Install dependencies
pip install fastapi uvicorn pymongo python-multipart

4️⃣ Setup MongoDB
Update your database.py with your MongoDB URL:
MONGO_URL = "your_mongodb_connection_string"

5️⃣ Run the app
uvicorn main:app --reload

6️⃣ Open in browser
http://127.0.0.1:8000

📌 API Endpoints
MethodEndpointDescriptionPOST/uploadUpload a noteGET/notesGet all notesGET/download/{id}Download note file

🔍 Search Functionality


Search notes by:


Title


Subject




Implemented on frontend using JavaScript filtering



📸 UI Preview


Clean list of notes


Search bar on top


Download button for each note



💡 Future Improvements


User authentication (login/signup)


Edit & delete notes


Cloud file storage (AWS / Firebase)


Pagination for large data


Tag-based filtering



🤝 Contributing
Feel free to fork this repo and improve the project. Pull requests are welcome!

📄 License
This project is open-source and available under the MIT License.

If you want, I can also:


Customize this README with your GitHub username


Add screenshots section


Or generate a perfect project description for resume 👍

