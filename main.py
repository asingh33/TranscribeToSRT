import io
import os

from transcribe import transcribe_gcs

lang = "hi-IN" 
uri = "gs://{PATH_TO_YOUR_FILE_IN_GOOGLE_BUCKET}.mp3"

creds = "{PATH_TO_YOUR_ACCOUNT_CREDENTIAL}.json"
data = transcribe_gcs(uri, lang, creds)





