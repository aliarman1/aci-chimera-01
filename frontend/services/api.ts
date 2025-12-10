import axios from 'axios';
import { ChatResponse, Conversation, ConversationListItem } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const chatAPI = {
  // Send a message with optional images
  sendMessage: async (
    message: string,
    conversationId?: number,
    images?: File[]
  ): Promise<ChatResponse> => {
    const formData = new FormData();
    formData.append('message', message);
    
    if (conversationId) {
      formData.append('conversation_id', conversationId.toString());
    }
    
    if (images && images.length > 0) {
      images.forEach((image) => {
        formData.append('images', image);
      });
    }
    
    const response = await api.post<ChatResponse>('/chat/message', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Get all conversations
  getConversations: async (): Promise<ConversationListItem[]> => {
    const response = await api.get<ConversationListItem[]>('/chat/conversations');
    return response.data;
  },

  // Get a specific conversation with all messages
  getConversation: async (conversationId: number): Promise<Conversation> => {
    const response = await api.get<Conversation>(`/chat/conversations/${conversationId}`);
    return response.data;
  },

  // Delete a conversation
  deleteConversation: async (conversationId: number): Promise<void> => {
    await api.delete(`/chat/conversations/${conversationId}`);
  },

  // Create a new conversation
  createConversation: async (): Promise<Conversation> => {
    const response = await api.post<Conversation>('/chat/conversations');
    return response.data;
  },
};

export default api;
