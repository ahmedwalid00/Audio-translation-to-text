import openai
from dotenv import load_dotenv 
import os 
from flask import Flask , request , jsonify , render_template

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

myapp = Flask(__name__)
myapp.config["UPLOAD_FOLDER"] = "static"

@myapp.route("/" , methods=['GET','POST'])
def main():
    if request.method == 'POST' : 
        language = request.form["language"]
        file = request.files["file"]
        if file:
            file_name = file.filename
            file.save(os.path.join(myapp.config["UPLOAD_FOLDER"], file_name))

            audio_recored = open("static/Recording.mp3" ,"rb")
            transcibt = openai.Audio.translate("whisper-1" , audio_recored)

            response = openai.ChatCompletion.create(
                model = "gpt-4" , 
                messages = [
                    {"role" : "system" , "content" : f"You will be provided with a sentence in English, and your task is to translate it into {language}"} ,
                    {"role" : "user" , "content" : transcibt.text}
                ] , 
                temperature = 0 ,
                max_tokens = 256
            )
            translated_text = response["choices"][0]["message"]["content"]
            return translated_text

    return render_template("index.html")

if __name__ == "__main__" :
    myapp.run(host="0.0.0.0",debug=True , port=8080)


