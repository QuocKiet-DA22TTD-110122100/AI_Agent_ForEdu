import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  BookOpen, MessageSquare, Trophy, TrendingUp, Clock, Award, 
  Target, Sparkles, Calendar, BarChart3, Users, ArrowRight,
  CheckCircle, Zap, Brain, Star, ChevronRight
} from 'lucide-react';
import Layout from '../components/Layout';
import { courseService } from '../services/courseService';
import { chatService } from '../services/chatService';
import { useAuthStore } from '../store/authStore';
import { Link } from 'react-router-dom';

const DashboardPage = () => {
  const user = useAuthStore((state) => state.user);

  const { data: courses = [] } = useQuery({
    queryKey: ['courses'],
    queryFn: courseService.getCourses,
  });

  const { data: sessions = [] } = useQuery({
    queryKey: ['chat-sessions'],
    queryFn: chatService.getSessions,
  });

  const stats = [
    {
      icon: BookOpen,
      label: 'Active Courses',
      value: courses.length,
      change: '+12%',
      changeType: 'positive',
      gradient: 'from-blue-500 to-cyan-500',
      iconBg: 'bg-blue-500/10',
      iconColor: 'text-blue-600',
    },
    {
      icon: MessageSquare,
      label: 'AI Conversations',
      value: sessions.length,
      change: '+8%',
      changeType: 'positive',
      gradient: 'from-purple-500 to-pink-500',
      iconBg: 'bg-purple-500/10',
      iconColor: 'text-purple-600',
    },
    {
      icon: Trophy,
      label: 'Achievements',
      value: 24,
      change: '+3',
      changeType: 'positive',
      gradient: 'from-amber-500 to-orange-500',
      iconBg: 'bg-amber-500/10',
      iconColor: 'text-amber-600',
    },
    {
      icon: TrendingUp,
      label: 'Learning Streak',
      value: '12 days',
      change: 'On fire!',
      changeType: 'positive',
      gradient: 'from-green-500 to-emerald-500',
      iconBg: 'bg-green-500/10',
      iconColor: 'text-green-600',
    },
  ];

  const recentActivities = [
    { type: 'course', title: 'Completed: Introduction to AI', time: '2 hours ago', icon: CheckCircle, color: 'text-green-500' },
    { type: 'chat', title: 'AI Chat Session', time: '3 hours ago', icon: MessageSquare, color: 'text-purple-500' },
    { type: 'achievement', title: 'Earned: Quick Learner Badge', time: '1 day ago', icon: Trophy, color: 'text-amber-500' },
  ];

  const upcomingTasks = [
    { title: 'Complete Chapter 5 Quiz', course: 'Machine Learning Basics', deadline: 'Today', priority: 'high' },
    { title: 'Review AI Ethics Module', course: 'AI Fundamentals', deadline: 'Tomorrow', priority: 'medium' },
    { title: 'Start New Course', course: 'Deep Learning', deadline: 'This Week', priority: 'low' },
  ];

  const recentCourses = courses.slice(0, 3);

  const priorityColors = {
    high: 'bg-red-100 text-red-700 border-red-200',
    medium: 'bg-yellow-100 text-yellow-700 border-yellow-200',
    low: 'bg-green-100 text-green-700 border-green-200',
  };

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2 bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
                Welcome back, {user?.fullName}! 👋
              </h1>
              <p className="text-gray-600 text-lg flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-yellow-500" />
                Ready to continue your learning journey?
              </p>
            </div>
            <div className="mt-4 md:mt-0">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-xl font-medium">
                <Zap className="w-4 h-4" />
                Level {Math.floor(courses.length / 3) + 1}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-xl ${stat.iconBg}`}>
                  <stat.icon className={`w-6 h-6 ${stat.iconColor}`} />
                </div>
                <span className={`text-sm font-semibold px-2 py-1 rounded-lg ${
                  stat.changeType === 'positive' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                }`}>
                  {stat.change}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-1 font-medium">{stat.label}</p>
              <p className="text-3xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent">
                {stat.value}
              </p>
            </motion.div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-8 mb-8">
          {/* Continue Learning Section */}
          <div className="lg:col-span-2 space-y-6">
            {/* Recent Courses */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
            >
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-2xl font-bold mb-1">Continue Learning</h2>
                  <p className="text-gray-600 text-sm">Pick up where you left off</p>
                </div>
                <Link 
                  to="/courses" 
                  className="flex items-center gap-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors font-medium"
                >
                  View All
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="space-y-4">
                {recentCourses.length > 0 ? (
                  recentCourses.map((course, index) => (
                    <motion.div
                      key={course.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      whileHover={{ scale: 1.02 }}
                    >
                      <Link 
                        to={`/courses/${course.id}`} 
                        className="flex items-center gap-4 p-4 rounded-xl border-2 border-gray-100 hover:border-blue-200 hover:shadow-md transition-all duration-300 group"
                      >
                        <div className="relative">
                          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white font-bold text-2xl shadow-lg">
                            {course.title.charAt(0)}
                          </div>
                          <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
                            <CheckCircle className="w-4 h-4 text-white" />
                          </div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="font-bold text-lg mb-1 group-hover:text-blue-600 transition-colors truncate">
                            {course.title}
                          </h3>
                          <p className="text-gray-600 text-sm line-clamp-1 mb-2">{course.description}</p>
                          <div className="flex items-center gap-4 text-sm text-gray-500">
                            <span className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              {new Date(course.createdAt).toLocaleDateString()}
                            </span>
                            <div className="flex-1 max-w-xs">
                              <div className="h-1.5 bg-gray-200 rounded-full overflow-hidden">
                                <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full" style={{ width: '65%' }} />
                              </div>
                            </div>
                            <span className="text-blue-600 font-medium">65%</span>
                          </div>
                        </div>
                        <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 group-hover:translate-x-1 transition-all" />
                      </Link>
                    </motion.div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="w-10 h-10 text-gray-400" />
                    </div>
                    <p className="text-gray-600 mb-4 font-medium">No courses yet</p>
                    <p className="text-gray-500 text-sm mb-6">Start your learning journey today!</p>
                    <Link 
                      to="/courses" 
                      className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all"
                    >
                      <BookOpen className="w-5 h-5" />
                      Browse Courses
                    </Link>
                  </div>
                )}
              </div>
            </motion.div>

            {/* Upcoming Tasks */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Target className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <h2 className="text-xl font-bold">Upcoming Tasks</h2>
                  <p className="text-gray-600 text-sm">Stay on track with your goals</p>
                </div>
              </div>

              <div className="space-y-3">
                {upcomingTasks.map((task, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="flex items-center gap-4 p-4 rounded-xl border-2 border-gray-100 hover:border-purple-200 hover:shadow-md transition-all cursor-pointer group"
                  >
                    <div className="flex-1">
                      <h4 className="font-semibold mb-1 group-hover:text-purple-600 transition-colors">{task.title}</h4>
                      <p className="text-sm text-gray-600 mb-2">{task.course}</p>
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-gray-400" />
                        <span className="text-sm text-gray-500">{task.deadline}</span>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-lg text-xs font-semibold border ${priorityColors[task.priority as keyof typeof priorityColors]}`}>
                      {task.priority.toUpperCase()}
                    </span>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Zap className="w-5 h-5 text-blue-600" />
                </div>
                <h2 className="text-xl font-bold">Quick Actions</h2>
              </div>

              <div className="space-y-3">
                <Link 
                  to="/chat" 
                  className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-100 hover:border-green-300 hover:shadow-md transition-all group"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center text-white shadow-lg">
                    <Brain className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold group-hover:text-green-700 transition-colors">AI Assistant</h3>
                    <p className="text-sm text-gray-600">Ask anything, learn faster</p>
                  </div>
                  <ChevronRight className="w-5 h-5 text-green-600 group-hover:translate-x-1 transition-transform" />
                </Link>

                <Link 
                  to="/courses" 
                  className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-blue-50 to-cyan-50 border-2 border-blue-100 hover:border-blue-300 hover:shadow-md transition-all group"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center text-white shadow-lg">
                    <BookOpen className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold group-hover:text-blue-700 transition-colors">Explore Courses</h3>
                    <p className="text-sm text-gray-600">Discover new topics</p>
                  </div>
                  <ChevronRight className="w-5 h-5 text-blue-600 group-hover:translate-x-1 transition-transform" />
                </Link>

                <Link 
                  to="/flashcards" 
                  className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-100 hover:border-purple-300 hover:shadow-md transition-all group"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-white shadow-lg">
                    <BarChart3 className="w-6 h-6" />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold group-hover:text-purple-700 transition-colors">Study Flashcards</h3>
                    <p className="text-sm text-gray-600">Review and memorize</p>
                  </div>
                  <ChevronRight className="w-5 h-5 text-purple-600 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </motion.div>

            {/* Daily Progress */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl p-6 shadow-lg text-white overflow-hidden relative"
            >
              <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16" />
              <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/10 rounded-full -ml-12 -mb-12" />
              
              <div className="relative z-10">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-white/20 backdrop-blur-sm rounded-lg">
                    <Award className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">Daily Goal</h3>
                    <p className="text-sm opacity-90">Keep up the great work!</p>
                  </div>
                </div>

                <div className="space-y-3 mb-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="opacity-90">Study Time</span>
                      <span className="font-semibold">2.5 / 3 hrs</span>
                    </div>
                    <div className="w-full bg-white/20 rounded-full h-2.5 overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: '83%' }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className="bg-white rounded-full h-full"
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="opacity-90">Lessons Completed</span>
                      <span className="font-semibold">5 / 7</span>
                    </div>
                    <div className="w-full bg-white/20 rounded-full h-2.5 overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: '71%' }}
                        transition={{ duration: 1, delay: 0.7 }}
                        className="bg-white rounded-full h-full"
                      />
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 bg-white/20 backdrop-blur-sm rounded-xl">
                  <span className="text-sm font-medium">Overall Progress</span>
                  <span className="text-2xl font-bold">77%</span>
                </div>
              </div>
            </motion.div>

            {/* Recent Activity */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
            >
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-indigo-100 rounded-lg">
                  <Clock className="w-5 h-5 text-indigo-600" />
                </div>
                <h2 className="text-xl font-bold">Recent Activity</h2>
              </div>

              <div className="space-y-4">
                {recentActivities.map((activity, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 + index * 0.1 }}
                    className="flex items-start gap-3 pb-4 border-b border-gray-100 last:border-0 last:pb-0"
                  >
                    <div className={`p-2 rounded-lg ${activity.color.replace('text-', 'bg-')}/10`}>
                      <activity.icon className={`w-4 h-4 ${activity.color}`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm mb-1">{activity.title}</p>
                      <p className="text-xs text-gray-500">{activity.time}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Achievement Showcase */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-2xl p-8 shadow-2xl text-white relative overflow-hidden"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full -ml-24 -mb-24" />
          
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <Star className="w-6 h-6 fill-current" />
                <h2 className="text-2xl font-bold">Your Learning Journey</h2>
              </div>
              <p className="text-lg opacity-90 mb-4">
                You're making amazing progress! Keep learning and unlock new achievements.
              </p>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <Trophy className="w-5 h-5" />
                  <span className="font-semibold">24 Badges</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5" />
                  <span className="font-semibold">Top 15%</span>
                </div>
                <div className="flex items-center gap-2">
                  <Zap className="w-5 h-5" />
                  <span className="font-semibold">Level {Math.floor(courses.length / 3) + 1}</span>
                </div>
              </div>
            </div>
            <div className="flex gap-3">
              <Link
                to="/profile"
                className="px-6 py-3 bg-white text-purple-600 rounded-xl font-semibold hover:shadow-xl transition-all"
              >
                View Profile
              </Link>
              <Link
                to="/achievements"
                className="px-6 py-3 bg-white/20 backdrop-blur-sm border-2 border-white/30 rounded-xl font-semibold hover:bg-white/30 transition-all"
              >
                All Achievements
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default DashboardPage;
