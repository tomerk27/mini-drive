import { Routes, Route, Navigate, BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/loginPage';
import Dashboard from '../pages/dashboard';

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/login' element={<LoginPage />} />
                <Route path='/dashboard' element={<Dashboard />} />
                <Route path='/' element={<Navigate to='/login' replace />} />
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;