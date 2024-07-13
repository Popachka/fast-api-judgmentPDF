import Card from "./components/Card";
import Header from "./components/Header";
import FileInput from "./components/FileInput";
import Footer from "./components/Footer";
function App() {
  return (
    <div className="App fh-full ">
      <Header />
      <div className="container p-6 mx-auto flex-col h-screen">
        <h1 className="mt-20 text-4xl">FAQ</h1>
        <div
          className="mt-5 border-double
         border-4 border-indigo-600 columns-2"
        >
          <div className=" p-5">
            Сайт поддерживает только определный вид документов
          </div>
          <div className="p-5">выфвфывфывыф</div>
        </div>
        <FileInput />
        <div className="mt-10 p-3 border-solid border-2 border-blue-300 h-full grid grid-cols-4 gap-4">
          <Card />
        </div>
        <Footer />
      </div>
    </div>
  );
}

export default App;
