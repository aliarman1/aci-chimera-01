'use client';

import React from 'react';
import { Message as MessageType } from '@/types';
import ImagePreview from './ImagePreview';

interface MessageProps {
  message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 animate-fadeIn`}>
      <div className={`max-w-[70%] ${isUser ? 'order-2' : 'order-1'}`}>
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-gradient-cyber text-white shadow-glow-cyan'
              : 'bg-dark-elevated border-2 border-accent-purple/30 text-text-primary shadow-glow-purple'
          }`}
        >
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
          
          {message.images && message.images.length > 0 && (
            <div className="mt-2">
              <ImagePreview images={message.images} isUploaded={true} />
            </div>
          )}
        </div>
        
        <div
          className={`text-xs text-text-secondary mt-1 px-2 ${
            isUser ? 'text-right' : 'text-left'
          }`}
        >
          {formatTime(message.created_at)}
        </div>
      </div>
    </div>
  );
};

export default Message;
