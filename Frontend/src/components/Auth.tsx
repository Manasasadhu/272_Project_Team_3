import { useState } from 'react';
import Landing from './Landing';
import Login from './Login';
import Signup from './Signup';
import Chat from './Chat';

type Page = 'landing' | 'login' | 'signup' | 'chat';

export default function Auth() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const [userName, setUserName] = useState<string>('');

  const goToLanding = () => setCurrentPage('landing');
  const goToChat = (email: string) => {
    setUserName(email);
    setCurrentPage('chat');
  };

  return (
    <>
      {currentPage === 'landing' && (
        <Landing 
          onSignIn={() => setCurrentPage('login')} 
          onSignUp={() => setCurrentPage('signup')}
        />
      )}
      {currentPage === 'login' && (
        <Login 
          onCreateAccount={() => setCurrentPage('signup')}
          onLogoClick={goToLanding}
          onLoginSuccess={goToChat}
        />
      )}
      {currentPage === 'signup' && (
        <Signup 
          onBackToLogin={() => setCurrentPage('login')}
          onLogoClick={goToLanding}
        />
      )}
      {currentPage === 'chat' && (
        <Chat onLogout={goToLanding} userName={userName} />
      )}
    </>
  );
}
