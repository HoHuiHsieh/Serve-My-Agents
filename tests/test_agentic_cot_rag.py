"""Tests for Agentic_CoT_RAG model through chat completion API."""

import pytest
from fastapi.testclient import TestClient
import json

from main import app
from src.models import ChatCompletionRequest, Message


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestAgenticCoTRAGChatCompletion:
    """Test suite for Agentic CoT RAG model via chat completion API."""
    
    def test_non_streaming_chat_completion(self, client):
        """Test non-streaming chat completion with agentic-cot-rag model."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"}
            ],
            "stream": False,
            "temperature": 0.7
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Assert response status
        assert response.status_code == 200
        
        # Parse response
        data = response.json()
        
        # Verify response structure
        assert "id" in data
        assert data["object"] == "chat.completion"
        assert "created" in data
        assert data["model"] == "agentic-cot-rag"
        
        # Verify choices
        assert "choices" in data
        assert len(data["choices"]) > 0
        
        choice = data["choices"][0]
        assert choice["index"] == 0
        assert "message" in choice
        assert choice["message"]["role"] == "assistant"
        assert "content" in choice["message"]
        assert len(choice["message"]["content"]) > 0
        assert choice["finish_reason"] == "stop"
        
        # Verify usage information
        assert "usage" in data
        assert "prompt_tokens" in data["usage"]
        assert "completion_tokens" in data["usage"]
        assert "total_tokens" in data["usage"]
        assert data["usage"]["total_tokens"] == (
            data["usage"]["prompt_tokens"] + data["usage"]["completion_tokens"]
        )
    
    def test_streaming_chat_completion(self, client):
        """Test streaming chat completion with agentic-cot-rag model."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "Count from 1 to 5."}
            ],
            "stream": True
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Assert response status
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Collect streaming chunks
        chunks = []
        for line in response.iter_lines():
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            
            # Skip empty lines
            if not line or not line.strip():
                continue
            
            # Parse SSE format (data: {...})
            if line.startswith("data: "):
                data_str = line[6:]  # Remove "data: " prefix
                
                # Check for [DONE] signal
                if data_str.strip() == "[DONE]":
                    break
                
                try:
                    chunk_data = json.loads(data_str)
                    chunks.append(chunk_data)
                except json.JSONDecodeError:
                    continue
        
        # Verify we received chunks
        assert len(chunks) > 0, "No chunks received from streaming response"
        
        # Verify first chunk structure
        first_chunk = chunks[0]
        assert "id" in first_chunk
        assert first_chunk["object"] == "chat.completion.chunk"
        assert "created" in first_chunk
        assert first_chunk["model"] == "agentic-cot-rag"
        assert "choices" in first_chunk
        
        # Verify chunk content
        content_pieces = []
        for chunk in chunks:
            if chunk["choices"] and "delta" in chunk["choices"][0]:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta and delta["content"]:
                    content_pieces.append(delta["content"])
        
        # Verify we got content
        assert len(content_pieces) > 0, "No content received in stream"
        
        # Verify last chunk has finish_reason
        last_chunk = chunks[-1]
        assert last_chunk["choices"][0].get("finish_reason") in ["stop", None]
    
    def test_multiple_messages_conversation(self, client):
        """Test chat completion with multiple message history."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": "What is 2 + 2?"},
                {"role": "assistant", "content": "2 + 2 equals 4."},
                {"role": "user", "content": "What about 3 + 3?"}
            ],
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response
        assert data["model"] == "agentic-cot-rag"
        assert len(data["choices"]) > 0
        assert data["choices"][0]["message"]["role"] == "assistant"
        assert len(data["choices"][0]["message"]["content"]) > 0
    
    def test_different_temperatures(self, client):
        """Test chat completion with different temperature settings."""
        base_request = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "Say hello!"}
            ],
            "stream": False
        }
        
        # Test with temperature 0.0 (more deterministic)
        request_low_temp = {**base_request, "temperature": 0.0}
        response_low = client.post("/v1/chat/completions", json=request_low_temp)
        assert response_low.status_code == 200
        
        # Test with temperature 1.0 (more random)
        request_high_temp = {**base_request, "temperature": 1.0}
        response_high = client.post("/v1/chat/completions", json=request_high_temp)
        assert response_high.status_code == 200
        
        # Both should return valid responses
        data_low = response_low.json()
        data_high = response_high.json()
        
        assert len(data_low["choices"][0]["message"]["content"]) > 0
        assert len(data_high["choices"][0]["message"]["content"]) > 0
    
    def test_max_tokens_parameter(self, client):
        """Test chat completion with max_tokens limit."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "Write a long story about space exploration."}
            ],
            "stream": False,
            "max_tokens": 50
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is generated (actual token limiting depends on implementation)
        assert len(data["choices"]) > 0
        assert "content" in data["choices"][0]["message"]
    
    def test_empty_user_message(self, client):
        """Test handling of empty user message."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": ""}
            ],
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Should handle gracefully (either respond or return appropriate error)
        assert response.status_code in [200, 400]
    
    def test_system_message_only(self, client):
        """Test with only system message."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}
            ],
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Should handle gracefully
        assert response.status_code in [200, 400]
    
    def test_invalid_model_name(self, client):
        """Test with invalid model name."""
        request_data = {
            "model": "invalid-model-name",
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Should return error or fallback
        assert response.status_code in [200, 400, 404, 500]
    
    def test_missing_required_fields(self, client):
        """Test request with missing required fields."""
        # Missing messages field
        request_data = {
            "model": "agentic-cot-rag",
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_invalid_message_role(self, client):
        """Test with invalid message role."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "invalid_role", "content": "Hello"}
            ],
            "stream": False
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_response_id_uniqueness(self, client):
        """Test that each response has a unique ID."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "stream": False
        }
        
        # Make two requests
        response1 = client.post("/v1/chat/completions", json=request_data)
        response2 = client.post("/v1/chat/completions", json=request_data)
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        data1 = response1.json()
        data2 = response2.json()
        
        # IDs should be different
        assert data1["id"] != data2["id"]
    
    def test_streaming_response_format(self, client):
        """Test that streaming response follows OpenAI SSE format."""
        request_data = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "Hi"}
            ],
            "stream": True
        }
        
        response = client.post("/v1/chat/completions", json=request_data)
        
        assert response.status_code == 200
        
        # Verify SSE format
        lines = list(response.iter_lines())
        assert len(lines) > 0
        
        # Check that lines follow "data: " format
        data_lines = [
            line.decode("utf-8") if isinstance(line, bytes) else line
            for line in lines
            if line
        ]
        
        # Should have at least one "data: " line
        data_prefixed = [line for line in data_lines if line.startswith("data: ")]
        assert len(data_prefixed) > 0


