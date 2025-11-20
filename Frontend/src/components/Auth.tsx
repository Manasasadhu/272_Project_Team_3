import { useState } from 'react';
import Landing from './Landing';
import Login from './Login';
import Signup from './Signup';
import Chat from './Chat';
import HowItWorks from './HowItWorks';

type Page = 'landing' | 'login' | 'signup' | 'chat' | 'how-it-works';

export default function Auth() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const [userName, setUserName] = useState<string>('');

  const goToLanding = () => setCurrentPage('landing');
  const goToChat = (email: string) => {
    setUserName(email);
    setCurrentPage('chat');
  };
  const goToHowItWorks = () => setCurrentPage('how-it-works');

  return (
    <>
      {currentPage === 'landing' && (
        <Landing 
          onSignIn={() => setCurrentPage('login')} 
          onSignUp={() => setCurrentPage('signup')}
          onHowItWorks={goToHowItWorks}
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
          onSignupSuccess={goToChat}
        />
      )}
      {currentPage === 'chat' && (
        <Chat onLogout={goToLanding} userName={userName} />
      )}
      {currentPage === 'how-it-works' && (
        <HowItWorks 
          onClose={goToLanding}
          onGetStarted={() => setCurrentPage('signup')}
        />
      )}
    </>
  );
}
