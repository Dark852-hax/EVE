// Type definitions for EVE AI

export type SidebarView = 'chat' | 'tools' | 'memory' | 'settings';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
  reasoning?: string;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
  category: 'web' | 'computer' | 'code' | 'system';
}

export interface Memory {
  id: string;
  type: 'conversation' | 'knowledge' | 'preference';
  content: string;
  timestamp: number;
}

export interface EVESettings {
  theme: 'dark' | 'light';
  model: string;
  temperature: number;
  maxTokens: number;
  webEnabled: boolean;
  computerEnabled: boolean;
  codeEnabled: boolean;
}

export interface ToolResult {
  success: boolean;
  output?: string;
  error?: string;
  data?: unknown;
}

export interface ChatRequest {
  messages: Message[];
  tools?: Tool[];
}

export interface ChatResponse {
  message: Message;
  toolResults?: ToolResult[];
}
