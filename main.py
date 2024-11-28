from fastapi import FastAPI, HTTPException, BackgroundTasks # type: ignore
from fastapi.responses import StreamingResponse, FileResponse # type: ignore
from pydantic import BaseModel, Field # type: ignore
import edge_tts # type: ignore
import tempfile # type: ignore
import os # type: ignore

# Initialize FastAPI app
app = FastAPI()

# Request model to handle inputs
class TTSRequest(BaseModel):
    message: str = Field(..., description="The text to synthesize.")
    voice: str = Field(..., description="The name of the TTS voice.")
    rate: str = Field(None, description="Speech speed (e.g., '-50%').")
    volume: str = Field(None, description="Speech volume (e.g., '-50%').")

# /edgetts/gen endpoint: Generate TTS and return audio file
@app.post("/edgetts/gen")
async def generate_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    """
    Generate a voice TTS response directly from the input text.
    """
    try:
        # Prepare arguments for the TTS communicate
        kwargs = {"text": request.message, "voice": request.voice}
        
        # Ensure rate and volume are passed as strings
        if request.rate is not None:
            kwargs["rate"] = str(request.rate)  # Ensure it's a string
        if request.volume is not None:
            kwargs["volume"] = str(request.volume)  # Ensure it's a string

        # Temporary file to store audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            output_file_path = temp_audio_file.name

        # Initialize Edge TTS and generate the audio
        communicate = edge_tts.Communicate(**kwargs)
        await communicate.save(output_file_path)

        # Validate the file
        if not os.path.exists(output_file_path) or os.path.getsize(output_file_path) == 0:
            raise HTTPException(status_code=500, detail="Failed to generate valid TTS output.")

        # Schedule file cleanup and return response
        background_tasks.add_task(os.remove, output_file_path)
        return FileResponse(
            output_file_path,
            media_type="audio/mpeg",
            filename="output.mp3",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating TTS: {str(e)}")


# /edgetts/stream endpoint: Stream TTS audio directly
@app.post("/edgetts/stream")
async def stream_tts(request: TTSRequest):
    """
    Stream a voice TTS response directly from the input text.
    """
    try:
        # Prepare arguments for the TTS communicate
        kwargs = {"text": request.message, "voice": request.voice}
        
        # Ensure rate and volume are passed as strings
        if request.rate is not None:
            kwargs["rate"] = str(request.rate)  # Ensure it's a string
        if request.volume is not None:
            kwargs["volume"] = str(request.volume)  # Ensure it's a string

        # Initialize TTS communicator
        communicate = edge_tts.Communicate(**kwargs)

        # Define generator function to stream audio chunks
        async def audio_generator():
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]  # Stream audio data

        # Stream audio only
        return StreamingResponse(audio_generator(), media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming TTS: {str(e)}")


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=5500)
