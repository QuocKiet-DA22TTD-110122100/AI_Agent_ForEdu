import { useQuery } from '@tanstack/react-query';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Sparkles, BookOpen, Clock, CheckCircle, Target, Brain, Zap } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';
import Layout from '../components/Layout';
import { courseService } from '../services/courseService';
import { quizService } from '../services/quizService';

const LessonPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const lessonId = parseInt(id || '0');
  const [generatingQuiz, setGeneratingQuiz] = useState(false);

  const { data: lesson, isLoading } = useQuery({
    queryKey: ['lesson', lessonId],
    queryFn: () => courseService.getLesson(lessonId),
  });

  const handleGenerateQuiz = async () => {
    setGeneratingQuiz(true);
    try {
      const quiz = await quizService.generateQuiz(lessonId, 'medium', 10);
      toast.success('Quiz generated successfully!');
      navigate(`/quiz/${quiz.id}`);
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to generate quiz');
    } finally {
      setGeneratingQuiz(false);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-gray-200 rounded w-1/4"></div>
            <div className="h-64 bg-gray-200 rounded-2xl"></div>
            <div className="h-32 bg-gray-200 rounded-2xl"></div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Back Button */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="mb-6"
        >
          <Link
            to={`/courses/${lesson?.courseId}`}
            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium hover:gap-3 transition-all"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Course
          </Link>
        </motion.div>

        {/* Lesson Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl p-8 md:p-12 mb-8 overflow-hidden relative"
        >
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -mr-32 -mt-32" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full -ml-24 -mb-24" />
          
          <div className="relative z-10">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-14 h-14 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center border-2 border-white/30">
                <BookOpen className="w-7 h-7 text-white" />
              </div>
              <div className="flex items-center gap-2 text-white/90 text-sm font-semibold">
                <Sparkles className="w-4 h-4" />
                <span>Lesson Content</span>
              </div>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">{lesson?.title}</h1>
            <div className="flex items-center gap-6 text-white/90 text-sm">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4" />
                <span>~15 min read</span>
              </div>
              <div className="flex items-center gap-2">
                <Target className="w-4 h-4" />
                <span>Beginner Level</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Lesson Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-8 md:p-12 shadow-lg border border-gray-100 mb-8"
        >
          <div className="prose prose-lg max-w-none">
            <div className="text-gray-800 leading-relaxed whitespace-pre-wrap">
              {lesson?.content}
            </div>
          </div>

          {/* Completion Indicator */}
          <div className="mt-12 pt-8 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <p className="font-bold text-lg">Lesson Progress</p>
                  <p className="text-sm text-gray-600">Mark as complete to track your progress</p>
                </div>
              </div>
              <button className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl">
                Mark Complete
              </button>
            </div>
          </div>
        </motion.div>

        {/* Quiz Generation Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl p-8 shadow-xl text-white overflow-hidden relative"
        >
          <div className="absolute top-0 right-0 w-48 h-48 bg-white/10 rounded-full -mr-24 -mt-24" />
          <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/10 rounded-full -ml-16 -mb-16" />
          
          <div className="relative z-10 flex flex-col md:flex-row items-center gap-6">
            <div className="w-20 h-20 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center border-2 border-white/30 flex-shrink-0">
              <Brain className="w-10 h-10" />
            </div>
            
            <div className="flex-1 text-center md:text-left">
              <h3 className="text-2xl font-bold mb-2">Test Your Knowledge</h3>
              <p className="text-lg opacity-90">
                Generate an AI-powered quiz to reinforce what you've learned
              </p>
            </div>
            
            <button
              onClick={handleGenerateQuiz}
              disabled={generatingQuiz}
              className="px-8 py-4 bg-white text-purple-600 rounded-xl font-bold hover:shadow-2xl transition-all disabled:opacity-50 flex items-center gap-3 text-lg"
            >
              {generatingQuiz ? (
                <>
                  <div className="w-6 h-6 border-3 border-purple-600 border-t-transparent rounded-full animate-spin"></div>
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  <span>Generate Quiz</span>
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default LessonPage;
