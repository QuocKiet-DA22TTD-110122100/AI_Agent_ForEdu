import { ReactNode } from 'react';
import { Menu, X } from 'lucide-react';

interface ModernChatLayoutProps {
  sidebarOpen: boolean;
  onToggleSidebar: () => void;
  sidebar: ReactNode;
  header: ReactNode;
  messages: ReactNode;
  input: ReactNode;
}

export const ModernChatLayout = ({
  sidebarOpen,
  onToggleSidebar,
  sidebar,
  header,
  messages,
  input,
}: ModernChatLayoutProps) => {
  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? 'w-80' : 'w-0'
        } transition-all duration-300 ease-in-out overflow-hidden bg-white border-r border-gray-200 shadow-lg`}
      >
        <div className="h-full flex flex-direction: column">
          {sidebar}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col relative">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between shadow-sm">
          <button
            onClick={onToggleSidebar}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          {header}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {messages}
        </div>

        {/* Input */}
        <div className="bg-white border-t border-gray-200 p-4">
          {input}
        </div>
      </div>
    </div>
  );
};
