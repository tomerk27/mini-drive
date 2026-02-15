import { Routes, Route, Navigate, BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/loginPage';
import Dashboard from '../pages/dashboard';
import SignupPage from '../pages/signupPage';

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/login' element={<LoginPage />} />
                <Route path="dashboard/folder/:folderId" element={<Dashboard />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path='/signup' element={<SignupPage />} />
                <Route path='/' element={<Navigate to='/login' replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;