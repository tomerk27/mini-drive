/**
 * App.jsx
 *
 * Top-level component. Delegates all routing to AppRouter, which handles
 * protected vs. public routes and renders the correct page.
 */
import AppRouter from "./routers/appRouter"

function App() {
  return (
    <>
      <AppRouter />
    </>
  )
}

export default App
