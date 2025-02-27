import streamlit as st
import openai
import config 
import summarize
import slide
import imagegen
# Set your OpenAI API key here
openai.api_key = config.api_key
sections = []
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript

    except Exception as e:
        return f"Error: {str(e)}"

# Set the title and description of your app
st.title("Lecturey")

# Create a file uploader widget that accepts both audio and video file types
uploaded_file = st.file_uploader("Upload a video or audio file to transcribe.", type=["mp3", "wav", "ogg", "mp4", "avi", "mov"])

# Check if a file was uploaded
if uploaded_file is not None:
    
    # Determine if the uploaded file is an audio or video based on the file extension
    file_extension = uploaded_file.type.split("/")[-1]

    if file_extension in ["mp3", "wav", "ogg", "mp4", "avi", "mov"]:
        
        # Display the file type
        st.write(f"Uploaded {file_extension} file")
        
        # Provide an option to upload a text file for transcription
        #txt_file = st.file_uploader("Upload a text file to get transcription", type=["txt"])
        #if txt_file is not None:
            # Perform audio to text transcription using OpenAI convertion 
        transcription = convert_audio_to_text(uploaded_file)
        transcription = str(transcription)
        #print(transcription)
        #st.write(transcription)
        notes = summarize.getNotes(transcription)
        #st.write(summarize.getNotes(transcription))
        sections = imagegen.getkeyword(notes)
        #st.write(imagegen.getkeyword(notes))

    else:
        st.write("Unsupported file format. Please upload an audio or video file.")
else:
    st.write("Please upload a file.")
for x in sections:
    
        response = openai.Completion.create(
      engine="text-davinci-002",  # Use the appropriate engine.
      prompt="Be more detailed with the following, give examples: " + x,
      max_tokens=500,
      temperature=0.3,
  )
        st.write(response['choices'][0]['text'])
        #st.write(x)
        st.image(str(imagegen.getImage(imagegen.makeOneWord(x))), caption="Image from URL", use_column_width=True)