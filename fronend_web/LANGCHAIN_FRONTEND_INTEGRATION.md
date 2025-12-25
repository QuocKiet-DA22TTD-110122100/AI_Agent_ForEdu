# 🎨 LangChain Frontend Integration Guide

## 📋 Tích Hợp LangChain Agent vào React Frontend

Hướng dẫn thêm LangChain agent vào giao diện chat hiện tại.

---

## 🔧 **Bước 1: Thêm Service**

### **File: `src/services/langchainService.ts`**

```typescript
import api from './api';

export interface LangChainChatRequest {
  message: string;
  user_id?: number;
  reset_memory?: boolean;
}

export interface LangChainChatResponse {
  success: boolean;
  response: string;
  agent_type: string;
  intermediate_steps?: any[];
  error?: string;
}

export interface LangChainStatus {
  available: boolean;
  tools?: string[];
  tool_count?: number;
  memory_enabled?: boolean;
  llm_model?: string;
  agent_type?: string;
  message?: string;
}

/**
 * Chat với LangChain AI Agent
 */
export const chatWithLangChain = async (
  message: string,
  resetMemory: boolean = false
): Promise<LangChainChatResponse> => {
  const response = await api.post('/api/chat/langchain', {
    message,
    reset_memory: resetMemory
  });
  return response.data;
};

/**
 * Reset agent memory
 */
export const resetLangChainMemory = async (): Promise<{ success: boolean; message: string }> => {
  const response = await api.post('/api/chat/langchain/reset');
  return response.data;
};

/**
 * Check LangChain agent status
 */
export const getLangChainStatus = async (): Promise<LangChainStatus> => {
  const response = await api.get('/api/chat/langchain/status');
  return response.data;
};
```

---

## 🎨 **Bước 2: Thêm UI Component**

### **File: `src/components/chat/AgentModeSelector.tsx`**

```typescript
import React, { useState, useEffect } from 'react';
import { getLangChainStatus } from '../../services/langchainService';

interface AgentModeSelectorProps {
  mode: 'standard' | 'langchain';
  onModeChange: (mode: 'standard' | 'langchain') => void;
}

export const AgentModeSelector: React.FC<AgentModeSelectorProps> = ({ mode, onModeChange }) => {
  const [langchainAvailable, setLangchainAvailable] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkLangChainStatus();
  }, []);

  const checkLangChainStatus = async () => {
    try {
      const status = await getLangChainStatus();
      setLangchainAvailable(status.available);
    } catch (error) {
      setLangchainAvailable(false);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-sm text-gray-500">Checking agent status...</div>;
  }

  return (
    <div className="flex items-center gap-2 p-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
        Agent Mode:
      </span>
      
      <button
        onClick={() => onModeChange('standard')}
        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
          mode === 'standard'
            ? 'bg-blue-500 text-white'
            : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50'
        }`}
      >
        Standard
      </button>
      
      <button
        onClick={() => onModeChange('langchain')}
        disabled={!langchainAvailable}
        className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
          mode === 'langchain'
            ? 'bg-purple-500 text-white'
            : langchainAvailable
            ? 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        🦜 LangChain
        {mode === 'langchain' && ' ✨'}
      </button>
      
      {!langchainAvailable && (
        <span className="text-xs text-red-500">
          (Not available)
        </span>
      )}
    </div>
  );
};
```

---

## 💬 **Bước 3: Update ChatPage**

### **File: `src/pages/ChatPage.tsx`**

Thêm vào component:

```typescript
import { chatWithLangChain, resetLangChainMemory } from '../services/langchainService';
import { AgentModeSelector } from '../components/chat/AgentModeSelector';

// Add state
const [agentMode, setAgentMode] = useState<'standard' | 'langchain'>('standard');

// Add function
const handleSendMessageLangChain = async (message: string) => {
  try {
    setIsLoading(true);
    
    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    
    // Call LangChain agent
    const result = await chatWithLangChain(message);
    
    // Add AI response
    const aiMessage: Message = {
      id: Date.now() + 1,
      text: result.response,
      sender: 'ai',
      timestamp: new Date(),
      agentType: 'langchain',
      intermediateSteps: result.intermediate_steps
    };
    setMessages(prev => [...prev, aiMessage]);
    
  } catch (error) {
    console.error('LangChain error:', error);
    toast.error('Lỗi khi chat với LangChain agent');
  } finally {
    setIsLoading(false);
  }
};

// Update handleSendMessage
const handleSendMessage = async (message: string) => {
  if (agentMode === 'langchain') {
    await handleSendMessageLangChain(message);
  } else {
    // Existing standard chat logic
    await handleSendMessageStandard(message);
  }
};

// Add reset memory button
const handleResetMemory = async () => {
  try {
    await resetLangChainMemory();
    toast.success('Agent memory reset!');
  } catch (error) {
    toast.error('Failed to reset memory');
  }
};

