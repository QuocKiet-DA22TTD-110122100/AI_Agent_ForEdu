import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const RegisterPage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to login page with register tab
    navigate('/login?tab=register');
  }, [navigate]);

  return null;
};

export default RegisterPage;
