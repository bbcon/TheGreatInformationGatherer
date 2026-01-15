"""
Audio transcription module using Whisper
"""

import logging
import os
from pathlib import Path


class Transcriber:
    """Transcribes audio using OpenAI Whisper"""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.transcription_config = config['transcription']
        
        # Initialize Whisper model
        self.use_api = self.transcription_config.get('use_api', False)
        
        if self.use_api:
            import openai
            self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        else:
            import whisper
            model_name = self.transcription_config.get('model', 'base')
            self.logger.info(f"Loading Whisper model: {model_name}")
            self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file
        Returns transcript text
        """
        self.logger.info(f"Transcribing audio: {audio_path}")
        
        if self.use_api:
            return self._transcribe_with_api(audio_path)
        else:
            return self._transcribe_local(audio_path)
    
    def _transcribe_local(self, audio_path):
        """Transcribe using local Whisper model"""
        try:
            result = self.model.transcribe(
                audio_path,
                language=self.transcription_config.get('language', 'en'),
                verbose=False
            )
            
            transcript = result['text'].strip()
            self.logger.info(f"Transcription complete: {len(transcript)} characters")
            
            return transcript
            
        except Exception as e:
            self.logger.error(f"Local transcription error: {str(e)}")
            raise
    
    def _transcribe_with_api(self, audio_path):
        """Transcribe using OpenAI Whisper API"""
        try:
            with open(audio_path, 'rb') as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=self.transcription_config.get('language', 'en')
                )
            
            text = transcript.text.strip()
            self.logger.info(f"API transcription complete: {len(text)} characters")
            
            return text
            
        except Exception as e:
            self.logger.error(f"API transcription error: {str(e)}")
            raise
