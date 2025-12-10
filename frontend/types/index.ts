export interface ImageInfo {
  id: number;
  file_path: string;
  file_name: string;
  mime_type: string;
  file_size?: number;
  created_at: string;
}

export interface Message {
  id: number;
  conversation_id: number;
  role: 'user' | 'assistant';
  content: string;
  images: ImageInfo[];
  created_at: string;
}

export interface Conversation {
  id: number;
  title?: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

export interface ConversationListItem {
  id: number;
  title?: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ChatResponse {
  user_message: Message;
  assistant_message: Message;
  conversation_id: number;
}
