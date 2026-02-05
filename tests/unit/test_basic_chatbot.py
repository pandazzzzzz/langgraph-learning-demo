"""
Unit tests for the basic chatbot example.

These tests verify that the basic chatbot functionality works correctly
and serves as an example of how to test LangGraph applications.
"""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage

from src.examples.basic_chatbot import (
    ChatState,
    chatbot_node,
    create_chatbot_graph,
)


class TestChatbotNode:
    """Test cases for the chatbot node function."""
    
    def test_chatbot_node_with_user_input(self):
        """Test that chatbot node processes user input correctly."""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.content = "Hello! How can I help you?"
        
        with patch('src.examples.basic_chatbot.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm
            
            # Test state
            state = {
                "messages": [],
                "user_input": "Hello",
                "response": ""
            }
            
            # Call the node
            result = chatbot_node(state)
            
            # Verify results
            assert len(result["messages"]) == 2  # User message + AI response
            assert isinstance(result["messages"][0], HumanMessage)
            assert result["messages"][0].content == "Hello"
            assert result["response"] == "Hello! How can I help you?"
            assert result["user_input"] == ""  # Should be cleared
    
    def test_chatbot_node_with_existing_messages(self):
        """Test that chatbot node preserves existing conversation history."""
        mock_response = Mock()
        mock_response.content = "I understand."
        
        with patch('src.examples.basic_chatbot.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm
            
            # Test state with existing messages
            existing_messages = [
                HumanMessage(content="Previous message"),
                AIMessage(content="Previous response")
            ]
            
            state = {
                "messages": existing_messages,
                "user_input": "New message",
                "response": ""
            }
            
            # Call the node
            result = chatbot_node(state)
            
            # Verify results
            assert len(result["messages"]) == 4  # 2 existing + 1 new user + 1 new AI
            assert result["messages"][:2] == existing_messages
            assert result["messages"][2].content == "New message"
            assert result["response"] == "I understand."
    
    def test_chatbot_node_handles_llm_error(self):
        """Test that chatbot node handles LLM errors gracefully."""
        with patch('src.examples.basic_chatbot.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.side_effect = Exception("API Error")
            mock_llm_class.return_value = mock_llm
            
            state = {
                "messages": [],
                "user_input": "Hello",
                "response": ""
            }
            
            # Call the node
            result = chatbot_node(state)
            
            # Verify error handling
            assert len(result["messages"]) == 2
            assert "Sorry, I encountered an error" in result["response"]
            assert isinstance(result["messages"][1], AIMessage)
    
    def test_chatbot_node_without_user_input(self):
        """Test that chatbot node handles empty user input."""
        mock_response = Mock()
        mock_response.content = "How can I help?"
        
        with patch('src.examples.basic_chatbot.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm
            
            state = {
                "messages": [HumanMessage(content="Previous message")],
                "user_input": "",  # Empty input
                "response": ""
            }
            
            # Call the node
            result = chatbot_node(state)
            
            # Should process existing messages without adding new user message
            assert len(result["messages"]) == 2  # 1 existing + 1 AI response
            assert result["response"] == "How can I help?"


class TestChatbotGraph:
    """Test cases for the chatbot graph creation and execution."""
    
    def test_create_chatbot_graph(self):
        """Test that chatbot graph is created correctly."""
        graph = create_chatbot_graph()
        
        # Verify graph structure
        nodes = list(graph.get_graph().nodes())
        assert "chatbot" in nodes
        
        # Verify edges
        edges = list(graph.get_graph().edges())
        assert any(edge[0] == "chatbot" for edge in edges)
    
    @patch('src.examples.basic_chatbot.chatbot_node')
    def test_graph_execution(self, mock_chatbot_node):
        """Test that graph executes correctly."""
        # Mock the chatbot node response
        mock_chatbot_node.return_value = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(content="Test response")
            ],
            "response": "Test response",
            "user_input": ""
        }
        
        graph = create_chatbot_graph()
        
        initial_state = {
            "messages": [],
            "user_input": "Test",
            "response": ""
        }
        
        # Execute the graph
        result = graph.invoke(initial_state)
        
        # Verify execution
        mock_chatbot_node.assert_called_once()
        assert result["response"] == "Test response"
        assert len(result["messages"]) == 2


class TestChatState:
    """Test cases for the ChatState type definition."""
    
    def test_chat_state_structure(self):
        """Test that ChatState has the expected structure."""
        # This is more of a documentation test
        # In a real scenario, you might use mypy or similar for type checking
        
        state: ChatState = {
            "messages": [],
            "user_input": "test",
            "response": "test response"
        }
        
        assert "messages" in state
        assert "user_input" in state
        assert "response" in state
        assert isinstance(state["messages"], list)
        assert isinstance(state["user_input"], str)
        assert isinstance(state["response"], str)


@pytest.fixture
def sample_chat_state():
    """Fixture providing a sample chat state for testing."""
    return {
        "messages": [
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!")
        ],
        "user_input": "How are you?",
        "response": ""
    }


class TestIntegration:
    """Integration tests for the complete chatbot system."""
    
    @pytest.mark.integration
    def test_full_conversation_flow(self, sample_chat_state):
        """Test a complete conversation flow through the graph."""
        mock_response = Mock()
        mock_response.content = "I'm doing well, thank you!"
        
        with patch('src.examples.basic_chatbot.ChatOpenAI') as mock_llm_class:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_llm_class.return_value = mock_llm
            
            graph = create_chatbot_graph()
            result = graph.invoke(sample_chat_state)
            
            # Verify the conversation flow
            assert len(result["messages"]) == 4  # 2 existing + 1 new user + 1 new AI
            assert result["messages"][-1].content == "I'm doing well, thank you!"
            assert result["response"] == "I'm doing well, thank you!"
            assert result["user_input"] == ""  # Should be cleared after processing