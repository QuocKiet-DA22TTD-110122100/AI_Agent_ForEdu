import React, { useState, useEffect } from 'react';
import { Calendar, Plus, Trash2, ExternalLink, Clock, MapPin, RefreshCw } from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { calendarService } from '../services/calendarService';
import type { CalendarEvent } from '../services/calendarService';
import toast from 'react-hot-toast';

const GoogleCalendarPage: React.FC = () => {
  const { user } = useAuthStore();
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  
  // Form states
  const [summary, setSummary] = useState('');
  const [description, setDescription] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [location, setLocation] = useState('');

  useEffect(() => {
    loadTodayEvents();
  }, []);
  
  // Set default time when modal opens
  useEffect(() => {
    if (showCreateModal && !startTime) {
      // Default: 1 hour from now
      const now = new Date();
      now.setMinutes(0, 0, 0); // Round to hour
      now.setHours(now.getHours() + 1);
      
      const start = now.toISOString().slice(0, 16); // Format: YYYY-MM-DDTHH:mm
      
      // End: 1 hour after start
      const endDate = new Date(now);
      endDate.setHours(endDate.getHours() + 1);
      const end = endDate.toISOString().slice(0, 16);
      
      setStartTime(start);
      setEndTime(end);
    }
  }, [showCreateModal]);

  const loadTodayEvents = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      const todayEvents = await calendarService.getTodayEvents(user.id);
      setEvents(todayEvents);
    } catch (error) {
      console.error('Failed to load events:', error);
      toast.error('Không thể tải lịch. Vui lòng kết nối Google Account trong Settings.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    // Convert datetime-local format to ISO 8601 with timezone
    // Input: "2025-12-23T14:30" -> Output: "2025-12-23T14:30:00+07:00"
    const formatDateTime = (datetime: string) => {
      if (!datetime) return '';
      // Add seconds if not present
      const withSeconds = datetime.includes(':') && datetime.split(':').length === 2 
        ? datetime + ':00' 
        : datetime;
      // Add Vietnam timezone
      return withSeconds + '+07:00';
    };

    try {
      const event = await calendarService.createEvent({
        user_id: user.id,
        summary,
        description,
        start_time: formatDateTime(startTime),
        end_time: formatDateTime(endTime),
        location,
      });

      if (event) {
        toast.success('✅ Đã tạo sự kiện trên Google Calendar!');
        setShowCreateModal(false);
        resetForm();
        loadTodayEvents();
      } else {
        toast.error('Không thể tạo sự kiện. Vui lòng kết nối Google Account.');
      }
    } catch (error) {
      console.error('Failed to create event:', error);
      toast.error('Lỗi khi tạo sự kiện');
    }
  };

  const handleDeleteEvent = async (eventId: string) => {
    if (!user) return;
    if (!window.confirm('Xóa sự kiện này?')) return;

    try {
      const success = await calendarService.deleteEvent(eventId, user.id);
      if (success) {
        toast.success('Đã xóa sự kiện');
        loadTodayEvents();
      } else {
        toast.error('Không thể xóa sự kiện');
      }
    } catch (error) {
      console.error('Failed to delete event:', error);
      toast.error('Lỗi khi xóa sự kiện');
    }
  };

  const resetForm = () => {
    setSummary('');
    setDescription('');
    setStartTime('');
    setEndTime('');
    setLocation('');
  };

  const formatTime = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
    } catch {
      return dateString;
    }
  };

  const getDefaultStartTime = () => {
    const now = new Date();
    now.setMinutes(0);
    now.setSeconds(0);
    return now.toISOString().slice(0, 16);
  };

  const getDefaultEndTime = () => {
    const now = new Date();
    now.setHours(now.getHours() + 1);
    now.setMinutes(0);
    now.setSeconds(0);
    return now.toISOString().slice(0, 16);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold dark:text-white flex items-center gap-3">
            <Calendar size={32} className="text-blue-500" />
            Google Calendar
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Quản lý lịch trình của bạn
          </p>
        </div>
        <button
          onClick={() => {
            setShowCreateModal(true);
            setStartTime(getDefaultStartTime());
            setEndTime(getDefaultEndTime());
          }}
          className="flex items-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors shadow-lg"
        >
          <Plus size={20} />
          Tạo sự kiện mới
        </button>
      </div>

      {/* Today's Events */}
      <div className="bg-white dark:bg-dark-800 rounded-lg shadow-lg p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold dark:text-white">Lịch hôm nay</h2>
          <button
            onClick={loadTodayEvents}
            className="text-blue-500 hover:text-blue-600"
            title="Refresh"
          >
            <RefreshCw size={20} />
          </button>
        </div>

        {events.length > 0 ? (
          <div className="space-y-4">
            {events.map((event) => (
              <div
                key={event.id}
                className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg dark:text-white">{event.summary}</h3>
                    {event.description && (
                      <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">
                        {event.description}
                      </p>
                    )}
                    
                    <div className="flex gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                      <div className="flex items-center gap-1">
                        <Clock size={16} />
                        {formatTime(event.start)} - {formatTime(event.end)}
                      </div>
                      {event.location && (
                        <div className="flex items-center gap-1">
                          <MapPin size={16} />
                          {event.location}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <a
                      href={event.html_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 text-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg"
                      title="Xem trên Google Calendar"
                    >
                      <ExternalLink size={18} />
                    </a>
                    <button
                      onClick={() => handleDeleteEvent(event.id)}
                      className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
                      title="Xóa"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Calendar size={48} className="mx-auto text-gray-400 mb-4" />
            <p className="text-gray-600 dark:text-gray-400">
              Không có sự kiện nào hôm nay
            </p>
          </div>
        )}
      </div>

      {/* Create Event Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-dark-800 rounded-xl p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4 dark:text-white">Tạo sự kiện mới</h2>
            
            <form onSubmit={handleCreateEvent}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Tiêu đề *
                </label>
                <input
                  type="text"
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  placeholder="VD: Họp team"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Mô tả
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  placeholder="Mô tả sự kiện..."
                  rows={3}
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Thời gian bắt đầu *
                </label>
                <input
                  type="datetime-local"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  required
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Thời gian kết thúc *
                </label>
                <input
                  type="datetime-local"
                  value={endTime}
                  onChange={(e) => setEndTime(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium mb-2 dark:text-gray-300">
                  Địa điểm
                </label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-dark-700 dark:text-white"
                  placeholder="VD: Phòng họp A"
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-dark-700 dark:text-white"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  Tạo sự kiện
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default GoogleCalendarPage;
