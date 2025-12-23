import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('🚨 Error Boundary caught an error:', error, errorInfo);
    this.setState({ error, errorInfo });
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
    // Reload the page to reset state
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default fallback UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full">
            <div className="flex items-center justify-center mb-6">
              <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
            </div>
            
            <h1 className="text-2xl font-bold text-gray-900 mb-4 text-center">
              Oops! Có lỗi xảy ra
            </h1>
            
            <p className="text-gray-600 mb-6 text-center">
              Chatbox gặp sự cố không mong muốn. Đừng lo lắng, dữ liệu của bạn vẫn an toàn.
            </p>

            {this.state.error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-800 font-mono break-words">
                  <strong>Lỗi:</strong> {this.state.error.toString()}
                </p>
              </div>
            )}

            <div className="flex flex-col space-y-3">
              <button
                onClick={this.handleReset}
                className="w-full px-6 py-3 bg-gradient-to-r from-primary-500 to-purple-500 text-white rounded-lg font-semibold hover:from-primary-600 hover:to-purple-600 transition-all shadow-md hover:shadow-lg"
              >
                🔄 Tải lại trang
              </button>
              
              <button
                onClick={() => window.history.back()}
                className="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-semibold hover:bg-gray-200 transition-colors"
              >
                ← Quay lại
              </button>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-500">
                Nếu lỗi tiếp tục xảy ra, vui lòng liên hệ hỗ trợ.
              </p>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
