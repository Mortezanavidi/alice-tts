# Alice-tts

**Alice-TTS** is a text-to-speech (TTS) module of the **AliceAI** project,
Alice-TTS has many modules inside itself but as of now, it's only leveraging the **Edge TTS** engine. It provides RESTful APIs to generate and stream TTS audio with customizable parameters like speech rate and volume.

## Features

- **Generate TTS Audio**: Convert text to speech and return the audio file.
- **Stream TTS Audio**: Stream the TTS audio in real-time.
- **Customizable Speech**: Adjust speech rate and volume (e.g., `"-50%"`, `"+20%"`).

## API Endpoints

### 1. **Generate TTS (POST `/edgetts/gen`)**
Convert text to speech and download the audio.

#### Example Request:
```bash
curl -X POST "http://localhost:5500/edgetts/gen" \
-H "Content-Type: application/json" \
-d '{"message": "Hello World!", "voice": "en-GB-SoniaNeural"}' \
--output output.mp3
```

### 2. **Stream TTS (POST `/edgetts/stream`)**
Stream TTS audio without downloading the full file.

#### Example Request:
```bash
curl -X POST "http://localhost:5500/edgetts/stream" \
-H "Content-Type: application/json" \
-d '{"message": "Hello World!", "voice": "en-GB-SoniaNeural"}' \
--output output.mp3
```

#### Optional Parameters
- `rate`: Speed adjustment (e.g., `"-50%"`, `"+20%"`).
- `volume`: Volume adjustment (e.g., `"-50%"`, `"+20%"`).

## Installation

### With Docker

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/alice-tts.git
   cd alice-tts
   ```

2. **Build and run**:
   ```bash|
   cd docker
   docker-compose up --build
   ```

3. **Access**: The API will be available at `http://localhost:5500`.

### Without Docker

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python main.py
   ```

3. **Access**: The API will be available at `http://localhost:5500`.