import './App.css'
import { Routes, Route } from 'react-router-dom'

function HomePage() {
  return (
    <div style={{ 
      background: '#181312', 
      color: 'white', 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      fontSize: '24px',
      flexDirection: 'column',
      gap: '2rem'
    }}>
      <h1>🎁 MR GIFT - Gift Giving Platform</h1>
      <p style={{ fontSize: '18px', color: '#FFB1EE' }}>
        Gift giving just became fun!
      </p>
      <div style={{
        padding: '1rem',
        background: 'rgba(255, 255, 255, 0.05)',
        borderRadius: '8px',
        fontSize: '14px',
        color: '#b8a89c'
      }}>
        <p>🚀 Deployed successfully on Vercel!</p>
      </div>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
    </Routes>
  )
}

export default App