// In JSX, add mode selector
<div className="chat-header">
  <AgentModeSelector 
    mode={agentMode}
    onModeChange={setAgentMode}
  />
  
  {agentMode === 'langchain' && (
    <button
      onClick={handleResetMemory}
      className="text-sm text-gray-500 hover:text-gray-700"
    >
      🔄 Reset Memory
    </button>
  )}
</div>
```

---

## 🎨 **Bước 4: Hiển Thị Intermediate Steps**

### **Component: `IntermediateStepsDisplay.tsx`**

```typescript
import React, { useState } from 'react';

interface IntermediateStepsDisplayProps {
  steps: any[];
}

export const IntermediateStepsDisplay: React.FC<IntermediateStepsDisplayProps> = ({ steps }) => {
  const [expanded, setExpanded] = useState(false);

  if (!steps || steps.length === 0) return null;

  return (
    <div className="mt-2 border-t border-gray-200 dark:border-gray-700 pt-2">
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
      >
        <span>{expanded ? '▼' : '▶'}</span>
        <span>Agent reasoning ({steps.length} steps)</span>
      </button>
      
      {expanded && (
        <div className="mt-2 space-y-2">
          {steps.map((step, index) => (
            <div key={index} className="text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded">
              <div className="font-medium text-purple-600">
                Step {index + 1}: {step.tool || 'Thinking'}
              </div>
              <div className="text-gray-600 dark:text-gray-400 mt-1">
                {JSON.stringify(step.input || step, null, 2)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
```

Sử dụng trong message:

```typescript
{message.intermediateSteps && (
  <IntermediateStepsDisplay steps={message.intermediateSteps} />
)}
```

---

## 🎯 **Bước 5: Add Badge**

Hiển thị badge khi dùng LangChain:

```typescript
{message.agentType === 'langchain' && (
  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800">
    🦜 LangChain
  </span>
)}
```

---

## 📱 **UI/UX Suggestions**

### **1. Mode Toggle**
```
┌─────────────────────────────────┐
│ Agent Mode: [Standard] [🦜 LangChain ✨] │
└─────────────────────────────────┘
```

### **2. Message Display**
```
┌─────────────────────────────────┐
│ 🤖 AI (🦜 LangChain)            │
│                                  │
│ ✅ Đã gửi email và thêm vào lịch│
│                                  │
│ ▶ Agent reasoning (3 steps)     │
└─────────────────────────────────┘
```

### **3. Loading State**
```
🦜 LangChain is thinking...
  → Step 1: Getting contacts
  → Step 2: Sending email
  → Step 3: Creating event
```

---

## 🎨 **Styling**

### **Tailwind Classes:**

```css
/* LangChain mode active */
.langchain-active {
  @apply bg-gradient-to-r from-purple-500 to-pink-500;
}

/* LangChain message */
.langchain-message {
  @apply border-l-4 border-purple-500;
}

/* Intermediate steps */
.intermediate-steps {
  @apply bg-purple-50 dark:bg-purple-900/20;
}
```

---

## 🧪 **Testing**

### **Test Cases:**

1. **Switch Mode**
   - Click "LangChain" button
   - Verify mode changes
   - Send message
   - Verify response has `agentType: 'langchain'`

2. **Memory Test**
   - Send: "Tên tôi là Minh"
   - Send: "Tên tôi là gì?"
   - Verify agent remembers

3. **Reset Memory**
   - Click "Reset Memory"
   - Send: "Tên tôi là gì?"
   - Verify agent doesn't remember

4. **Intermediate Steps**
   - Send complex query
   - Click "Agent reasoning"
   - Verify steps display

---

## 📊 **Example Flow**

```typescript
// User sends message
User: "Gửi email xin nghỉ cho thầy và thêm vào lịch"

// Frontend calls
await chatWithLangChain(message)

// Backend processes (LangChain agent)
Agent:
  Thought: Need to send email
  Action: GetContacts
  Observation: [teacher@tvu.edu.vn]
  
  Thought: Now send email
  Action: SendEmail
  Observation: Email sent
  
  Thought: Add to calendar
  Action: CreateCalendarEvent
  Observation: Event created
  
  Final Answer: ✅ Done!

// Frontend displays
AI (🦜 LangChain): ✅ Đã gửi email và thêm vào lịch

▶ Agent reasoning (3 steps)
  Step 1: GetContacts
  Step 2: SendEmail
  Step 3: CreateCalendarEvent
```

---

## ✅ **Checklist**

- [ ] Add `langchainService.ts`
- [ ] Add `AgentModeSelector` component
- [ ] Update `ChatPage.tsx`
- [ ] Add `IntermediateStepsDisplay` component
- [ ] Add styling
- [ ] Test mode switching
- [ ] Test memory
- [ ] Test reset
- [ ] Test intermediate steps display

---

## 🚀 **Deploy**

```bash
# Build frontend
cd fronend_web
npm run build

# Deploy
# (Your deployment process)
```

---

**Happy coding!** 🎉
