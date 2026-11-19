import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import '@fontsource-variable/geist'
import './styles/tokens.css'
import './styles/base.css'
import './styles/tablas.css'
import './styles/formularios.css'
import './styles/paginas.css'
import './styles/documentos.css'
import { SesionProvider } from './features/auth/Sesion.jsx'
import { AvisoProvider } from './components/Aviso/Aviso.jsx'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <SesionProvider>
        <AvisoProvider>
          <App />
        </AvisoProvider>
      </SesionProvider>
    </BrowserRouter>
  </StrictMode>,
)
