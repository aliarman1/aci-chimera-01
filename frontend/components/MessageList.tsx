'use client';

import React, { useEffect, useRef } from 'react';
import { Message as MessageType } from '@/types';
import Message from './Message';

interface MessageListProps {
  messages: MessageType[];
  isLoading: boolean;
}

const MessageList: React.FC<MessageListProps> = ({ messages, isLoading }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      <div className="max-w-4xl mx-auto">
        {messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full text-center py-20">
            <div className="mb-4 text-6xl">🤖</div>
            <h2 className="text-2xl font-bold text-text-primary mb-2 bg-gradient-cyber bg-clip-text text-transparent">
              Welcome to Chimera AI
            </h2>
            <p className="text-text-secondary max-w-md">
              Start a conversation by typing a message or uploading images. I can help you with
              multimodal tasks using Gemini Pro Vision.
            </p>
          </div>
        )}
        
        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-dark-elevated border-2 border-accent-purple/30 px-4 py-3 rounded-2xl shadow-glow-purple">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-accent-cyan rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-accent-purple rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-accent-pink rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default MessageList;
