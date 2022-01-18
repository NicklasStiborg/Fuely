import logo from './logo.svg';
import Navbar from './components/navbar/navbar';
import './App.css';
import Footer from './components/footer/footer';
import FuelTable from './components/fuelTable/fuelTable';

function App() {
  return (
    <div className="App">
      <Navbar />
      <FuelTable className="fuelTable"/>
      <Footer />
    </div>
  );
}

export default App;