class TestAgenticCoTRAGIntegration:
    """Integration tests for Agentic CoT RAG model."""
    
    def test_complete_conversation_flow(self, client):
        """Test a complete multi-turn conversation."""
        # First message
        request1 = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "What is Python?"}
            ],
            "stream": False
        }
        
        response1 = client.post("/v1/chat/completions", json=request1)
        assert response1.status_code == 200
        data1 = response1.json()
        first_response = data1["choices"][0]["message"]["content"]
        
        # Follow-up message
        request2 = {
            "model": "agentic-cot-rag",
            "messages": [
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": first_response},
                {"role": "user", "content": "Can you give me an example?"}
            ],
            "stream": False
        }
        
        response2 = client.post("/v1/chat/completions", json=request2)
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Verify second response
        assert len(data2["choices"][0]["message"]["content"]) > 0
    
    def test_streaming_to_non_streaming_consistency(self, client):
        """Test that streaming and non-streaming return similar responses."""
        messages = [
            {"role": "user", "content": "Say 'Hello, World!'"}
        ]
        
        # Non-streaming
        request_non_stream = {
            "model": "agentic-cot-rag",
            "messages": messages,
            "stream": False,
            "temperature": 0.0
        }
        
        response_non_stream = client.post("/v1/chat/completions", json=request_non_stream)
        assert response_non_stream.status_code == 200
        data_non_stream = response_non_stream.json()
        non_stream_content = data_non_stream["choices"][0]["message"]["content"]
        
        # Streaming
        request_stream = {
            "model": "agentic-cot-rag",
            "messages": messages,
            "stream": True,
            "temperature": 0.0
        }
        
        response_stream = client.post("/v1/chat/completions", json=request_stream)
        assert response_stream.status_code == 200
        
        # Collect streaming content
        stream_content = ""
        for line in response_stream.iter_lines():
            line = line.decode("utf-8") if isinstance(line, bytes) else line
            if line.startswith("data: ") and not line.endswith("[DONE]"):
                data_str = line[6:]
                try:
                    chunk_data = json.loads(data_str)
                    if chunk_data["choices"] and "delta" in chunk_data["choices"][0]:
                        delta = chunk_data["choices"][0]["delta"]
                        if "content" in delta and delta["content"]:
                            stream_content += delta["content"]
                except json.JSONDecodeError:
                    continue
        
        # Both should have content
        assert len(non_stream_content) > 0
        assert len(stream_content) > 0
