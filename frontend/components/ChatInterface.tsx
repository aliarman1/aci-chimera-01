'use client';

import React, { useState, useEffect } from 'react';
import { Message, ConversationListItem } from '@/types';
import { chatAPI } from '@/services/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';

const ChatInterface: React.FC = () => {
  const [conversations, setConversations] = useState<ConversationListItem[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  // Load messages when conversation changes
  useEffect(() => {
    if (currentConversationId) {
      loadConversation(currentConversationId);
    }
  }, [currentConversationId]);

  const loadConversations = async () => {
    try {
      const convs = await chatAPI.getConversations();
      setConversations(convs);
    } catch (err) {
      console.error('Failed to load conversations:', err);
    }
  };

  const loadConversation = async (id: number) => {
    try {
      const conv = await chatAPI.getConversation(id);
      setMessages(conv.messages);
      setError(null);
    } catch (err) {
      console.error('Failed to load conversation:', err);
      setError('Failed to load conversation');
    }
  };

  const handleSendMessage = async (message: string, images: File[]) => {
    if (!message.trim() && images.length === 0) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await chatAPI.sendMessage(message, currentConversationId || undefined, images);
      
      // Add both user and assistant messages
      setMessages((prev) => [...prev, response.user_message, response.assistant_message]);
      
      // Update current conversation ID if it's a new conversation
      if (!currentConversationId) {
        setCurrentConversationId(response.conversation_id);
      }
      
      // Reload conversations list
      loadConversations();
    } catch (err: any) {
      console.error('Failed to send message:', err);
      const errorMessage = err.response?.data?.detail || 'Failed to send message. Please try again.';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([]);
    setError(null);
  };

  const handleDeleteConversation = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!confirm('Are you sure you want to delete this conversation?')) return;

    try {
      await chatAPI.deleteConversation(id);
      
      // If deleted conversation was active, reset
      if (id === currentConversationId) {
        handleNewConversation();
      }
      
      // Reload conversations
      loadConversations();
    } catch (err) {
      console.error('Failed to delete conversation:', err);
      setError('Failed to delete conversation');
    }
  };

  return (
    <div className="flex h-screen bg-dark-bg text-text-primary">
      {/* Sidebar */}
      <div
        className={`${
          isSidebarOpen ? 'w-80' : 'w-0'
        } bg-dark-surface border-r-2 border-border-color transition-all duration-300 overflow-hidden flex flex-col`}
      >
        <div className="p-4 border-b-2 border-border-color">
          <button
            onClick={handleNewConversation}
            className="w-full px-4 py-3 bg-gradient-cyber hover:shadow-glow-cyan text-white font-medium rounded-lg transition-all flex items-center justify-center gap-2 shadow-md"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Conversation
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setCurrentConversationId(conv.id)}
              className={`p-3 mb-2 rounded-lg cursor-pointer transition-all group ${
                currentConversationId === conv.id
                  ? 'bg-dark-elevated border-2 border-accent-cyan shadow-glow-cyan'
                  : 'bg-dark-bg border-2 border-transparent hover:border-accent-purple/50 hover:bg-dark-elevated'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-text-primary truncate">
                    {conv.title || 'New Conversation'}
                  </h3>
                  <p className="text-xs text-text-secondary mt-1">
                    {conv.message_count} messages
                  </p>
                </div>
                <button
                  onClick={(e) => handleDeleteConversation(conv.id, e)}
                  className="ml-2 p-1 text-text-secondary hover:text-accent-pink opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-16 bg-dark-surface border-b-2 border-border-color flex items-center px-4 shadow-md">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="p-2 hover:bg-dark-elevated rounded-lg transition-all mr-4 border-2 border-transparent hover:border-accent-cyan"
          >
            <svg className="w-6 h-6 text-accent-cyan" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 className="text-xl font-bold bg-gradient-cyber bg-clip-text text-transparent">
            Chimera AI - Multimodal Chat
          </h1>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mx-4 mt-4 p-4 bg-accent-pink/20 border-2 border-accent-pink rounded-lg text-accent-pink flex items-start gap-2">
            <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <p className="font-medium">Error</p>
              <p className="text-sm mt-1">{error}</p>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-accent-pink hover:text-white transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        )}

        {/* Messages */}
        <MessageList messages={messages} isLoading={isLoading} />

        {/* Input */}
        <MessageInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;
