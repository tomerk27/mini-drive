import { Routes, Route, Navigate, BrowserRouter } from 'react-router-dom';
import LoginPage from '../pages/loginPage';
import Dashboard from '../pages/dashboard';
import SignupPage from '../pages/signupPage';
import StarredPage from '../pages/starredPage';
import ProtectedRoute from '../components/protectedRoute';

const AppRouter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/login' element={<LoginPage />} />
                <Route path='/signup' element={<SignupPage />} />
                <Route path='/' element={<Navigate to='/login' replace />} />

                <Route element={<ProtectedRoute />}>
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="dashboard/:folderId" element={<Dashboard />} />
                    <Route path="starred" element={<StarredPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    );
};

export default AppRouter;