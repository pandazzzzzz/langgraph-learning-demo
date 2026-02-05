"""
Basic Chatbot Example - Module 01

This example demonstrates the fundamental concepts of LangGraph:
- Creating a simple state graph
- Defining nodes and edges
- Managing conversation state
- Basic LLM integration

This is your first hands-on introduction to LangGraph!
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# LangGraph and LangChain imports
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing_extensions import TypedDict

# Load environment variables
load_dotenv()


class ChatState(TypedDict):
    """
    State schema for our chatbot.
    
    This defines what information our graph will track
    as it processes conversations.
    """
    messages: list[BaseMessage]
    user_input: str
    response: str


def chatbot_node(state: ChatState) -> Dict[str, Any]:
    """
    Main chatbot node that processes user input and generates responses.
    
    Args:
        state: Current conversation state
        
    Returns:
        Updated state with AI response
    """
    # Initialize the LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Get the conversation history
    messages = state.get("messages", [])
    
    # Add the new user message
    if state.get("user_input"):
        messages.append(HumanMessage(content=state["user_input"]))
    
    # Generate AI response
    try:
        ai_response = llm.invoke(messages)
        messages.append(ai_response)
        
        return {
            "messages": messages,
            "response": ai_response.content,
            "user_input": ""  # Clear the input after processing
        }
    except Exception as e:
        error_message = f"Sorry, I encountered an error: {str(e)}"
        messages.append(AIMessage(content=error_message))
        
        return {
            "messages": messages,
            "response": error_message,
            "user_input": ""
        }


def create_chatbot_graph() -> StateGraph:
    """
    Create and configure the chatbot graph.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Create a new state graph
    workflow = StateGraph(ChatState)
    
    # Add the chatbot node
    workflow.add_node("chatbot", chatbot_node)
    
    # Set the entry point
    workflow.set_entry_point("chatbot")
    
    # Add edge from chatbot to END
    workflow.add_edge("chatbot", END)
    
    # Compile the graph
    return workflow.compile()


def run_chatbot_demo():
    """
    Run an interactive chatbot demo.
    
    This function demonstrates how to use the compiled graph
    in a conversation loop.
    """
    print("🤖 LangGraph Basic Chatbot Demo")
    print("=" * 40)
    print("Type 'quit' to exit the conversation")
    print("=" * 40)
    
    # Create the chatbot graph
    chatbot = create_chatbot_graph()
    
    # Initialize conversation state
    conversation_state = {
        "messages": [],
        "user_input": "",
        "response": ""
    }
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye! Thanks for trying the LangGraph chatbot!")
            break
        
        if not user_input:
            continue
        
        # Update state with user input
        conversation_state["user_input"] = user_input
        
        # Process through the graph
        try:
            result = chatbot.invoke(conversation_state)
            conversation_state = result
            
            # Display AI response
            print(f"🤖 Bot: {result['response']}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Please check your OpenAI API key and try again.")


def demonstrate_graph_structure():
    """
    Demonstrate how to inspect the graph structure.
    
    This is useful for understanding and debugging your graphs.
    """
    print("\n📊 Graph Structure Analysis")
    print("=" * 30)
    
    # Create the graph
    chatbot = create_chatbot_graph()
    
    # Print graph information
    print("Nodes in the graph:")
    for node_name in chatbot.get_graph().nodes():
        print(f"  • {node_name}")
    
    print("\nEdges in the graph:")
    for edge in chatbot.get_graph().edges():
        print(f"  • {edge[0]} → {edge[1]}")
    
    print("\nEntry points:")
    entry_points = chatbot.get_graph().get_input_schema()
    print(f"  • Input schema: {entry_points}")


if __name__ == "__main__":
    # Check if OpenAI API key is configured
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        print("Example: OPENAI_API_KEY=your_api_key_here")
        exit(1)
    
    print("🚀 Starting LangGraph Basic Chatbot Example")
    
    # Demonstrate graph structure
    demonstrate_graph_structure()
    
    # Run the interactive demo
    run_chatbot_demo()