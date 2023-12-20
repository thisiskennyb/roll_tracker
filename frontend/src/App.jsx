import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Login from './routes/Login'
import Home from './routes/Home'
import UserProfile from './routes/UserProfile'
import ResetPassword from './routes/ResetPassword'
import EmailReset from './routes/EmailReset'
import './App.css'

function App() {


  return (
    <Router>
     <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Home />} />
      <Route path="/profile" element={<UserProfile />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/email-reset" element={<EmailReset />} />
     </Routes>
     </Router>
  )
}

export default App
