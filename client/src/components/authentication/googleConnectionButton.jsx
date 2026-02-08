import { GoogleLogin } from '@react-oauth/google';

const GoogleConnectionButton = (handleSuccess, handleError) => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', margin: '10px 0' }}>
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
        theme="filled_blue"
        shape="pill"
        text="signin_with"
        size="large"
      />
    </div>
  );
};

export default GoogleConnectionButton;